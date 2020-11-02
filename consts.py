"""
    Author:  Nathan Dow / Bitheral
    Created: 24/10/2020
"""
from enums import Screens
from util import Logger, Mouse

running = True
game = None
version = "1.0.0"

current_screen = Screens.SPLASHSCREEN
last_screen = Screens.SPLASHSCREEN
LOGGER = Logger()
MOUSE = Mouse()

SETTINGS_TEMPLATE = {
    "DEBUG_OVERLAY": False,
    "FULLSCREEN": False,
    "RESOLUTION": {
        "WIDTH":  800,
        "HEIGHT":  600
    }
}


SETTINGS = {}
