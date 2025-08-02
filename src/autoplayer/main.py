from time import sleep
from autoplayer.handler import Screen
from autoplayer.events import left_click, scroll
from utils.constants import Player
from utils.exceptions import BorderNotFoundException, VideoIconNotFoundException

SCROLL_DELAY = Player.SCROLL_DELAY
BORDER_CHECK_DELAY = Player.BORDER_CHECK_DELAY
VIDEO_CHECK_DELAY = Player.VIDEO_CHECK_DELAY
PAGE_LOADING_DELAY = Player.PAGE_LOADING_DELAY
SCROLL_VALUE = Player.SCROLL_VALUE

def scroll_and_start_new_video(scroll_delay=SCROLL_DELAY, video_check_delay=VIDEO_CHECK_DELAY, page_loading_delay=PAGE_LOADING_DELAY):
    for _ in range(5):
        border = Screen().capture("img\\border.png", threshold = 0.95)
        if border:
            break
        sleep(BORDER_CHECK_DELAY)
    else:
        raise BorderNotFoundException()

    x, y, w, h = border.get_pos()
    left_click(x+w, y+h)
    scroll_until_video_list()
    sleep(SCROLL_DELAY+2)

    while True:
        videos_icons_screen = Screen()

        open_category_button = videos_icons_screen.capture("img\\open_button.png",mode="single")
        if open_category_button:
            open_category_button.click("left")

        new_video_icon = videos_icons_screen.capture("img\\new_video_icon.png", threshold = 0.95)
        if new_video_icon:
            x, y, w, h = new_video_icon.get_pos()
            start_new_video((x+w+19,y), page_loading_delay)
            scroll_current_video(scroll_delay=scroll_delay, page_loading_delay=page_loading_delay)
            control_current_video(scroll_delay=scroll_delay, video_check_delay=video_check_delay)
            break

        current_video_icon = videos_icons_screen.capture("img\\selected_current_icon.png") or videos_icons_screen.capture("img\\current_icon.png")
        if current_video_icon:
            x, y, w, h = current_video_icon.get_pos()
            start_new_video((x+w+19,y), page_loading_delay)
            scroll_current_video(scroll_delay=scroll_delay)
            control_current_video(scroll_delay=scroll_delay, video_check_delay=video_check_delay)
            break

        finished_icon = videos_icons_screen.capture("img\\selected_finished_icon.png") or videos_icons_screen.capture("img\\finished_icon.png")
        if finished_icon:
            finished_icon.click("scroll",SCROLL_VALUE)
            sleep(scroll_delay)
            continue

        non_clickable_icon = videos_icons_screen.capture("img\\non_clickable_icon.png", threshold = 0.95)
        if non_clickable_icon:
            non_clickable_icon.click("scroll",SCROLL_VALUE)

        sleep(scroll_delay)

def scroll_until_video_list(scroll_delay=SCROLL_DELAY):
    while True:
        if Screen().capture("img\\video_list_indicator.png", threshold = 0.9):
            break
        
        scroll(SCROLL_VALUE)
        sleep(scroll_delay)

def scroll_current_video(scroll_delay=SCROLL_DELAY):
    for _ in range(5):
        border = Screen().capture("img\\border.png", threshold = 0.95)
        if border:
            break
        sleep(BORDER_CHECK_DELAY)
    else:
        raise BorderNotFoundException()

    border.click("left")
    scroll_until_video_list()
    sleep(SCROLL_DELAY+2)

    while True:
        videos_icons_screen = Screen()

        open_category_button = videos_icons_screen.capture("img\\open_button.png",mode="single",threshold=0.9)
        if open_category_button:
            open_category_button.click("left")      

        if videos_icons_screen.capture("img\\selected_current_icon.png"):
            break

        finished_icon = videos_icons_screen.capture("img\\finished_icon.png")
        if finished_icon:
            finished_icon.click("scroll",SCROLL_VALUE)
            sleep(scroll_delay)
            continue

        non_clickable_icon = videos_icons_screen.capture("img\\non_clickable_icon.png")
        if non_clickable_icon:
            non_clickable_icon.click("scroll",SCROLL_VALUE)

        sleep(scroll_delay)

def start_new_video(pos, page_loading_delay=PAGE_LOADING_DELAY):
    left_click(new_x_pos=pos[0],new_y_pos=pos[1])
    
    sleep(page_loading_delay)

    for _ in range(5):
        border = Screen().capture("img\\border.png", threshold = 0.95)
        if border:
            break
        sleep(BORDER_CHECK_DELAY)
    else:
        raise BorderNotFoundException()

    x, y, w, h = border.get_pos()
    left_click(x+w, y+h)


def control_current_video(scroll_delay=SCROLL_DELAY, video_check_delay=VIDEO_CHECK_DELAY):
    for _ in range(5):
        selected_current_icon = Screen().capture("img\\selected_current_icon.png")
        if selected_current_icon:
            break
    else:
        raise VideoIconNotFoundException()

    while True:
        finished_icons = Screen().capture("img\\selected_finished_icon.png",mode="all")

        if selected_current_icon.get_pos()[:2] in ([] if not finished_icons else [i.get_pos()[:2] for i in finished_icons]):
            scroll_and_start_new_video(scroll_delay, video_check_delay)
            break

        sleep(video_check_delay)


def start(scroll_delay=SCROLL_DELAY, video_check_delay=VIDEO_CHECK_DELAY, page_loading_delay=PAGE_LOADING_DELAY):
    scroll_and_start_new_video(scroll_delay, video_check_delay, page_loading_delay)
