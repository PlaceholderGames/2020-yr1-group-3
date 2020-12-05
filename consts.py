"""
    Author:  Nathan Dow / Bitheral
    Created: 24/10/2020
"""
from enums import Screens
from util import Logger, Mouse

running = True
game = None
version = "0.7.1"

current_screen = Screens.SPLASHSCREEN
last_screen = Screens.SPLASHSCREEN
current_scene = 0
time_since_start = 0
start_time = None
LOGGER = Logger()
MOUSE = Mouse()

clock = None

SETTINGS_TEMPLATE = {
    "DEBUG_OVERLAY": False,
    "FULLSCREEN": False,
    "RESOLUTION": {
        "WIDTH":  800,
        "HEIGHT":  600
    }
}


SETTINGS = {}
