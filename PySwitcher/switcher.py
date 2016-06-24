import win32clipboard
import os
import logging

from initialization import get_options

# TODO: полный рефакторинг
# TODO: проверять наличие файлов языков
# TODO: вынести отдельным модулем загрузку языков

logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def load_langs(langs, path=os.getcwd()):  # загружаем языки из файла
    layouts = []
    path += '\\lang\\'
    langs = langs.split(',')
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        logging.critical('Language dictionaries doesn\'t found. Please, place them in /lang directory')
        messages.append('Language dictionaries doesn\'t found. Please, place them in /lang directory')
        return layouts
    lang_list = []
    for lfile in files:
        if lfile.endswith('.txt'):
            lang_list.append(lfile.split('.')[0])
    if langs[0] in lang_list:
        data_file = open('{}/{}.txt'.format(path, langs[0]))
        layouts.append(data_file.readline().replace('\n', ''))
        data_file.close()
    if langs[1] in lang_list:
        data_file = open('{}/{}.txt'.format(path, langs[1]))
        layouts.append(data_file.readline().replace('\n', ''))
        data_file.close()
    if not layouts:
        logging.error('Language dictionaries doesn\'t found')
    return layouts


def cross_chars(layouts):  # определяем пересекающиеся символы
    result = ''
    for i in layouts[0]:
        if i in layouts[1]:
            result += i
    return result


def lang_define(phrase, layouts):
    if layouts:
        for char in phrase:
            if char not in cross_list:
                if char in layouts[0]:
                    lang_setup = (0, 1)
                    break
                elif char in layouts[1]:
                    lang_setup = (1, 0)
                    break
            else:
                lang_setup = None  # В случае, если слово целиком из пересекающихся символов
    else:
        lang_setup = None
    return lang_setup


def switcher(phrase):
    temp = []
    result = phrase.split()

    def sub_switch(word):
        lang_setup = lang_define(word, layouts)
        temp = ''
        if lang_setup:
            for position, char in list(enumerate(word)):
                if char == '\\':
                    temp += '\\'
                elif char == ' ':
                    temp += ' '
                else:
                    try:
                        i = layouts[lang_setup[0]].index(char)
                        temp += layouts[lang_setup[1]][i]
                    except ValueError:
                        logging.error('Symbol not founded. Searching in other language')
                        try:
                            lang_setup = lang_define(word, layouts)
                            i = layouts[lang_setup[0]].index(char)
                            temp += layouts[lang_setup[1]][i]
                        except ValueError:
                            logging.error('Symbol {} not find'.format(char))
            return temp
        else:
            return word

    for word in result:
        temp.append(sub_switch(word))
    result = ' '.join(temp)

    return result


messages = []
options = get_options()
layouts = load_langs(options['langs'])
if layouts:
    cross_list = cross_chars(layouts)
warning_level = options['warning_level']
encoding = options['encoding']


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
                logging.error('Problem with encoding: {}.\tPlease specify encoding in options.txt'.format(encoding))
    except Exception as e:
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


if __name__ == '__main__':
    data = copy()
    print(data)
    print(paste(data))
