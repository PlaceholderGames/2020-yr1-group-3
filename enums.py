"""
Author:  Nathan Dow / Bitheral
Created: 24/10/2020
"""
from enum import Enum


# Screens list
# All possible screens to exist
class Screens(Enum):
    SPLASHSCREEN = -1
    MAIN_MENU = 0
    SETTINGS = 1
    CREDITS = 2
    QUIT = 3
    GAME = 4
    SOUND_WARNING = 5


# Direction list
# All possible directions to exit
# Needed for player attack
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8

# Scene list
# All scenes in game
# Needed for portals
class Scenes(Enum):
    TUTORIAL = 0
    LEVEL_1 = 1
