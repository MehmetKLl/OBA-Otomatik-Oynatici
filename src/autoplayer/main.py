from time import sleep
from autoplayer.handler import Screen
from autoplayer.events import left_click, scroll
from utils.constants import Player
from utils.exceptions import BorderNotFoundException, VideoIconNotFoundException, ImageNotFoundException

SCROLL_DELAY = Player.SCROLL_DELAY
VIDEO_CHECK_DELAY = Player.VIDEO_CHECK_DELAY
SCROLL_VALUE = Player.SCROLL_VALUE

def scroll_and_start_new_video(scroll_delay=SCROLL_DELAY, video_check_delay=VIDEO_CHECK_DELAY):
    for _ in range(5):
        border = Screen().capture("img/border.png",exceptions="silent")
        if border:
            break
    else:
        raise BorderNotFoundException()
    
    border.click("left")
    border.click("scroll",SCROLL_VALUE)

    while True:
        videos_icons_screen = Screen()

        open_category_button = videos_icons_screen.capture("img/open_button.png",mode="single",threshold=0.9)
        if open_category_button:
            open_category_button.click("left")

        new_video_icon = videos_icons_screen.capture("img/new_video_icon.png")
        if new_video_icon:
            x, y, w, h = new_video_icon.get_pos()
            start_new_video((x+5,y-5))
            scroll_current_video(scroll_delay=scroll_delay)
            control_current_video(scroll_delay=scroll_delay, video_check_delay=video_check_delay)
            break
        
        current_video_icon = videos_icons_screen.capture("img/current_icon.png")
        if current_video_icon:
            x, y, w, h = current_video_icon.get_pos()
            start_new_video((x+5,y-5))
            scroll_current_video(scroll_delay=scroll_delay)
            control_current_video(scroll_delay=scroll_delay, video_check_delay=video_check_delay)
            break

        finished_icon = videos_icons_screen.capture("img/finished_icon.png")
        if finished_icon:
            finished_icon.click("scroll",SCROLL_VALUE)
            sleep(scroll_delay)
            continue
            
        non_clickable_icon = videos_icons_screen.capture("img/non_clickable_icon.png")
        if non_clickable_icon:
            non_clickable_icon.click("scroll",SCROLL_VALUE)

        sleep(scroll_delay)

            


def scroll_current_video(scroll_delay=SCROLL_DELAY):
    for _ in range(5):
        border = Screen().capture("img/border.png",exceptions="silent")
        if border:
            break
    else:
        raise BorderNotFoundException()

    border.click("left")
    border.click("scroll",SCROLL_VALUE)

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
            sleep(scroll_delay)
            continue
            
        non_clickable_icon = videos_icons_screen.capture("img/non_clickable_icon.png")
        if non_clickable_icon:
            non_clickable_icon.click("scroll",SCROLL_VALUE)

        sleep(scroll_delay)
            
def start_new_video(pos):
    left_click(new_x_pos=pos[0],new_y_pos=pos[1])
    sleep(5)
    
    for _ in range(5):
        border = Screen().capture("img/border.png",exceptions="silent")
        if border:
            break
    else:
        raise BorderNotFoundException()
    
    border_pos = border.get_pos()

    left_click(new_x_pos=border_pos[0]+20,new_y_pos=border_pos[1]+20)
    sleep(5)
    if Screen().capture("img/stopped.png"):
        left_click(new_x_pos=border_pos[0]+20,new_y_pos=border_pos[1]+20)


def control_current_video(scroll_delay=SCROLL_DELAY, video_check_delay=VIDEO_CHECK_DELAY):
    for _ in range(5):
        cur_icon = Screen().capture("img/current_icon.png")
        if cur_icon:
            break
    else:
        raise VideoIconNotFoundException()
    
    while True:
        finished_icons = Screen().capture("img/finished_icon.png",mode="all")

        if cur_icon.get_pos()[:2] in ([] if not finished_icons else [i.get_pos()[:2] for i in finished_icons]):
            scroll_and_start_new_video(scroll_delay, video_check_delay)
            break

        sleep(video_check_delay)


def start(scroll_delay=SCROLL_DELAY, video_check_delay=VIDEO_CHECK_DELAY):
    scroll_and_start_new_video(scroll_delay, video_check_delay)
