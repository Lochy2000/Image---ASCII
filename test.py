def create_ascii_art(text):
    ascii_letters = {
        'A': [
            "  A  ",
            " A A ",
            "AAAAA",
            "A   A",
            "A   A"
        ],
        'B': [
            "BBBB ",
            "B   B",
            "BBBB ",
            "B   B",
            "BBBB "
        ],
        'C': [
            " CCC ",
            "C   C",
            "C    ",
            "C   C",
            " CCC "
        ],
        'D': [
            "DDDD ",
            "D   D",
            "D   D",
            "D   D",
            "DDDD "
        ],
        'E': [
            "EEEEE",
            "E    ",
            "EEE  ",
            "E    ",
            "EEEEE"
        ],
        'F': [
            "FFFFF",
            "F    ",
            "FFF  ",
            "F    ",
            "F    "
        ],
        'G': [
            " GGG ",
            "G    ",
            "G  GG",
            "G   G",
            " GGG "
        ],
        'H': [
            "H   H",
            "H   H",
            "HHHHH",
            "H   H",
            "H   H"
        ],
        'I': [
            "IIIII",
            "  I  ",
            "  I  ",
            "  I  ",
            "IIIII"
        ],
        'J': [
            "JJJJJ",
            "   J ",
            "   J ",
            "J  J ",
            " JJ  "
        ],
        'K': [
            "K   K",
            "K  K ",
            "KKK  ",
            "K  K ",
            "K   K"
        ],
        'L': [
            "L    ",
            "L    ",
            "L    ",
            "L    ",
            "LLLLL"
        ],
        'M': [
            "M   M",
            "MM MM",
            "M M M",
            "M   M",
            "M   M"
        ],
        'N': [
            "N   N",
            "NN  N",
            "N N N",
            "N  NN",
            "N   N"
        ],
        'O': [
            " OOO ",
            "O   O",
            "O   O",
            "O   O",
            " OOO "
        ],
        'P': [
            "PPPP ",
            "P   P",
            "PPPP ",
            "P    ",
            "P    "
        ],
        'Q': [
            " QQQ ",
            "Q   Q",
            "Q Q Q",
            "Q  Q ",
            " QQ Q"
        ],
        'R': [
            "RRRR ",
            "R   R",
            "RRRR ",
            "R  R ",
            "R   R"
        ],
        'S': [
            " SSS ",
            "S    ",
            " SSS ",
            "    S",
            "SSSS "
        ],
        'T': [
            "TTTTT",
            "  T  ",
            "  T  ",
            "  T  ",
            "  T  "
        ],
        'U': [
            "U   U",
            "U   U",
            "U   U",
            "U   U",
            " UUU "
        ],
        'V': [
            "V   V",
            "V   V",
            "V   V",
            " V V ",
            "  V  "
        ],
        'W': [
            "W   W",
            "W   W",
            "W W W",
            "WW WW",
            "W   W"
        ],
        'X': [
            "X   X",
            " X X ",
            "  X  ",
            " X X ",
            "X   X"
        ],
        'Y': [
            "Y   Y",
            " Y Y ",
            "  Y  ",
            "  Y  ",
            "  Y  "
        ],
        'Z': [
            "ZZZZZ",
            "   Z ",
            "  Z  ",
            " Z   ",
            "ZZZZZ"
        ],
        ' ': [
            "     ",
            "     ",
            "     ",
            "     ",
            "     "
        ]
    }
    
    output = [""] * 5
    text = text.upper()
    
    for char in text:
        if char in ascii_letters:
            for i in range(5):
                output[i] += ascii_letters[char][i] + " "
        else:
            for i in range(5):
                output[i] += "     "
    
    return "\n".join(output)

if __name__ == "__main__":
    text = input("Enter text: ")
    print(create_ascii_art(text))