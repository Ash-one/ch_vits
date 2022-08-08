_pause = ['sil','eos',"sp","#0", "#1", "#2", "#3",'#4']
# sil表示一段静音，通常加在句子的前后
# eos表示结束符
# 0表示每个音素后的极短停顿，使用0级停顿时就不能使用VITS自带的add_blank加停顿
# 1表示每个韵律词后的短停顿
# 2表示每个韵律短语后的停顿
# 3表示每个语调短语后的停顿，包括逗号顿号
# 4表示句子的结束

_initials = [
    "^",
    "b",
    "c",
    "ch",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "sh",
    "t",
    "x",
    "z",
    "zh",
]

_tones = ["1", "2", "3", "4", "5"]

_finals = [
    "a",
    "ai",
    "an",
    "ang",
    "ao",
    "e",
    "ei",
    "en",
    "eng",
    "er",
    "i",
    "ia",
    "ian",
    "iang",
    "iao",
    "ie",
    "ii",
    "iii",
    "in",
    "ing",
    "iong",
    "iou",
    "o",
    "ong",
    "ou",
    "u",
    "ua",
    "uai",
    "uan",
    "uang",
    "uei",
    "uen",
    "ueng",
    "uo",
    "v",
    "van",
    "ve",
    "vn",
]

symbols = _pause + _initials + [i + j for i in _finals for j in _tones]