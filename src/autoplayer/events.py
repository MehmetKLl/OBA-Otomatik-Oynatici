from win32api import SetCursorPos, GetCursorPos, mouse_event
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP, MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, MOUSEEVENTF_WHEEL
from numpy import arange
from time import sleep

def left_click(new_x_pos=None, new_y_pos=None):
    x_pos, y_pos = GetCursorPos() if not new_x_pos and not new_y_pos else (new_x_pos, new_y_pos)
    SetCursorPos((x_pos, y_pos))
    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0)
    sleep(0.1)
    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0)

def right_click(new_x_pos=None, new_y_pos=None):
    x_pos, y_pos = GetCursorPos() if not new_x_pos and not new_y_pos else (new_x_pos, new_y_pos)
    SetCursorPos((x_pos, y_pos))
    mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0)
    sleep(0.1)
    mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0)

def scroll(scroll_count=0, new_x_pos=None, new_y_pos=None):
    x_pos, y_pos = GetCursorPos() if not new_x_pos and not new_y_pos else (new_x_pos, new_y_pos)
    SetCursorPos((x_pos, y_pos))
    mouse_event(MOUSEEVENTF_WHEEL, x_pos, y_pos, scroll_count, 0)
