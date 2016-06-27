from tkinter import *
import logging
from keys_registrator import start_app, stop_app, options, messages
from initialization import save_to

running = False

root = Tk()
root.title('PySwitcher Alpha')

"""Textbox for logging output"""
txt = Frame(root)
textbox = Text(txt, font='Arial 10', wrap='word')
scrollbar = Scrollbar(txt)
scrollbar['command'] = textbox.yview
textbox['yscrollcommand'] = scrollbar.set


class TextHandler(
    logging.Handler):  # Slightly modified class from: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        self.formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        self.setFormatter(self.formatter)
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert('end', msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview('end')

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


# Create textLogger
text_handler = TextHandler(textbox)
# Add the handler to logger
logger = logging.getLogger()
logger.addHandler(text_handler)


def debugpanelshow():
    txt.pack(side='bottom')
    textbox.pack(side='left')
    scrollbar.pack(side='right', fill='y')
    var_label.grid(row=7, column=0, sticky=W)
    var_entry.grid(row=8, column=0, sticky=W)
    btn_var.grid(row=3, column=1, sticky=E)


def debugpanelhide():
    txt.pack_forget()
    var_label.grid_forget()
    var_entry.grid_forget()
    btn_var.grid_forget()


def inspectvar():
    vars_to_inspect = var_entry.get().replace(' ', '').split(',')
    for var in vars_to_inspect:
        try:
            mvar = globals()[var]
        except KeyError:
            logging.error('No such variable', exc_info=True)
        else:
            logging.debug('{} = {}'.format(var, mvar))


def starter():
    global running
    if not running:
        running = True
        btn_start.config(text='Stop Switcher')
        start_app()
    elif running:
        running = False
        btn_start.config(text='Start Switcher')
        stop_app()


def exit_app():
    if running:
        starter()
    root.destroy()


def reload_opt():
    if running:
        starter()
    options['encoding'] = enc_entry.get()
    options['switch_combination'] = comb_entry.get()
    options['hotkey'] = hotkey_entry.get()
    save_to(options)
    if debug.get():
        debugpanelshow()
    elif not debug.get():
        debugpanelhide()

label_size = entry_size = 40

main_frame = Frame(root, bd=2)
main_frame.pack()
left_frame = Frame(main_frame, bd=2)
left_frame.grid(row=0, column=0, rowspan=6)

enc_label = Label(left_frame,
                    text='System encoding (ex. cp1251)',
                    width=label_size,
                    anchor=W)
enc_entry = Entry(left_frame, width=entry_size)
enc_label.grid(row=0, column=0, sticky=W)
enc_entry.grid(row=1, column=0, sticky=W)
enc_entry.insert(0, options['encoding'])

comb_label = Label(left_frame,
                   text='Switch combination (ex. ctrl+shift)',
                   width=label_size,
                   anchor=W)
comb_entry = Entry(left_frame, width=entry_size)
comb_label.grid(row=2, column=0, sticky=W)
comb_entry.grid(row=3, column=0, sticky=W)
comb_entry.insert(0, options['switch_combination'] if options['switch_combination'] else 'empty')

hotkey_label = Label(left_frame,
                     text='Hotkey combination (default pause)',
                     width=label_size,
                     anchor=W)
hotkey_entry = Entry(left_frame, width=entry_size)
hotkey_label.grid(row=4, column=0, sticky=W)
hotkey_entry.grid(row=5, column=0, sticky=W)
hotkey_entry.insert(0, options['hotkey'])

var_label = Label(left_frame,
                  text='Variable to inspect',
                  width=label_size,
                  anchor=W)
var_entry = Entry(left_frame, width=entry_size)

btn_start = Button(main_frame,
                   width=12, height=2,
                   text='Start app',
                   bg="white", fg="black",
                   command=starter)
btn_start.grid(row=1, column=1, sticky=E, padx=2, pady=2)

btn_stop = Button(main_frame,
                  width=12, height=2,
                  text='Exit',
                  bg="white", fg="black",
                  command=exit_app)
btn_stop.grid(row=2, column=1, sticky=E, padx=2, pady=2)

btn_rld_opt = Button(main_frame,
                     width=12, height=2,
                     text='Reload options',
                     bg="white", fg="black",
                     command=reload_opt)
btn_rld_opt.grid(row=0, column=1, sticky=E, padx=2, pady=2)

btn_var = Button(main_frame,
                 width=12, height=2,
                 text='View variable',
                 bg="white", fg="black",
                 command=inspectvar)

debug = IntVar()
check_debug = Checkbutton(left_frame,
                          text="Enable debug panel",
                          variable=debug)
check_debug.grid(row=6, column=0, sticky=W)

for message in messages:  # сообщения, которые необходимо вывести после загрузки gui
    logging.info(message)

starter()
root.mainloop()
