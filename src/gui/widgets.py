from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

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