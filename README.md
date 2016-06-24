# Win_Switcher

This app help you to switch words typed on wrong keyboard layout. Works only on Windows Vista and higher (maybe XP, not tested yet)
To make it work you need to create subdirectory 'langs' and place there language dictionaries.
Example:

file en.txt contains string:
`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?

file ru.txt:
ё1234567890-=йцукенгшщзхъфывапролджэячсмитьбю.Ё!"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,

For other layout you can get this string by just pressing every symbol key on your keyboard starting from upper left side.
You can add as much layouts as you want, but switcher works between 2 languages which specifies in options.txt.
Later I will add possibility to change dictionaries and used languages through GUI.

App launches via switcher_gui.py and at first launch generates default options.txt and subdirectory 'langs' if it doesn't exist.

How it works:
Start switcher_gui.py
Type something somewhere on wrong keyboard layout.
Select typed string and press hotkey. By default it is 'Pause'.
Switcher will cut string, convert it to right layout and paste it back.

If you want to make an exe file, use PyInstaller (install it via pip).
For example:
In cmd run "pyinstaller --onefile --clean --windowed switcher_gui.py". For more information read PyInstaller's documentation.
Or just e-mail me and I will make an exe file for you.
