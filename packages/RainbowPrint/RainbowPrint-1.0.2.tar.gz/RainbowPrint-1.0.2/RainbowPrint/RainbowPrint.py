# 0	终端默认设置
# 1	高亮显示
# 4	使用下划线
# 5	闪烁
# 7	反白显示
# 8	不可见

from enum import Enum, unique
from datetime import datetime

@unique
class TextColor(Enum):
    Default = 0
    BlACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


@unique
class BackgroundColor(Enum):
    Default = 0
    BlACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47


@unique
class DisplayMode(Enum):
    TERMINAL_DEFAULT_SETTINGS = 0
    HIGHLIGHT = 1
    USE_UNDERLINE = 4
    BLINK = 5
    BACKWHITE_DISPLAY = 7
    INVISIBLE = 8


base_str = '\033[{};{};{}m{}\033[0m'

def rainbow_print(data, display_mode=DisplayMode.HIGHLIGHT, text_color=TextColor.YELLOW,
                  background=BackgroundColor.BLUE):
    """
    Output color text in the terminal

    Args:
        data: Text that needs to be printed.
        display_mode:
        text_color: the color of text.
        background: the color of background.
    """
    print(base_str.format(display_mode.value, text_color.value, background.value, data))



def get_time():
    return '[{}]'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])


def info(string_data):
    print(get_time(), base_str.format(DisplayMode.HIGHLIGHT.value,TextColor.WHITE.value,BackgroundColor.GREEN.value,' INFO  '), green(string_data))


def error(string_data):
    print(get_time(),base_str.format(DisplayMode.HIGHLIGHT.value,TextColor.WHITE.value,BackgroundColor.RED.value,' ERROR '),red(string_data))


def debug(string_data):
    print(get_time(),base_str.format(DisplayMode.HIGHLIGHT.value,TextColor.WHITE.value,BackgroundColor.MAGENTA.value,' DEBUG '),magenta(string_data))



def red(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.RED.value, data)


def black(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.BlACK.value, data)


def green(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.GREEN.value, data)


def yellow(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.YELLOW.value, data)


def blue(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.BLUE.value, data)


def magenta(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.MAGENTA.value, data)


def cyan(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.CYAN.value, data)


def white(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.WHITE.value, data)


def rainbow():
    t = [i for i in range(30, 38)]
    b = [i for i in range(40, 48)]
    for tc in t:
        for bc in b:
            print('\033[1;{};{}m{} [textcolor:{}, background:{}]\033[0m'.format(tc, bc, 'RainBow', TextColor(tc).name,
                                                                                BackgroundColor(bc).name))


def help():
    dispaly_mode = '''
     0	终端默认设置
     1	高亮显示
     4	使用下划线
     5	闪烁
     7	反白显示
     8	不可见
    '''
    print(dispaly_mode)

def test():
    for v in TextColor:
        print(v.value)
# test()