from win32api import MessageBox
from win32con import IDYES, MB_OK, MB_YESNO, MB_ICONERROR, MB_ICONINFORMATION, MB_TOPMOST

def show_error(text,title):
    return MessageBox(0, text, title, MB_OK | MB_ICONERROR | MB_TOPMOST)

def ask_error(text,title):
    return MessageBox(0, text, title, MB_YESNO | MB_ICONERROR | MB_TOPMOST) == IDYES

def ask_info(text,title):
    return MessageBox(0, text, title, MB_YESNO | MB_ICONINFORMATION | MB_TOPMOST) == IDYES

def ask_no_icon(text, title):
    return MessageBox(0, text, title, MB_YESNO | MB_TOPMOST) == IDYES

