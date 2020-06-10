class colors:
    gray = '\033[90m'
    orange = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    pink = '\033[95m'
    lightblue = '\033[96m'
    black = '\033[97'

    bold = '\033[1m'
    italic = '\033[3m'
    underline = '\033[4m'
    marked = '\033[7m'
    deleted = '\033[9m'
    squared = '\033[51m'


def color_print(string: str, color: str):
    print(color + string + '\033[1m')