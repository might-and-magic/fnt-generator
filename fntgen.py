# Might and Magic 6 7 8 and Heroes 3 FNT (font) File Generator for Multiple Languages (Python Script)
# 
# Copyright (c) 2020 Tom Chen (tomchen.org)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation self.files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import struct
import os
import bdfparser as bp
import dbcs4fntgen as dbcs # double-byte character set (DBCS) support for fntgen


class FntGen(object):

	def __init__(self, bdfFileName):
		self.bpo = bp.BdfParser(bdfFileName)
		self.setCharset().setDecoration().setSpacing()


	# For double-byte charsets, only gb2312, gbk, big5, euc_jp, euc_kr are supported
	#   (Change CHARSET_RANGE in dbcs4fntgen to support more)
	#   (aliases are not supported)
	# All single-byte charsets are supported, typical example:
	#   cp1252 (default value, for latin alphabet-based languages),
	#   cp1251 (for Cyrillic script-based languages)
	# See https://docs.python.org/library/codecs.html#standard-encodings for a full list
	def setCharset(self, charset='cp1252', bytenumber=None):
		self.charset = charset
		if bytenumber == None:
			if charset in ['gb2312', 'gbk', 'big5', 'euc_jp', 'euc_kr']:
				self.bytenumber = 2 # double-byte character set such as CJK (Chinese, Japanese, Korean)
			else:
				self.bytenumber = 1 # single-byte character set
		else:
			self.bytenumber = bytenumber
		return self


	# Could be None (default value), 'shadow', 'glow' or 'black'
	def setDecoration(self, decoration=None):
		self.decoration = decoration
		if decoration == None:
			self.outputWidthPropName = 'outputW'
			self.outputHeightPropName = 'outputH'
			self.fbbH = self.bpo.fbbH # all glyphs have a same height (fbbH)
			self.fbbW = self.bpo.fbbW # global width (fbbW) is usually overridden by individual glyph's width
		elif decoration == 'shadow':
			self.outputWidthPropName = 'shadowedOutputW'
			self.outputHeightPropName = 'shadowedOutputH'
			self.fbbH = self.bpo.fbbHShadowed
			self.fbbW = self.bpo.fbbWShadowed
		elif decoration == 'glow':
			self.outputWidthPropName = 'glowedOutputW'
			self.outputHeightPropName = 'glowedOutputH'
			self.fbbH = self.bpo.fbbHGlowed
			self.fbbW = self.bpo.fbbWGlowed
		elif decoration == 'black':
			self.outputWidthPropName = 'outputW'
			self.outputHeightPropName = 'outputH'
			self.fbbH = self.bpo.fbbH
			self.fbbW = self.bpo.fbbW
		return self


	# set space before/after every character, defaults are 0
	def setSpacing(self, spaceBefore=0, spaceAfter=0):
		self.spaceBefore = spaceBefore
		self.spaceAfter = spaceAfter
		return self


	# path is optional
	def output(self, fileName, path):
		if self.bytenumber == 1:
			self.writeBytesToFile(
				self.glyphList2FntBytes(self.getGlyphList(
					map(lambda x: bytes([x]), range(256)),
					self.charset
				)),
				fileName.replace("<SIZE>", str(self.fbbH)) + '.fnt',
				path
			)
		else:
			charsetCodeList = self.getDBCSCharsetCodeList(self.charset)
			for highByteSet in charsetCodeList:
				self.writeBytesToFile(
					self.glyphList2FntBytes(self.getGlyphList(
						highByteSet['lowByteUnicodeDecList'],
						self.charset
					)),
					fileName.replace("<SIZE>", str(self.fbbH)) + highByteSet['highByteHexStr'] + '.fnt',
					path
				)


	def getDBCSCharsetCodeList(self, charset):
		charsetCodeList = []
		
		for highByte in dbcs.CHARSET_RANGE[charset]['highByteRange']:
			lowByteUnicodeDecList = [None]*256
			highByteHexStr = hex(highByte)[2:].upper()
			for lowByte in dbcs.CHARSET_RANGE[charset]['lowByteRange']:
				lowByteUnicodeDecList[lowByte] = bytes([highByte]) + bytes([lowByte])
			charsetCodeList.append({
				'highByteHexStr': highByteHexStr,
				'lowByteUnicodeDecList': lowByteUnicodeDecList
			})
		
		return charsetCodeList


	def getGlyphList(self, iterable, charset):

		glyphList = []
		specialCharsetList = dbcs.CHARSET_FIX.get(charset)

		def unicodeDecimals(char, chunk_size=2):
			encoded_char = char.encode('utf-16-be')
			decimals = []
			for i in range(0, len(encoded_char), chunk_size):
				chunk = encoded_char[i:i+chunk_size]
				decimals.append(int.from_bytes(chunk, 'big'))
			return decimals

		def tryToGetGlyphInfo(unicodeDecimal):
			try:
				return self.bpo.getGlyphInfo(unicodeDecimal)
			except:
				return None

		# iterable is a iterable of bytes encoded in local encoding
		for byt in iterable:
			unicodeDecimal = None

			if byt == None:
				glyphInfo = None
				unicodeDecimal = '' # skip NORMAL block
			elif specialCharsetList != None:
				specialList = specialCharsetList.get(byt)
				if specialList != None:
					specialList = iter(specialList)
					while True:
						# skip NORMAL block
						unicodeDecimal = next(specialList, None)
						if unicodeDecimal == None:
							glyphInfo = None
							unicodeDecimal = ''
							break
						elif unicodeDecimal == 'full-width space':
							glyphInfo = 'full-width space'
							break
						glyphInfo = tryToGetGlyphInfo(unicodeDecimal)
						if glyphInfo != None:
							break

			# NORMAL block
			if unicodeDecimal == None:
				try:
					unicodeDecimal = unicodeDecimals(byt.decode(charset), 8)[0]
					glyphInfo = tryToGetGlyphInfo(unicodeDecimal)
				except:
					glyphInfo = None

			if glyphInfo == None:
				glyphObj = {
					"width": 0,
					"spaceBefore": 0,
					"spaceAfter": 0,
					"bitmap": b''
				}

			elif glyphInfo == 'full-width space':
				glyphObj = {
					"width": self.fbbW,
					"spaceBefore": 0,
					"spaceAfter": 0,
					"bitmap": b'\x00'*(self.fbbW*self.fbbH)
				}

			else:
				if self.decoration == None:
					bitmap = self.bpo.getCharHexByUnicode(unicodeDecimal)
				elif self.decoration == 'shadow':
					bitmap = self.bpo.getShadowedCharHexByUnicode(unicodeDecimal)
				elif self.decoration == 'glow':
					bitmap = self.bpo.getGlowedCharHexByUnicode(unicodeDecimal)
				elif self.decoration == 'black':
					bitmap = self.bpo.getBlackedCharHexByUnicode(unicodeDecimal)
				glyphObj = {
					"width": self.bpo.getGlyphInfo(unicodeDecimal)[self.outputWidthPropName],
					"spaceBefore": self.spaceBefore,
					"spaceAfter": self.spaceAfter,
					"bitmap": bitmap
				}

			glyphList.append(glyphObj)

		return glyphList


	def glyphList2FntBytes(self, glyphList):
		header = 0x08ff1f # Usually is 08ff1f, could alse be: 08ff1e, 08ff40

		glyphWidthList = []
		glyphBitmapOffsetList = []
		glyphBitmapOffsetTemp = 0
		glyphBitmapBytes = bytes()

		for glyphWidthDict in glyphList:
			glyphWidthList.extend([glyphWidthDict["spaceBefore"], glyphWidthDict["width"], glyphWidthDict["spaceAfter"]])
			glyphBitmapOffsetList.append(glyphBitmapOffsetTemp)
			glyphBitmapOffsetTemp += len(glyphWidthDict["bitmap"])
			glyphBitmapBytes += glyphWidthDict["bitmap"]

		# 768 = 3*256
		fnt = struct.Struct(f'= i I 24x 768i 256I {len(glyphBitmapBytes)}s')
		byt = fnt.pack(header, self.fbbH << 8, *glyphWidthList, *glyphBitmapOffsetList, glyphBitmapBytes)

		return byt


	def writeBytesToFile(self, contentBytes, fileName, path=''):
		curDir = os.path.dirname(os.path.realpath('__file__'))
		if not os.path.exists(os.path.join(curDir, path)):
			os.makedirs(os.path.join(curDir, path))
		outFile = open(os.path.join(curDir, path, fileName), "wb")
		outFile.write(contentBytes)
		outFile.close()
