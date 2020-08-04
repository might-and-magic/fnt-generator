# FNT Generator

[![MIT License](https://img.shields.io/github/license/might-and-magic/fnt-generator)](https://github.com/might-and-magic/fnt-generator/blob/master/LICENSE "MIT License")

Might and Magic 6 7 8 and Heroes 3 FNT (font) File Generator for Multiple Languages (Python Script). It uses another small library of mine: [BDF Parser](https://github.com/tomchen/bdfparser)

## Usage

### Instantiation

```python
FntObject = FntGen(<FONT_FILE_PATH>)
```

Example:

```python
FntObject = FntGen('example_fonts/bdf/unifont-9.0.06.bdf')
```

### `setCharset`

```python
FntObject.setCharset(<CHARSET>)
```

Set charset. `CHARSET` is a string

* All single-byte charsets are supported, typical example:
  * `cp1252` (**default value**, for latin alphabet-based languages, e.g. en, fr, de, es, it)
  * `cp1251` (for Cyrillic script-based languages, e.g. ru)
  * `cp1250` (for Central European languages, e.g. cs, pl)
* For double-byte charsets (DBCS), only `gb2312` (zh_CN), `gbk` (zh_CN), `big5` (zh_TW), `euc_jp` (ja), `euc_kr` (ko) are supported

Example:

```python
FntObject.setCharset('cp1252')
```

### `setDecoration`

```python
FntObject.setDecoration(<DECORATION>)
```

Set decoration. `DECORATION` is a string, it can be: *empty*, `shadow`, `black`, or `glow`

Example:

```python
FntObject.setDecoration('shadow')
```

### `output`

```python
FntObject.output(<FILE_NAME>, [PATH])
```

Output .fnt file(s). `FILE_NAME` is a required string parameter, `PATH` is an optional string parameter.

If there is any "`<SIZE>`" in `FILE_NAME` parameter, it will be replaced by the final font's actual size.

For single-byte charsets, a single .fnt file is generated.

For double-byte charsets (DBCS), it outputs multiple .fnt files. Each file name is followed by a hex representation of its corresponding high byte.

Examples:

```python
FntObject.output('myfont', 'folder')
FntObject.output('myfont_<SIZE>_', 'folder2')
```

### Combined examples

```python
import fntgen as f
FntObject = f.FntGen('example_fonts/bdf/unifont-9.0.06.bdf')
FntObject.setCharset('cp1252').setDecoration('shadow').output('FONT', 'uni_cp1252')
FntObject.setCharset('gb2312').setDecoration('glow').output('DBCS_<SIZE>_', 'uni_gb2312')
```

(More combined examples: [example.py](https://github.com/might-and-magic/fnt-generator/blob/master/example.py))

## Other tools
* [Example .bdf fonts](https://github.com/might-and-magic/fnt-generator/tree/master/example_fonts/bdf):
  * GNU Unifont: [Wikipedia article](https://en.wikipedia.org/wiki/GNU_Unifont). Unicode font (intended to support "all" common languages)
  * M+ FONTS: [Wikipedia article](https://en.wikipedia.org/wiki/M%2B_FONTS). Japanese font
  * HanWangYanKai 王漢宗自由字型顏體: Traditional Chinese font
  * MingLiU 細明體: Traditional Chinese font
  * SimSun 中易宋体: Simplified Chinese font
  * STKaiti 华文楷体: Simplified Chinese font
  * FZCKJW 方正粗楷简体: Simplified Chinese font
* [FNT font file editors](https://github.com/might-and-magic/fnt-generator/tree/master/tools/fnt_editors): 2 old, executable FNT file editors. Just an archive. Not written by me.
* [otf2bdf](https://github.com/tomchen/bdfparser/tree/master/tools/otf2bdf): OpenType to BDF Converter. Just an archive. Not written by me.

## License

* Python code is written by me (Tom CHEN) and is released under the MIT License.
* [otf2bdf](https://github.com/tomchen/bdfparser/tree/master/tools/otf2bdf): see its page.
* FNT font file editors: fair use.
* Example .bdf fonts:
  * GNU Unifont: [GNU General Public License](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html), by Roman Czyborra, Paul Hardy, part of the GNU Project
  * M+ FONTS: [a free license](https://mplus-fonts.osdn.jp/about-en.html#license), designed by Coji Morishita
  * HanWangYanKai 王漢宗自由字型顏體: [GNU General Public License](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html), by 王漢宗
  * Other fonts are proprietary, and are used non-commercially and fairly