def up_char(n):
    return f"\033[{n}A"


def down_char(n):
    return f"\033[{n}B"


def clr_char():
    return "\x1B[K"
