"""
Author:  Nathan Dow / Bitheral
Created: 24/10/2020
"""
from enum import Enum


class Screens(Enum):
    SPLASHSCREEN = -1
    MAIN_MENU = 0
    SETTINGS = 1
    CREDITS = 2
    QUIT = 3
    GAME = 4


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8
