import logging
import keyboard
from time import sleep

from switcher import copy, paste, options, messages, clean_clipboard

logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
running = False


def main():
    comb = options['switch_combination']
    keyboard.send('ctrl+c')
    sleep(0.05)
    data = copy()
    if data == None:
        logging.error('Nothing to convert')
        return
    logging.debug('String to convert:\t{}'.format(data))
    result = paste(data)
    sleep(0.05)
    logging.debug('Converted string:\t{}'.format(result))
    if comb: keyboard.send(comb)
    keyboard.send('ctrl+v')
    sleep(0.25)
    clean_clipboard()
    return


def start_app():
    logging.debug(
        '\nVariables at start:\nEncoding: {}\nHotkey: {}\nSwitch combination: {}\n'.format(options['encoding'],
                                                                                           options['hotkey'], options[
                                                                                               'switch_combination']))
    global running
    logging.info('App is running...')
    keyboard.add_hotkey(options['hotkey'], main)
    running = True


def stop_app():
    global running
    logging.info('App stopped...')
    running = False
    keyboard.remove_hotkey(options['hotkey'])


if __name__ == "__main__":
    import sys

    start_app()


    def stop_app():
        global running
        logging.info('App stopped...')
        running = False
        keyboard.remove_hotkey(options['hotkey'])
        keyboard.remove_hotkey('esc')
        sys.exit()


    keyboard.add_hotkey('esc', stop_app)
