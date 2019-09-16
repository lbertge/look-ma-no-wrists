import os
import time
from bounds import UL_CORNER_RECT, UR_CORNER_RECT, LL_CORNER_RECT, LR_CORNER_RECT
import logging
import keyboard

class Command:
    def __init__(self, name, box, f):
        self.name = name
        self.f = f
        self.box = box

command_dict = {}
state_change = False

def register(cmd):
    command_dict[cmd.name] = cmd

def ll_command():
    logging.info("ll")
    keyboard.press_and_release("up")
    #os.system("osascript desktop_left.scpt")

def lr_command():
    logging.info("lr")

    keyboard.press_and_release("down")
    #os.system("osascript desktop_right.scpt")

def ul_command():
    logging.info("ul")
    os.system("osascript show_desktop.scpt")

def ur_command():
    logging.info("ur")

def zoom_in_command():
    logging.info("zoomIn")
    keyboard.press_and_release("command+plus")
    keyboard.press_and_release("command+plus")
    keyboard.press_and_release("command+plus")

def zoom_out_command():
    logging.info("zoomOut")
    keyboard.press_and_release("command+-")
    keyboard.press_and_release("command+-")
    keyboard.press_and_release("command+-")

register(Command('UL', UL_CORNER_RECT, ul_command))
register(Command('LL', LL_CORNER_RECT, ll_command))
register(Command('UR', UR_CORNER_RECT, ur_command))
register(Command('LR', LR_CORNER_RECT, lr_command))
register(Command('zoomIn', None, zoom_in_command))
register(Command('zoomOut', None, zoom_out_command))

if __name__ == '__main__':
    print("Running tests")
    right_command()
    left_command()
    top_command()
