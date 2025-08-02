from keyboard import is_pressed
from ctypes import windll, wintypes, byref, sizeof, c_bool
from pywintypes import error as WinApiError
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QLineEdit, QCheckBox
from PyQt5.QtGui import QIcon,QRegExpValidator, QDesktopServices
from PyQt5.QtCore import Qt, QUrl, QRegExp
from utils.constants import GUI, Player, VERSION, GitHub, Registry
from utils.exceptions import BorderNotFoundException, ImageNotFoundException, VideoIconNotFoundException
from utils.registry import check_is_first_use, delete_first_use_key
from .widgets import TextBox, DialogBox
from .autoplayer import Autoplayer
from .styles import Styles, SYSTEM_THEME


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
        self.place_widgets()

    def setup(self):
        self.setGeometry(0,0,450,400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.size())
        self.setWindowTitle(GUI.TITLE)
        self.setWindowModality(Qt.WindowModal)
        self.icon = QIcon("logo.ico")
        self.setWindowIcon(self.icon)
        self.setObjectName("main")
        self.setStyleSheet(Styles.MainWindowStyle)

        window_geometry = self.frameGeometry()
        screen_center_point = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center_point)
        self.move(window_geometry.topLeft())

        if SYSTEM_THEME == "DARK":
            self.window_handle = self.winId()
            change_window_theme = windll.dwmapi.DwmSetWindowAttribute(int(self.window_handle), 20, byref(c_bool(True)), sizeof(wintypes.BOOL))

            if change_window_theme:
                windll.dwmapi.DwmSetWindowAttribute(int(self.window_handle), 19, byref(c_bool(True)), sizeof(wintypes.BOOL))

        self.shortcut = GUI.SHORTCUT
        self.dev_mode = GUI.DEV_MODE
        self.autoclose = GUI.AUTOCLOSE
        self.scroll_delay = Player.SCROLL_DELAY
        self.video_check_delay = Player.VIDEO_CHECK_DELAY
        self.page_loading_delay = Player.PAGE_LOADING_DELAY

    def place_footer(self):
        self.footer = QWidget()
        self.footer.setObjectName("footer")
        self.footer.setFixedHeight(50)
        footer_layout = QHBoxLayout()
        self.start_button = QPushButton(text="Başlat")
        self.start_button.setObjectName("main_buttons")
        self.start_button.clicked.connect(self.start_autoplayer)
        self.settings_button = QPushButton(text="Ayarlar")
        self.settings_button.setObjectName("main_buttons")
        self.settings_button.clicked.connect(self.open_settings)
        self.version_text = QLabel(text=f"v{VERSION}")
        self.version_text.setObjectName("version_text")
        self.support_me_button = QPushButton(text="Bana destek ol!")
        self.support_me_button.setObjectName("support_me_button")
        self.support_me_button.clicked.connect(self.open_support_me)

        footer_layout.addWidget(self.start_button,1,Qt.AlignLeft)
        footer_layout.addWidget(self.settings_button,1,Qt.AlignLeft)
        footer_layout.addWidget(self.support_me_button,7,Qt.AlignRight)
        footer_layout.addWidget(self.version_text,1,Qt.AlignRight)

        self.footer.setLayout(footer_layout)

    def place_widgets(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)

        self.top_layout = QVBoxLayout()
        self.top_layout.setContentsMargins(10,10,10,10)
        self.top_layout.setSpacing(20)

        self.about_textbox = TextBox("Nedir bu ÖBA Otomatik Oynatıcı?","ÖBA Otomatik Oynatıcı Python ile yazılan arayüzlü basit bir makro uygulamasıdır. Program ekran görüntüsünü işleyip doğal tıklama işlemlerini taklit ederek çalışmaktadır.",char_per_row=60)
        self.why_textbox = TextBox("Niye ÖBA Otomatik Oynatıcı?","<b>•</b> Program tamamen tıklama işlemlerini taklit ettiği için diğer alternatiflerine göre sıkıntı oluşturmaz.<br><b>•</b> Program açık kaynak kodlu olduğundan daha güvenilirdir.<br><b>•</b> Kullanımı daha kolaydır.",char_per_row=60)
        self.usage_textbox = TextBox("Kullanım","<b>•</b> Program videoların izlendiği kısımdan itibaren başlatılmalıdır. Aksi takdirde program doğru çalışmayacaktır.<br><b>•</b> Program çalışırken fare ile oynanmamalı ve program durdurulmak isteniyorsa sadece kısayol tuşu veya \"Durdur\" tuşuna basılarak kapatılmalıdır, aksi takdirde program çökebilir.",char_per_row=60)
        self.top_layout.addLayout(self.about_textbox)
        self.top_layout.addLayout(self.why_textbox)
        self.top_layout.addLayout(self.usage_textbox)

        self.main_layout.addLayout(self.top_layout,0)

        self.place_footer()
        self.main_layout.addWidget(self.footer,0,Qt.AlignBottom)
        self.setLayout(self.main_layout)

    def open_support_me(self):
        QDesktopServices.openUrl(QUrl(GitHub.SUPPORT_ME_URL))
        self.showMinimized()

    def open_settings(self):
        self.settings_window = SettingsWindow(parent=self)
        self.settings_window.show()

    def check_is_shortcut_valid(self):
        try:
            is_pressed(self.shortcut)
        except:
            return False

        return True

    def start_autoplayer(self):
        if not self.check_is_shortcut_valid():
            invalid_shortcut_msgbox = DialogBox(GUI.TITLE, "Kısayol tuşu geçersiz.", QMessageBox.Critical, self.icon)
            invalid_shortcut_msgbox.exec_()
            return
        
        if check_is_first_use():
            firstuse_msgbox = DialogBox(GUI.TITLE, GUI.TUTORIAL_TEXT, QMessageBox.Warning, self.icon)
            firstuse_msgbox.exec_()
            delete_first_use_key()

        self.autoplayer_thread = Autoplayer(parent=self)
        self.autoplayer_thread.started.connect(self.autoplayer_startedEvent)
        self.autoplayer_thread.finished.connect(self.autoplayer_finishedEvent)
        self.autoplayer_thread.exception_signal.connect(self.autoplayer_exceptionEvent)
        self.autoplayer_thread.stopped_signal.connect(self.autoplayer_stoppedEvent)
        self.autoplayer_thread.start()

    def autoplayer_startedEvent(self):
        self.start_button.setEnabled(False)
        windll.kernel32.SetThreadExecutionState(0x80000002)

        if self.autoclose:
            self.setWindowOpacity(0)

        self.setWindowTitle(f"{GUI.TITLE} - Çalışıyor...")

    def autoplayer_finishedEvent(self):
        if self.autoclose:
            self.setWindowOpacity(1)

        self.start_button.setEnabled(True)
        windll.kernel32.SetThreadExecutionState(0x80000000)

        self.setWindowTitle(GUI.TITLE)

    def autoplayer_stoppedEvent(self):
        DialogBox(GUI.TITLE, "Program sonlandırıldı.", QMessageBox.Information, self.icon).exec_()

        self.autoplayer_finishedEvent()

    def autoplayer_exceptionEvent(self, exception):
        if self.dev_mode:
            error_string = f"Hata yakalandı:\n\n{exception[1]}"

        elif isinstance(exception[0], BorderNotFoundException):
            error_string = "Oynatılacak videonun kenarlıkları bulunamadı. Programı belirtildiği kısımda çalıştırdığınızdan emin olun."

        elif isinstance(exception[0], WinApiError):
            error_string = "Programda farenin zorlanması sonucunda hata oluştu ve program sonlandırıldı."

        elif isinstance(exception[0], ImageNotFoundException):
            error_string = f"Ekranda \"{exception[0].image}\" görüntüsü bulunamadı."

        elif isinstance(exception[0], VideoIconNotFoundException):
            error_string = "Ekranda \"oynatılan video\" simgesi bulunamadı ve programda hata oluştu."

        else:
            error_string = "Hata oluştu ve program sonlandırıldı. Detaylı hata bilgisi almak için geliştirici modunu açıp tekrar deneyebilirsiniz."

        exception_dialogbox = DialogBox(GUI.TITLE, error_string, QMessageBox.Critical, self.icon)
        exception_dialogbox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        exception_dialogbox.exec_()

        self.autoplayer_finishedEvent()



class SettingsWindow(QWidget):    
    def __init__(self, *args, **kwargs):
       super().__init__(*args,**kwargs)
       self.setup()
       self.place_widgets()

    def setup(self):
        self.setGeometry(0,0,275,410)
        self.setWindowFlags(Qt.Sheet | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle(GUI.TITLE)
        self.setWindowIcon(self.parent().icon)
        self.setFixedSize(self.size())
        self.setObjectName("settings")
        self.setStyleSheet(Styles.SettingsWindowStyle)

        window_geometry = self.frameGeometry()
        screen_center_point = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(screen_center_point)
        self.move(window_geometry.topLeft())

        if SYSTEM_THEME == "DARK":
            self.window_handle = self.winId()
            change_window_theme = windll.dwmapi.DwmSetWindowAttribute(int(self.window_handle), 20, byref(c_bool(True)), sizeof(wintypes.BOOL))

            if change_window_theme:
                windll.dwmapi.DwmSetWindowAttribute(int(self.window_handle), 19, byref(c_bool(True)), sizeof(wintypes.BOOL))


    def closeEvent(self,event):
        return super().closeEvent(event)

    def autoclose_checkbox_clickEvent(self):
        self.parent().autoclose = self.autoclose_checkbox.isChecked()
        self.autoclose_checkbox.setText("Açık" if self.parent().autoclose else "Kapalı")

    def dev_mode_checkbox_clickEvent(self):
        self.parent().dev_mode = self.dev_mode_checkbox.isChecked()
        self.dev_mode_checkbox.setText("Açık" if self.parent().dev_mode else "Kapalı")

    def shortcut_entry_textChangedEvent(self):
        self.parent().shortcut = self.shortcut_entry.text()

    def scroll_delay_entry_textChangedEvent(self):
        if not self.scroll_delay_entry.text():
            return

        self.parent().scroll_delay = int(self.scroll_delay_entry.text())

    def video_check_delay_entry_textChangedEvent(self):
        if not self.video_check_delay_entry.text():
            return

        self.parent().video_check_delay = int(self.video_check_delay_entry.text())

    def page_loading_delay_entry_textChangedEvent(self):
        if not self.page_loading_delay_entry.text():
            return

        self.parent().page_loading_delay = int(self.page_loading_delay_entry.text())

    def place_widgets(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        self.shortcut_widget = QWidget()
        self.shortcut_widget.setObjectName("option_box")
        self.shortcut_layout = QVBoxLayout()
        self.shortcut_text = QLabel("Programı kapatma kısayolu:")
        self.shortcut_entry = QLineEdit()
        self.shortcut_entry.setText(self.parent().shortcut)
        self.shortcut_entry.textChanged.connect(self.shortcut_entry_textChangedEvent)
        self.shortcut_entry.setFixedSize(self.shortcut_entry.sizeHint().width()+6,self.shortcut_entry.sizeHint().height())
        self.shortcut_layout.addWidget(self.shortcut_text)
        self.shortcut_layout.addWidget(self.shortcut_entry)
        self.shortcut_widget.setLayout(self.shortcut_layout)
        self.shortcut_widget.setFixedSize(self.shortcut_widget.sizeHint().width(),self.shortcut_widget.sizeHint().height())

        self.autoclose_widget = QWidget()
        self.autoclose_widget.setObjectName("option_box")
        self.autoclose_layout = QVBoxLayout()
        self.autoclose_text = QLabel("Otomatik kapanma ayarı:")
        self.autoclose_checkbox = QCheckBox("Açık" if self.parent().autoclose else "Kapalı")
        self.autoclose_checkbox.setChecked(self.parent().autoclose)
        self.autoclose_checkbox.stateChanged.connect(self.autoclose_checkbox_clickEvent)
        self.autoclose_layout.addWidget(self.autoclose_text)
        self.autoclose_layout.addWidget(self.autoclose_checkbox)
        self.autoclose_widget.setLayout(self.autoclose_layout)
        self.autoclose_widget.setFixedSize(self.autoclose_widget.sizeHint().width(),self.autoclose_widget.sizeHint().height())

        self.dev_mode_widget = QWidget()
        self.dev_mode_widget.setObjectName("option_box")
        self.dev_mode_layout = QVBoxLayout()
        self.dev_mode_text = QLabel("Geliştirici modu:")
        self.dev_mode_checkbox = QCheckBox("Açık" if self.parent().dev_mode else "Kapalı")
        self.dev_mode_checkbox.setChecked(self.parent().dev_mode)
        self.dev_mode_checkbox.stateChanged.connect(self.dev_mode_checkbox_clickEvent)
        self.dev_mode_layout.addWidget(self.dev_mode_text)
        self.dev_mode_layout.addWidget(self.dev_mode_checkbox)
        self.dev_mode_widget.setLayout(self.dev_mode_layout)
        self.dev_mode_widget.setFixedSize(self.dev_mode_widget.sizeHint().width(),self.dev_mode_widget.sizeHint().height())

        self.scroll_delay_widget = QWidget()
        self.scroll_delay_widget.setObjectName("option_box")
        self.scroll_delay_entry_validator = QRegExpValidator(QRegExp("[0-9]{1,2}"))
        self.scroll_delay_widget_layout = QVBoxLayout()
        self.scroll_delay_text = QLabel("Video kaydırma gecikmesi:")
        self.scroll_delay_entry_layout = QHBoxLayout()
        self.scroll_delay_entry = QLineEdit()
        self.scroll_delay_entry.setAlignment(Qt.AlignCenter)
        self.scroll_delay_entry.setValidator(self.scroll_delay_entry_validator)
        self.scroll_delay_entry.setText(str(self.parent().scroll_delay))
        self.scroll_delay_entry.textChanged.connect(self.scroll_delay_entry_textChangedEvent)
        self.scroll_delay_entry.setFixedWidth(20)
        self.scroll_delay_entry_type = QLabel("saniye")
        self.scroll_delay_entry_type.setAlignment(Qt.AlignCenter)
        self.scroll_delay_entry_layout.addWidget(self.scroll_delay_entry,0, Qt.AlignLeft)
        self.scroll_delay_entry_layout.addWidget(self.scroll_delay_entry_type,1, Qt.AlignLeft)
        self.scroll_delay_widget_layout.addWidget(self.scroll_delay_text)
        self.scroll_delay_widget_layout.addLayout(self.scroll_delay_entry_layout)
        self.scroll_delay_widget.setLayout(self.scroll_delay_widget_layout)
        self.scroll_delay_widget.setFixedSize(self.scroll_delay_widget.sizeHint().width(),self.scroll_delay_widget.sizeHint().height())

        self.video_check_delay_widget = QWidget()
        self.video_check_delay_widget.setObjectName("option_box")
        self.video_check_delay_entry_validator = QRegExpValidator(QRegExp("[0-9]{1,2}"))
        self.video_check_delay_widget_layout = QVBoxLayout()
        self.video_check_delay_text = QLabel("Video kontrol gecikmesi:")
        self.video_check_delay_entry_layout = QHBoxLayout()
        self.video_check_delay_entry = QLineEdit()
        self.video_check_delay_entry.setAlignment(Qt.AlignCenter)
        self.video_check_delay_entry.setValidator(self.video_check_delay_entry_validator)
        self.video_check_delay_entry.setText(str(self.parent().video_check_delay))
        self.video_check_delay_entry.textChanged.connect(self.video_check_delay_entry_textChangedEvent)
        self.video_check_delay_entry.setFixedWidth(20)
        self.video_check_delay_entry_type = QLabel("saniye")
        self.video_check_delay_entry_type.setAlignment(Qt.AlignCenter)
        self.video_check_delay_entry_layout.addWidget(self.video_check_delay_entry,0, Qt.AlignLeft)
        self.video_check_delay_entry_layout.addWidget(self.video_check_delay_entry_type,1, Qt.AlignLeft)
        self.video_check_delay_widget_layout.addWidget(self.video_check_delay_text)
        self.video_check_delay_widget_layout.addLayout(self.video_check_delay_entry_layout)
        self.video_check_delay_widget.setLayout(self.video_check_delay_widget_layout)
        self.video_check_delay_widget.setFixedSize(self.video_check_delay_widget.sizeHint().width(),self.video_check_delay_widget.sizeHint().height())

        self.page_loading_delay_widget = QWidget()
        self.page_loading_delay_widget.setObjectName("option_box")
        self.page_loading_delay_entry_validator = QRegExpValidator(QRegExp("[0-9]{1,2}"))
        self.page_loading_delay_widget_layout = QVBoxLayout()
        self.page_loading_delay_text = QLabel("Sayfa yüklenme bekleme süresi:")
        self.page_loading_delay_entry_layout = QHBoxLayout()
        self.page_loading_delay_entry = QLineEdit()
        self.page_loading_delay_entry.setAlignment(Qt.AlignCenter)
        self.page_loading_delay_entry.setValidator(self.page_loading_delay_entry_validator)
        self.page_loading_delay_entry.setText(str(self.parent().page_loading_delay))
        self.page_loading_delay_entry.textChanged.connect(self.page_loading_delay_entry_textChangedEvent)
        self.page_loading_delay_entry.setFixedWidth(20)
        self.page_loading_delay_entry_type = QLabel("saniye")
        self.page_loading_delay_entry_type.setAlignment(Qt.AlignCenter)
        self.page_loading_delay_entry_layout.addWidget(self.page_loading_delay_entry,0, Qt.AlignLeft)
        self.page_loading_delay_entry_layout.addWidget(self.page_loading_delay_entry_type,1, Qt.AlignLeft)
        self.page_loading_delay_widget_layout.addWidget(self.page_loading_delay_text)
        self.page_loading_delay_widget_layout.addLayout(self.page_loading_delay_entry_layout)
        self.page_loading_delay_widget.setLayout(self.page_loading_delay_widget_layout)
        self.page_loading_delay_widget.setFixedSize(self.page_loading_delay_widget.sizeHint().width(),self.page_loading_delay_widget.sizeHint().height())

        self.main_layout.addWidget(self.shortcut_widget)
        self.main_layout.addWidget(self.autoclose_widget)
        self.main_layout.addWidget(self.dev_mode_widget)
        self.main_layout.addWidget(self.scroll_delay_widget)
        self.main_layout.addWidget(self.video_check_delay_widget)
        self.main_layout.addWidget(self.page_loading_delay_widget)
        self.setLayout(self.main_layout)
