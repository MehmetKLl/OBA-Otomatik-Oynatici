from win32api import MessageBox
from win32con import MB_OK, MB_YESNO, MB_ICONERROR, MB_ICONINFORMATION

def show_error(text,title):
    return MessageBox(0, text, title, MB_OK | MB_ICONERROR)

def ask_error(text,title):
    return MessageBox(0, text, title, MB_YESNO | MB_ICONERROR) == 6

def ask_info(text,title):
    return MessageBox(0, text, title, MB_YESNO | MB_ICONINFORMATION) == 6


