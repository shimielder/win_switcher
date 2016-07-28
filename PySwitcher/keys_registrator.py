import logging
import keyboard
from time import sleep
from initialization import layout_switch, set_loglevel
from switcher import copy, paste, options, messages, clean_clipboard

logger = logging.getLogger()
set_loglevel(options['log_level'])
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
    if comb: layout_switch(comb)
    sleep(0.25)
    keyboard.send('ctrl+v')
    sleep(0.05)
    clean_clipboard()
    return


def start_app():
    logging.debug(
        '\nVariables at start:\nEncoding: {}\nHotkey: {}\nSwitch combination: {}\nLogging level: {}'.format(
            options['encoding'],
            options['hotkey'],
            options['switch_combination'],
            options['log_level']))
    global running
    logging.info('App is running...')
    keyboard.add_hotkey(options['hotkey'], main)
    logging.debug('Existing hotkeys: {}'.format(keyboard.hotkeys))
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
