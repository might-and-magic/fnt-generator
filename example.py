import fntgen as f


# Uncomment, modify and execute the following code


# unifont for various languages:

FntObject = f.FntGen('example_fonts/bdf/unifont-9.0.06.bdf')
FntObject.setCharset('cp1252').setDecoration('shadow').output('FONT', 'uni_cp1252')
FntObject.setCharset('cp1251').setDecoration().output('FONT', 'uni_cp1251')
FntObject.setCharset('cp1250').setDecoration('black').output('FONT', 'uni_cp1250')
FntObject.setCharset('gb2312').setDecoration('glow').output('DBCS_<SIZE>_', 'uni_gb2312')
FntObject.setCharset('big5').setDecoration().output('DBCS_<SIZE>_', 'uni_big5')



# For MM6-8 zh_CN:

FntObject = f.FntGen('example_fonts/bdf/SimSun-12.bdf')
FntObject.setCharset('gb2312').setDecoration('shadow').output('DBCS_<SIZE>_', 'zh_CN_small/')

FntObject = f.FntGen('example_fonts/bdf/SimSun-14.bdf')
FntObject.setCharset('gb2312').setDecoration('black').output('DBCS_<SIZE>b_', 'zh_CN_mid-b/')

FntObject = f.FntGen('example_fonts/bdf/SimSun-14.bdf')
FntObject.setCharset('gb2312').setDecoration('shadow').output('DBCS_<SIZE>_', 'zh_CN_mid/')

FntObject = f.FntGen('example_fonts/bdf/FZCKJW-GB1-0-26.bdf')
FntObject.setCharset('gb2312').setDecoration('glow').output('DBCS_<SIZE>_', 'zh_CN_large/')



# For MM6-8 zh_TW:

FntObject = f.FntGen('example_fonts/bdf/MingLiU-98-13.bdf')
FntObject.setCharset('big5').setDecoration('shadow').output('DBCS_<SIZE>_', 'zh_TW_small/')

FntObject = f.FntGen('example_fonts/bdf/MingLiU-98-15.bdf')
FntObject.setCharset('big5').setDecoration('black').output('DBCS_<SIZE>b_', 'zh_TW_mid-b/')

FntObject = f.FntGen('example_fonts/bdf/MingLiU-98-15.bdf')
FntObject.setCharset('big5').setDecoration('shadow').output('DBCS_<SIZE>_', 'zh_TW_mid/')

FntObject = f.FntGen('example_fonts/bdf/HanWangYanKai-26.bdf')
FntObject.setCharset('big5').setDecoration('glow').output('DBCS_<SIZE>_', 'zh_TW_large/')
