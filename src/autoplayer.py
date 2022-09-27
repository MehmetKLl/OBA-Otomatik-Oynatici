from pyautogui import locateOnScreen, FAILSAFE, click, moveTo, scroll, locateAllOnScreen
from time import sleep


def scroll_new_video():
    x, y, w, h = locateOnScreen("img/border.png")
    moveTo(x,y)
    scroll(-100)
    while True:
        if locateOnScreen("img/open_button.png"):
            x, y, w, h = locateOnScreen("img/open_button.png")
            click(x=x,y=y,button="left")
        elif locateOnScreen("img/open_button2.png"):
            x, y, w, h = locateOnScreen("img/open_button2.png")
            click(x=x,y=y,button="left")
        elif locateOnScreen("img/open_button3.png"):
            x, y, w, h = locateOnScreen("img/open_button3.png")
            click(x=x,y=y,button="left")

        if locateOnScreen("img/new_video_icon.png"):
            x, y, w, h = locateOnScreen("img/new_video_icon.png")
            start_new_video(x,y)
            scroll_current_video()
            control_current_video()
            break
        elif locateOnScreen("img/current_icon.png"):
            x, y, w, h = locateOnScreen("img/current_icon.png")
            start_new_video(x,y)
            scroll_current_video()
            control_current_video()
            break
        else:
            x, y, w, h = locateOnScreen("img/finished_icon.png") if locateOnScreen("img/finished_icon.png") else locateOnScreen("img/non_clickable_icon.png")
            moveTo(x,y)
            scroll(-50)

def scroll_current_video():
    x, y, w, h = locateOnScreen("img/border.png")
    moveTo(x,y)
    scroll(-100)
    while True:
        if locateOnScreen("img/open_button.png"):
            x, y, w, h = locateOnScreen("img/open_button.png")
            click(x=x,y=y,button="left")
        elif locateOnScreen("img/open_button2.png"):
            x, y, w, h = locateOnScreen("img/open_button2.png")
            click(x=x,y=y,button="left")
        elif locateOnScreen("img/open_button3.png"):
            x, y, w, h = locateOnScreen("img/open_button3.png")
            click(x=x,y=y,button="left")

        if locateOnScreen("img/current_icon.png"):
            break
        elif locateOnScreen("img/finished_icon.png"):
            x, y, w, h = locateOnScreen("img/finished_icon.png")
            moveTo(x,y)
            scroll(-50)
        elif locateOnScreen("img/non_clickable_icon.png"):
            x, y, w, h = locateOnScreen("img/non_clickable_icon.png")
            moveTo(x,y)
            scroll(-50)

def start_new_video(x,y):
    click(x=x,y=y,button="left")
    sleep(5)
    x, y, w, h = locateOnScreen("img/border.png")
    click(x=x+20,y=y+20,button="left")
    if locateOnScreen("img/stopped.png"):
        click(x=x,y=y,button="left")


def control_current_video():
        x, y, l, h = locateOnScreen("img/border.png")
        certain_video = locateOnScreen("img/current_icon.png")
        while True:
            if certain_video in list(locateAllOnScreen("img/finished_icon.png")):
                scroll_new_video()
                break

start = scroll_new_video

def main():
    FAILSAFE = False
    try:
        start()
    except Exception as err:
        pass
