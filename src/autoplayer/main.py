from time import sleep
from autoplayer.handler import Screen
from autoplayer.events import left_click
from utils.constants import Player
from utils.exceptions import BorderNotFoundException

SCROLL_DELAY = Player.SCROLL_DELAY
VIDEO_CHECK_DELAY = Player.VIDEO_CHECK_DELAY
SCROLL_VALUE = Player.SCROLL_VALUE

def scroll_new_video():
    for _ in range(5):
        border = Screen().capture("img/border.png",exceptions="silent")
        if border:
            break
    else:
        raise BorderNotFoundException()
    
    border.click("left")
    border.click("scroll",SCROLL_DELAY)

    while True:
        videos_icons_screen = Screen()

        open_category_button = videos_icons_screen.capture("img/open_button.png",mode="single",threshold=0.9)
        if open_category_button:
            open_category_button.click("left")

        new_video_icon = videos_icons_screen.capture("img/new_video_icon.png")
        if new_video_icon:
            x, y, w, h = new_video_icon.get_pos()
            start_new_video((x,y))
            scroll_current_video()
            control_current_video()
            break
        
        current_video_icon = videos_icons_screen.capture("img/current_icon.png")
        if current_video_icon:
            x, y, w, h = current_video_icon.get_pos()
            start_new_video((x,y))
            scroll_current_video()
            control_current_video()
            break

        finished_icon = videos_icons_screen.capture("img/finished_icon.png")
        if finished_icon:
            finished_icon.click("scroll",SCROLL_VALUE)
            sleep(SCROLL_DELAY)
            continue
            
        non_clickable_icon = videos_icons_screen.capture("img/non_clickable_icon.png")
        if non_clickable_icon:
            non_clickable_icon.click("scroll",SCROLL_VALUE)

        sleep(SCROLL_DELAY)

            


def scroll_current_video():
    for _ in range(5):
        border = Screen().capture("img/border.png",exceptions="silent")
        if border:
            break
    else:
        raise BorderNotFoundException()

    border.click("left")
    border.click("scroll",SCROLL_DELAY)

    while True:
        videos_icons_screen = Screen()

        open_category_button = videos_icons_screen.capture("img/open_button.png",mode="single",threshold=0.9)
        if open_category_button:
            open_category_button.click("left")      

        if videos_icons_screen.capture("img/current_icon.png"):
            break

        finished_icon = videos_icons_screen.capture("img/finished_icon.png")
        if finished_icon:
            finished_icon.click("scroll",SCROLL_VALUE)
            sleep(SCROLL_DELAY)
            continue
            
        non_clickable_icon = videos_icons_screen.capture("img/non_clickable_icon.png")
        if non_clickable_icon:
            non_clickable_icon.click("scroll",SCROLL_VALUE)

        sleep(SCROLL_DELAY)
            
def start_new_video(pos):
    left_click(x=pos[0],y=pos[1])
    sleep(5)
    
    for _ in range(5):
        border = Screen().capture("img/border.png",exceptions="silent")
        if border:
            break
    else:
        raise BorderNotFoundException()
    
    left_click(x=border_pos[0]+20,y=border_pos[1]+20)
    sleep(5)
    if Screen().capture("img/stopped.png"):
        left_click(x=border_pos[0]+20,y=border_pos[1]+20)


def control_current_video():
    cur_icon = Screen().capture("img/current_icon.png")

    while True:
        if cur_icon in Screen().capture("img/finished_icon.png",mode="all"):
            scroll_new_video()
            break

        sleep(VIDEO_CHECK_DELAY)


def start():
    scroll_new_video()

