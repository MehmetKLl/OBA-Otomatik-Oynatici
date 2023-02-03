from ctypes import windll, wintypes, byref, sizeof, c_bool
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QPushButton
from PyQt5.QtCore import Qt
from .styles import Styles, SYSTEM_THEME

class TextBox(QVBoxLayout):
    def __init__(self, title, text, char_per_row):
        super().__init__()
        width_limit = char_per_row*6
        self.title_box = QLabel()
        self.title_box.setObjectName("textbox_title")
        self.title_box.setText(title)
        self.title_box.setAlignment(Qt.AlignLeft)
        self.title_box.setFixedSize(self.title_box.sizeHint().width()+6,self.title_box.sizeHint().height()+6)
        self.addWidget(self.title_box)
        self.text_box = QLabel()
        self.text_box.setFixedWidth(width_limit+6*2)
        self.text_box.setObjectName("textbox_box")
        self.text_box.setWordWrap(True)
        self.text_box.setText(text)
        self.text_box.setAlignment(Qt.AlignLeft)
        self.setSpacing(5)
        self.addWidget(self.text_box)

class DialogBox(QMessageBox):
    def __init__(self, title, text, msg_icon, window_icon):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.setWindowIcon(window_icon)
        self.setIcon(msg_icon)
        self.setWindowTitle(title)
        self.setObjectName("msgbox")
        self.setStyleSheet(Styles.MessageBoxStyle)
        self.addButton(QPushButton("Tamam"), QMessageBox.YesRole)
        self.setText(text)

        if SYSTEM_THEME == "DARK":
            self.window_handle = self.winId()
            change_window_theme = windll.dwmapi.DwmSetWindowAttribute(int(self.window_handle), 20, byref(c_bool(True)), sizeof(wintypes.BOOL))
            
            if change_window_theme:
                windll.dwmapi.DwmSetWindowAttribute(int(self.window_handle), 19, byref(c_bool(True)), sizeof(wintypes.BOOL))