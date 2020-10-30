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
    RIGHT = 1
    LEFT = -1
    UP = 2
    DOWN = 3
