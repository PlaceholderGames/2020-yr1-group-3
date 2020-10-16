"""
    Author:  Nathan Dow / Bitheral
    Created: 15/10/2020
"""

import pygame
import util
import enum
import gui

pygame.font.init()


# All screens
class Screens(enum.Enum):
    MAIN_MENU = 0
    SETTINGS = 1
    CREDITS = 2
    GAME = 3
    QUIT = 4


# Window dimensions
DIMENSIONS = {
    'width': 800,
    'height': 600
}

# All textures get initialized and assigned
TEXTURES = {
    # 'window_icon': util.load_image("assets/textures/gui/icon.png")
    # 'player_spritesheet': util.load_image("assets/textures/spritesheets/player.png"),
    'usw_logo': util.load_image("assets/textures/gui/usw_logo.png"),
    'button': util.load_image("assets/textures/gui/button.png"),
    'checkbox': gui.Spritesheet("assets/textures/gui/checkbox.png")
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

# All buttons in the game, organized by screen
BUTTONS = {
    'MAIN_MENU': {
        'play': gui.Button((DIMENSIONS['width'] / 2) - 64, 82, 128, 64, "Play", Screens.GAME),
        'settings': gui.Button((DIMENSIONS['width'] / 2) - 64, 150, 128, 64, "Settings", Screens.SETTINGS),
        'credits': gui.Button((DIMENSIONS['width'] / 2) - 64, 218, 128, 64, "Credits", Screens.CREDITS),
        'quit': gui.Button((DIMENSIONS['width'] / 2) - 64, 286, 128, 64, "Quit", Screens.QUIT),
    },
    "CREDITS": {
        'back': gui.Button((DIMENSIONS['width'] / 2) - 64, 488, 128, 64, "Back", Screens.MAIN_MENU),
    }
}

CHECKBOXES = {
    'SETTINGS': {
        'fullscreen': gui.Checkbox((DIMENSIONS['width'] / 2) - 64, 488, 128, 64, "Back", Screens.CREDITS, True)
    }
}

CREDITS = {
    'LEAD_PROGRAMMER': gui.Credit(98, "Lead Programmer:", ['Nathan Dow / Bitheral']),
    'PROGRAMMING': gui.Credit(176, "Programming:", ['Bartosz Swieszkowski', 'Conner Hughes']),
    'LEAD_ARTIST': gui.Credit(270, "Lead Artist:", ['Conner Hughes']),
    "CONCEPT_ARTIST": gui.Credit(348, "Concept Artist:", ['Bartosz Swieszkowski'])
}

SETTINGS = {
    'DEBUG_MODE': False,
    'FULLSCREEN': False,
    'RESOLUTION': {
        'WIDTH': 600,
        'HEIGHT': 800
    },
    'FPS_LIMIT': 120
}
