from win32api import GetKeyboardLayout
from win32gui import GetForegroundWindow
from ctypes import windll
from os import getcwd
from time import sleep
import logging

import keyboard

logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def get_options():
    options = {
        'hotkey': 'pause',
        'langs': 'ru,en',
        'log_level': 'DEBUG',
        'encoding': 'cp1251',
        'switch_combination': combination_definition()
    }
    valid_loglevels = ('NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    loaded_options = load_from()
    if 'switch_combination' in loaded_options:
        comb = options['switch_combination']
        if not comb_check(comb):
            options['switch_combination'] = combination_definition()
    for key in loaded_options:
        if loaded_options[key]:
            options[key] = loaded_options[key]
    if options['log_level'].upper() not in valid_loglevels: options['log_level'] = 'DEBUG'
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
            return generate_default()
        for item in data:
            key = item.split('=')[0]
            value = item.split('=')[1].replace('\n', '')
            if value == 'empty':
                value = None
            options[key] = value
        return options
    except FileNotFoundError:
        logging.error('Options file not found...')
        return generate_default()


def save_to(options, path=getcwd()):
    logging.info('Saving options to file...')
    opt_file = open('{}\\options.txt'.format(path), 'w')
    for opt in options:
        key = opt
        value = options[opt]
        if not value:
            value = 'empty'  # Необходимо, чтобы можно было потом записать в файл настройки
        opt_file.write(key + '=' + value + '\n')
    opt_file.close()


def comb_check(comb):
    logging.info('Checking switch combination...')
    try:
        if not comb:
            return False
        user32 = windll.user32
        cur_hwnd = GetForegroundWindow()
        cur_pid = user32.GetWindowThreadProcessId(cur_hwnd, None)  # Получаем pid процесса для текущего юзера
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


def generate_default():
    logging.info('Generating default options...')
    options = {
        'hotkey': 'pause',
        'langs': 'ru,en',
        'log_level': 'DEBUG',
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


def layout_switch(switch_combination, attempts=5):
    logging.info('Switching layout...')
    user32 = windll.user32
    cur_hwnd = GetForegroundWindow()
    cur_pid = user32.GetWindowThreadProcessId(cur_hwnd, None)  # Получаем pid процесса
    current_lang = GetKeyboardLayout(cur_pid)  # Получаем раскладку по pid
    for i in range(attempts):
        keyboard.send(switch_combination)
        sleep(0.25)
        if current_lang != GetKeyboardLayout(cur_pid):
            logging.info('Layout switching successfull...')
            return
    logging.info('Layout switching NOT switched. Check your settings.')


def set_loglevel(loglevel):
    if not loglevel:
        numeric_level = 10
        return logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                                   level=numeric_level)
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        logging.error('Improper log_level. Check settings. Log_level set to "DEBUG"')
        numeric_level = 10
    # logging.debug('Numeric log_level: {}'.format(numeric_level))
    return logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                               level=numeric_level)

if __name__ == '__main__':
    options = get_options()
    print(options)
