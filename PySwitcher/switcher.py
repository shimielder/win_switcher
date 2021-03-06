import win32clipboard
import os
import logging

from initialization import get_options, set_loglevel

# TODO: полный рефакторинг
# TODO: вынести отдельным модулем загрузку языков


def load_langs(layouts):  # загружаем языки из файла
    if not layouts[0] or not layouts[1]:
        logging.error('Dictionaries is empty.')
    elif len(layouts[0]) != len(layouts[1]):
        logging.error('Dictionaries lengths is not equal')
    return layouts


def cross_chars(layouts):  # определяем пересекающиеся символы
    result = ''
    for i in layouts[0]:
        if i in layouts[1]:
            result += i
    return result


def lang_define(char, layouts):
    lang_setup = ()
    if char in layouts[0]:
        lang_setup = (0, 1)
    elif char in layouts[1]:
        lang_setup = (1, 0)
    return lang_setup


def switcher(phrase):
    #    cross_list = cross_chars(layouts)
    escape = (' ', '\\')
    lang_setup = ()
    phrase_length = len(phrase)
    result = ''
    temp = ''
    for position, char in enumerate(list(phrase)):
        if char in cross_list:
            if len(lang_setup) > 0:
                i = layouts[lang_setup[0]].index(char)
                result += layouts[lang_setup[1]][i]
            else:
                temp += char
            if len(temp) == phrase_length:
                result = temp
            elif position == phrase_length - 1:
                result += temp
        else:
            temp += char
            lang_setup = lang_define(char, layouts)
            for char in list(temp):
                if char in escape:
                    result += char
                elif len(lang_setup) > 0:
                    i = layouts[lang_setup[0]].index(char)
                    result += layouts[lang_setup[1]][i]
                else:
                    result += char
            temp = ''
    return result


logger = logging.getLogger(__name__)
messages = []
options = get_options()
layouts = load_langs(options['layouts'])
if layouts:
    cross_list = cross_chars(layouts)
encoding = options['encoding']
set_loglevel(options['log_level'])

def copy():
    data = ''
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
        if data == None:
            return None
        if type(data) is bytes:
            try:
                data = data.decode(encoding)
            except UnicodeDecodeError:
                logging.error('Problem with encoding: {}.'.format(encoding))
    except Exception:
        logging.error('Something happened while copying from clipboard:\n', exc_info=True)
    return data


def paste(data):
    data = switcher(data)
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, data)
        win32clipboard.CloseClipboard()
    except Exception as e:
        logging.error('Something happened while pasting to clipboard:\n', exc_info=True)
    return data


def clean_clipboard():
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
    except Exception:
        logging.error('Something happened while resetting clipboard:\n', exc_info=True)


if __name__ == '__main__':
    data = copy()
    print(data)
    print(paste(data))
