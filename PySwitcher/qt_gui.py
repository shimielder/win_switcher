import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,
                             QSystemTrayIcon, QGridLayout, QMenu, QLabel,
                             QLineEdit, QCheckBox, QComboBox, QFrame,
                             QPlainTextEdit)
from keys_registrator import start_app, stop_app, options, messages
from initialization import save_to, HOME
import logging

VERSION = '0.8'
LOGGING_LEVELS = ['DEBUG', "INFO",
                  "WARNING", "ERROR", "CRITICAL"]


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.running = False
        self.setWindowTitle('PySwicher v{}'.format(VERSION))

        # Logging config
        self.log_textbox = QPlainTextEditLogger(self)
        logging.getLogger().addHandler(self.log_textbox)
        self.log_textbox.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s]:    %(message)s'))
        self.log_textbox.setLevel(self.get_numeric_loglevel(options['log_level']))
        self.log_to_file = False

        # System tray configuration
        self.tray_menu = QMenu(self)
        self.systemTrayIcon = QSystemTrayIcon()
        self.systemTrayIcon.setVisible(False)
        self.systemTrayIcon.setIcon(QtGui.QIcon('C:\\Users\\Admin\\Pictures\\tray_stop.jpg'))
        self.systemTrayIcon.activated.connect(self.sys_tray)
        self.exit_action = self.tray_menu.addAction('Exit')
        self.exit_action.triggered.connect(self.exit_app)
        self.systemTrayIcon.setContextMenu(self.tray_menu)
        self.click_tray_timer = QtCore.QTimer(self)  # Fix for systemtray click trigger
        self.click_tray_timer.setSingleShot(True)
        self.click_tray_timer.timeout.connect(self.click_timeout)

        self.main_window_ui()
        self.starter()

    def set_log_to_file(self, state):
        logger = logging.getLogger(__name__)
        file = logging.FileHandler(HOME + '\\switcher.log')
        if state == QtCore.Qt.Checked:
            self.log_to_file = True
            file.setFormatter(
                logging.Formatter('%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'))
            file.setLevel(self.get_numeric_loglevel(options['log_level']))
            logger.addHandler(file)
        else:
            if 'file' in logger.handlers:
                logger.removeHandler(file)
            self.log_to_file = False

    def starter(self):
        if not self.running:
            self.running = True
            self.start_btn.setText('Stop switcher')
            self.systemTrayIcon.setIcon(QtGui.QIcon('C:\\Users\\Admin\\Pictures\\tray_stop.jpg'))
            start_app()
        elif self.running:
            self.running = False
            self.start_btn.setText('Start switcher')
            self.systemTrayIcon.setIcon(QtGui.QIcon('C:\\Users\\Admin\\Pictures\\tray_start.jpg'))
            stop_app()
        return

    def main_window_ui(self):
        grid = QGridLayout(self)
        self.setLayout(grid)
        grid.setSpacing(5)

        # Here goes options layout
        self.topleft = QFrame(self)
        self.topleft.setFrameShape(QFrame.StyledPanel)
        self.topleft_grid = QGridLayout(self)
        self.topleft.setLayout(self.topleft_grid)

        self.switch_comb_label = QLabel('Switch combination:')
        self.switch_comb_text = QLineEdit()
        self.switch_comb_text.setText(options['switch_combination'])

        self.hotkey_label = QLabel('Hotkey:')
        self.hotkey_comb_text = QLineEdit()
        self.hotkey_comb_text.setText(options['hotkey'])

        self.topleft_grid.addWidget(self.switch_comb_label, 0, 0)
        self.topleft_grid.addWidget(self.switch_comb_text, 1, 0)
        self.topleft_grid.addWidget(self.hotkey_label, 2, 0)
        self.topleft_grid.addWidget(self.hotkey_comb_text, 3, 0)

        grid.addWidget(self.topleft, 0, 0)

        self.topright = QFrame(self)
        self.topright.setFrameShape(QFrame.StyledPanel)
        self.topright_grid = QGridLayout(self)
        self.topright.setLayout(self.topright_grid)

        self.info_label = QLabel('===INFO===')
        self.info_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.info_author = QLabel('Author: Kurashov Sergey')
        self.info_author.setAlignment(QtCore.Qt.AlignHCenter)

        self.info_contacts = QLabel('Contacts: shimielder@gmail.com')
        self.info_contacts.setAlignment(QtCore.Qt.AlignHCenter)

        self.info_sourcecode = QLabel('<a href="https://github.com/shimielder/win_switcher">Sourcecode on GitHub</a>')
        self.info_sourcecode.setAlignment(QtCore.Qt.AlignHCenter)
        self.info_sourcecode.setOpenExternalLinks(True)

        self.topright_grid.addWidget(self.info_label, 0, 0)
        self.topright_grid.addWidget(self.info_author, 1, 0)
        self.topright_grid.addWidget(self.info_contacts, 2, 0)
        self.topright_grid.addWidget(self.info_sourcecode, 3, 0)

        grid.addWidget(self.topright, 0, 1)

        self.middle = QFrame(self)
        self.middle.setFrameShape(QFrame.StyledPanel)
        self.middle_grid = QGridLayout(self)
        self.middle.setLayout(self.middle_grid)

        self.dictionsries_label = QLabel('Dictionaries to switch:')
        self.dict_one = QPlainTextEdit()
        self.dict_one.clear()
        self.dict_one.appendPlainText(options['layouts'][0])
        self.dict_two = QPlainTextEdit()
        self.dict_two.clear()
        self.dict_two.appendPlainText(options['layouts'][1])

        self.middle_grid.addWidget(self.dictionsries_label, 0, 0, 1, 4)
        self.middle_grid.addWidget(self.dict_one, 1, 0, 1, 4)
        self.middle_grid.addWidget(self.dict_two, 2, 0, 1, 4)
        grid.addWidget(self.middle, 1, 0, 1, 2)

        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom_grid = QGridLayout(self)
        self.bottom.setLayout(self.bottom_grid)

        self.loglevel_label = QLabel('Logging level:')
        self.loglevel_dropmenu = QComboBox(self)
        self.loglevel_dropmenu.addItems(LOGGING_LEVELS)
        self.loglevel_dropmenu.setCurrentIndex(LOGGING_LEVELS.index((options['log_level'].upper())))
        self.loglevel_dropmenu.activated[str].connect(self.set_logginglevel)

        # self.log_to_file_label = QLabel('Check to save logs to file')
        self.log_to_file_chk = QCheckBox('Check to save logs to file')
        self.log_to_file_chk.stateChanged.connect(self.set_log_to_file)

        self.logging_output_label = QLabel('Logging output:')
        self.logging_output_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.bottom_grid.addWidget(self.loglevel_label, 0, 0)
        self.bottom_grid.addWidget(self.loglevel_dropmenu, 0, 1)
        self.bottom_grid.addWidget(self.log_to_file_chk, 0, 3, 1, 1)
        self.bottom_grid.addWidget(self.logging_output_label, 1, 0, 1, 4)
        self.bottom_grid.addWidget(self.log_textbox.widget, 2, 0, 2, 4)
        grid.addWidget(self.bottom, 2, 0, 1, 2)

        self.bottom_buttons = QFrame(self)
        # self.bottom_buttons.setFrameShape(QFrame.StyledPanel)
        self.bottom_buttons_grid = QGridLayout(self)
        self.bottom_buttons.setLayout(self.bottom_buttons_grid)

        self.start_btn = QPushButton('Start switcher')
        self.start_btn.clicked.connect(self.starter)
        self.apply_btn = QPushButton('Apply changes')
        self.apply_btn.clicked.connect(self.apply)
        self.exit_btn = QPushButton('Exit app')
        self.exit_btn.clicked.connect(self.exit_app)

        self.bottom_buttons_grid.addWidget(self.start_btn, 0, 0)
        self.bottom_buttons_grid.addWidget(self.apply_btn, 0, 1)
        self.bottom_buttons_grid.addWidget(self.exit_btn, 0, 2)
        grid.addWidget(self.bottom_buttons, 3, 0, 1, 2)

        self.resize(480, 320)
        self.show()

    def get_numeric_loglevel(self, loglevel):
        numeric_level = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            numeric_level = 0
        return numeric_level

    def set_logginglevel(self, loglevel):
        return self.log_textbox.setLevel(self.get_numeric_loglevel(loglevel))

    @QtCore.pyqtSlot(QSystemTrayIcon.ActivationReason)
    def sys_tray(self, reason):
        """
        По-умолчанию, trigger срабатывает всегда. Для обхода этого
        я повесил таймер на событие.
        Взято отсюда:
        https://riverbankcomputing.com/pipermail/pyqt/2010-November/028394.html
        """
        if reason == QSystemTrayIcon.Trigger:
            self.click_tray_timer.start(QApplication.doubleClickInterval())
        elif reason == QSystemTrayIcon.DoubleClick:
            self.click_tray_timer.stop()
            if self.isHidden():
                self.showNormal()
                self.systemTrayIcon.setVisible(False)

    def click_timeout(self):
        self.starter()

    def apply(self):
        self.starter()
        options['layouts'] = []
        options['layouts'].append(self.dict_one.toPlainText())
        options['layouts'].append(self.dict_two.toPlainText())
        options['log_level'] = LOGGING_LEVELS[self.loglevel_dropmenu.currentIndex()]
        self.set_logginglevel(options['log_level'])
        options['switch_combination'] = self.switch_comb_text.text()
        options['hotkey'] = self.hotkey_comb_text.text()
        logging.debug('Options from GUI: {}'.format(options))
        save_to(options)
        self.starter()
        return options

    def exit_app(self):
        if self.running:
            self.starter()
        self.systemTrayIcon.setVisible(False)
        self.destroy()

    def closeEvent(self, event):
        self.exit_app()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                self.hide()
                self.systemTrayIcon.setVisible(True)
                self.systemTrayIcon.showMessage('', 'Running in the background.')
        super(MainWindow, self).changeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
