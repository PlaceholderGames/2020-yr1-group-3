"""
    Author:  Nathan Dow / Bitheral
    Created: 15/10/2020
"""

import pygame
import util
import enum

pygame.font.init()

DIMENSIONS = {
    'width': 800,
    'height': 600
}

TEXTURES = {
    # 'window_icon': util.load_image("assets/textures/gui/icon.png")
    # 'player_spritesheet': util.load_image("assets/textures/spritesheets/player.png"),
    'usw_logo': util.load_image("assets/textures/gui/usw_logo.png"),
    'button': util.load_image("assets/textures/gui/button.png")
}

"""
# All sounds get initialized and assigned
SOUNDS = {

}
"""

# All fonts get initialized and assigned
FONTS = {
    'Pixellari': util.load_font("assets/fonts/Pixellari.ttf", 24, False)
}


class Screens(enum.Enum):
    MAIN_MENU = 0
    SETTINGS = 1
    CREDITS = 2
    GAME = 3
    QUIT = 4


BUTTONS = {
    'MAIN_MENU': {
        'play': util.Button((DIMENSIONS['width'] / 2) - 64, 82, 128, 64, "Play", Screens.GAME),
        'settings': util.Button((DIMENSIONS['width'] / 2) - 64, 150, 128, 64, "Settings", Screens.SETTINGS),
        'credits': util.Button((DIMENSIONS['width'] / 2) - 64, 218, 128, 64, "Credits", Screens.CREDITS),
        'quit': util.Button((DIMENSIONS['width'] / 2) - 64, 286, 128, 64, "Quit", Screens.QUIT),
    },
    "CREDITS": {
        'back': util.Button((DIMENSIONS['width'] / 2) - 64, 488, 128, 64, "Back", Screens.MAIN_MENU),
    }
}
