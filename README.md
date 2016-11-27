#### Py_Switcher

This app help you to switch words typed on wrong keyboard layout. Works only on Windows Vista and higher (maybe XP, not tested yet).

Example:


First dictionary contains string:

`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?

Second dictionary contains string:

ё1234567890-=йцукенгшщзхъфывапролджэячсмитьбю.Ё!"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,


For other layout you can get this string by just pressing every symbol key on your keyboard starting from upper left side.
Then repeat with Shift holded.


App launches via qt_gui.py and at first launch generates default options and dictionaries.


How it works:

1. Start qt_gui.py
2. Type something somewhere on wrong keyboard layout.
3. Select typed string (for example, using ctrl+A) and press hotkey. By default it is 'Pause'.
4. Switcher will cut string, convert it to right layout and paste it back. And switch layout.


If you want to make an exe file, use PyInstaller (install it via pip).

For example:

In cmd run "pyinstaller --onefile --clean --windowed switcher_gui.py". For more information read PyInstaller's documentation.

Or just e-mail me and I will make an exe file for you.
