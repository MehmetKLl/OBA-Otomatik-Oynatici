<<<<<<< HEAD
import ctypes

def show_error(text,title):
    return ctypes.windll.user32.MessageBox(0, text, title, MB_OK | MB_ICONERROR)

def ask_error(text,title):
    return ctypes.windll.user32.MessageBox(0, text, title, MB_YESNO | MB_ICONERROR) == 6

def ask_info(text,title):
    return ctypes.windll.user32.MessageBox(0, text, title, MB_YESNO | MB_ICONINFORMATION) == 6
=======
from win32api import MessageBox
from win32con import IDYES, MB_OK, MB_YESNO, MB_ICONERROR, MB_ICONINFORMATION, MB_TOPMOST

def show_error(text,title):
    return MessageBox(0, text, title, MB_OK | MB_ICONERROR | MB_TOPMOST)

def ask_error(text,title):
    return MessageBox(0, text, title, MB_YESNO | MB_ICONERROR | MB_TOPMOST) == IDYES

def ask_info(text,title):
    return MessageBox(0, text, title, MB_YESNO | MB_ICONINFORMATION | MB_TOPMOST) == IDYES
>>>>>>> 04441ed9df47c89f9216eaac69aa64fd7ea19b40

def ask_no_icon(text, title):
    return MessageBox(0, text, title, MB_YESNO | MB_TOPMOST) == IDYES

