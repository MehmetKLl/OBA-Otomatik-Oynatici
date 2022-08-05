from __future__ import print_function
from traceback import format_exc
from pyautogui import locateOnScreen, FAILSAFE, click, moveTo, scroll, locateAllOnScreen
from time import sleep
from multiprocessing import Process, Pipe
from keyboard import wait
from os import system
from sys import exit

class Process(Process):
    def __init__(self, *args, **kwargs):
        Process.__init__(self, *args, **kwargs)
        self._pconn, self._cconn = Pipe()
        self._exception = None

    def run(self):
        try:
            Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = format_exc()
            self._cconn.send((e, tb))
    

    @property
    def exception(self):
        if self._pconn.poll():
            self._exception = self._pconn.recv()
        return self._exception 

def capture_image(img):
    return locateOnScreen(img)

def scroll_new_video():
    x, y, w, h = capture_image("img/border.png")
    moveTo(x,y)
    scroll(-100)
    while True:
        if capture_image("img/open_button.png") or capture_image("img/open_button2.png"):
            x, y, w, h = capture_image("img/open_button.png") if capture_image("img/open_button.png") else capture_image("img/open_button2.png")
            click(x=x,y=y,button="left")
        if capture_image("img/new_video_icon.png") or capture_image("img/current_icon.png"):
            x, y, w, h = capture_image("img/new_video_icon.png") if capture_image("img/new_video_icon.png") else capture_image("img/current_icon.png")
            start_new_video(x,y)
            scroll_current_video()
            control_current_video()
            break
        else:
            x, y, w, h = capture_image("img/finished_icon.png") if capture_image("img/finished_icon.png") else capture_image("img/non_clickable_icon.png")
            moveTo(x,y)
            scroll(-50)

def scroll_current_video():
    x, y, w, h = capture_image("img/border.png")
    moveTo(x,y)
    scroll(-100)
    while True:
        if capture_image("img/open_button.png") or capture_image("img/open_button2.png"):
            x, y, w, h = capture_image("img/open_button.png") if capture_image("img/open_button.png") else capture_image("img/open_button2.png")
            click(x=x,y=y,button="left")
        if capture_image("img/current_icon.png"):
            break
        else:
            x, y, w, h = capture_image("img/finished_icon.png") if capture_image("img/finished_icon.png") else capture_image("img/non_clickable_icon.png")
            moveTo(x,y)
            scroll(-50)
            
def start_new_video(x,y):
    click(x=x,y=y,button="left")
    sleep(5)
    x, y, w, h = capture_image("img/border.png")
    click(x=x+200,y=y+200,button="left")
    if capture_image("img/stopped.png"):
        click(x=x,y=y,button="left")


def control_current_video():
        x, y, l, h = capture_image("img/border.png")
        certain_video = capture_image("img/current_icon.png")
        while True:
            if certain_video in list(locateAllOnScreen("img/finished_icon.png")):
                scroll_new_video()
                break

start = scroll_new_video

def main():
    try:
        start()
    except Exception as err:
        print(f"[!] Hata yakalandı: {err}")
        raise
        
