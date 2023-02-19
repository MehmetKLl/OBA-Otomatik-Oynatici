import ctypes

def show_error(text,title):
    return ctypes.windll.user32.MessageBox(0, text, title, MB_OK | MB_ICONERROR)

def ask_error(text,title):
    return ctypes.windll.user32.MessageBox(0, text, title, MB_YESNO | MB_ICONERROR) == 6

def ask_info(text,title):
    return ctypes.windll.user32.MessageBox(0, text, title, MB_YESNO | MB_ICONINFORMATION) == 6


