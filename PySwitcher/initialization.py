from win32api import GetKeyboardLayout
from win32gui import GetForegroundWindow
from ctypes import windll
from os import getcwd
from time import sleep
import logging

import keyboard

logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def get_options(path=getcwd()):
    options = load_from()
    if 'switch_combination' in options:
        comb = options['switch_combination']
        if not comb_check(comb):
            options['switch_combination'] = combination_definition()
    save_to(options)
    return options


def load_from(path=getcwd()):
    logging.info('Loading options from file...')
    options = {}
    try:
        opt_file = open('{}\\options.txt'.format(path), 'r')
        data = opt_file.readlines()
        opt_file.close()
        if not data:
            logging.error('Options file is empty...')
            return generate_default(path)
        for item in data:
            key = item.split('=')[0]
            value = item.split('=')[1].replace('\n', '')
            if value == 'empty':
                value = None
            options[key] = value
        return options
    except FileNotFoundError:
        logging.error('Options file not found...')
        return generate_default(path)


def save_to(options, path=getcwd()):
    logging.info('Saving options to file...')
    opt_file = open('{}\\options.txt'.format(path), 'w')
    for opt in options:
        key = opt
        value = options[opt]
        if not value:
            value = 'empty'
        opt_file.write(key + '=' + value + '\n')
    opt_file.close()


def comb_check(comb):
    logging.info('Checking switch combination...')
    try:
        if not comb:
            return False
        user32 = windll.user32
        cur_hwnd = GetForegroundWindow()
        cur_pid = user32.GetWindowThreadProcessId(cur_hwnd, None)  # Получаем pid процесса
        current_lang = GetKeyboardLayout(cur_pid)  # Получаем раскладку по pid
        keyboard.send(comb)
        sleep(0.1)
        if 'alt' in comb: keyboard.send('alt')  # Нажимаем Alt снова, если он есть в комбинации
        if current_lang != GetKeyboardLayout(cur_pid):
            keyboard.send(comb)
            return True
        else:
            return False
    except ValueError:
        logging.error('An error occured while checking switch combination', exc_info=True)
        return False


def generate_default(path=getcwd()):
    logging.info('Generating default options...')
    options = {
        'hotkey': 'pause',
        'langs': 'ru,en',
        'warning_level': 'DEBUG',
        'encoding': 'cp1251',
        'switch_combination': combination_definition()
    }
    return options


def combination_definition():
    logging.info('Defining switch combination...')
    user32 = windll.user32
    cur_hwnd = GetForegroundWindow()
    cur_pid = user32.GetWindowThreadProcessId(cur_hwnd, None)  # Получаем pid процесса
    current_lang = GetKeyboardLayout(cur_pid)  # Получаем раскладку по pid
    combinations = (('ctrl+shift'), ('alt+shift'), ('alt+shift+ctrl'))
    #    logging.debug('\nUser32: {}\nhwnd: {}\nPID: {}\nLang: {}'.format(user32, cur_hwnd, cur_pid, current_lang))
    for comb in combinations:
        keyboard.send(comb)
        sleep(0.1)
        if 'alt' in comb: keyboard.send('alt')  # Нажимаем Alt снова, если он есть в комбинации
        if current_lang != GetKeyboardLayout(cur_pid):
            logging.debug('Switch combination found: {}'.format(comb))
            keyboard.send(comb)
            return comb
    return None


if __name__ == '__main__':
    options = get_options()
    print(options)
