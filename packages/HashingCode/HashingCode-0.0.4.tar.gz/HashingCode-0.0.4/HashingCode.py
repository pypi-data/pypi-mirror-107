def copyright():
    __author__ = "Abderrahman Hiroual"
    __copyright__ = f"Copyright (C) 2021 {__author__}"
    __license__ = "Python developer"
    __version__ = "0.0.4"
    __All__ = __author__,__copyright__,__version__,__license__
    print(__All__)
def enc254(arg):
    global Encrypt
    global parameter
    List = []
    parameter = {"\n":563 * 63 + 65,"'":561 * 61 + 63,",":559 * 58 + 60 + 1,":":555 * 57 + 59 + 1,"\"":533 * 55 + 57 + 1,"": "", " ": 0 * 0 + 0, ".": 67918, "a": 11 * 3 + 3, "b": 33 * 5 + 4, "c": 55 * 7 + 7, "d": 77 * 8 + 9,
                 "e": 98 * 9 + 11, "f": 111 * 13 + 13, "g": 133 * 14 + 15, "h": 155 * 17 + 17, "i": 177 * 19 + 19,
                 "j": 199 * 21 + 12, "k": 211 * 23 + 22, "l": 233 * 25 + 22, "m": 254 * 23 + 22, "n": 277 * 26 + 22,
                 "o": 299 * 31 + 23, "p": 327 * 34 + 33, "q": 333 * 35 + 33, "r": 355 * 37 + 33, "s": 377 * 39 + 33,
                 "t": 399 * 41 + 34, "u": 411 * 43 + 44, "v": 433 * 45 + 44, "w": 455 * 47 + 44, "x": 477 * 49 + 44,
                 "y": 499 * 51 + 45, "z": 511 * 53 + 55, "A": 11 * 3 + 3 + 1, "B": 33 * 5 + 6, "C": 55 * 7 + 7 + 1,
                 "D": 77 * 8 + 9 + 1,
                 "E": 98 * 9 + 11 + 1, "F": 111 * 13 + 13 + 1, "G": 133 * 14 + 15 + 1, "H": 155 * 17 + 17 + 1,
                 "I": 177 * 19 + 19 + 1,
                 "J": 199 * 21 + 12 + 1, "K": 211 * 23 + 22 + 1, "L": 233 * 25 + 22 + 1, "M": 254 * 23 + 22 + 1,
                 "N": 277 * 26 + 22 + 1,
                 "O": 299 * 31 + 23 + 1, "P": 327 * 34 + 33 + 1, "Q": 333 * 35 + 33 + 1, "R": 355 * 37 + 33 + 1,
                 "S": 377 * 39 + 33 + 1,
                 "T": 399 * 41 + 34 + 1, "U": 411 * 43 + 44 + 1, "V": 433 * 45 + 44 + 2, "W": 455 * 47 + 44 + 3,
                 "X": 477 * 49 + 44 + 1,
                 "Y": 499 * 51 + 45 + 1, "Z": 511 * 53 + 55 + 1}
    for item in str(arg):
        if item in parameter:
            Encrypt = str(parameter.get(item, ""))
        else:
            Encrypt = "0"
        List.append(Encrypt)
    return "".join(List)


def dec254(arg):
    global Encrypt2
    List = []
    List2 = []
    parameter2 = {"35534":"\n","34284":"'","32483":",","0": " ","31695":":","29373":"\"", " ": " ", "67918": ".", "36": "a", "169": "b", "392": "c", "625": "d",
                  "893": "e", "1456": "f", "1877": "g", "2652": "h", "3382": "i",
                  "4191": "j", "4875": "k", "5847": "l", "5864": "m", "7224": "n",
                  "9292": "o", "11151": "p", "11688": "q", "13168": "r", "14736": "s",
                  "16393": "t", "17717": "u", "19529": "v", "21429": "w", "23417": "x",
                  "25494": "y", "27138": "z", "37": "A", "171": "B", "393": "C", "626": "D",
                  "894": "E", "1457": "F", "1878": "G", "2653": "H", "3383": "I",
                  "4192": "J", "4876": "K", "5848": "L", "5865": "M", "7225": "N",
                  "9293": "O", "11152": "P", "11689": "Q", "13169": "R", "14737": "S",
                  "16394": "T", "17718": "U", "19531": "V", "21432": "W", "23418": "X",
                  "25495": "Y", "27139": "Z"}
    for item in str(arg):
        List2.append(item)
        Get = "".join(List2)
        if Get in parameter2:
            Encrypt2 = parameter2.get(Get, ".")
            List.append(Encrypt2)
            List2.clear()
        else:
            if len(List2) == 7:
                List2.clear()
            else:
                pass
    return "".join(List)

