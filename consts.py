"""
    Author:  Nathan Dow / Bitheral
    Created: 15/10/2020
"""

import pygame
import util
import enum
import gui
import ctypes
import os

pygame.font.init()


# All screens
class Screens(enum.Enum):
    MAIN_MENU = 0
    SETTINGS = 1
    CREDITS = 2
    GAME = 3
    QUIT = 4


if not os.path.exists("settings.json"):
    SETTINGS = {
        'SHOW_FPS': False,
        'FULLSCREEN': False,
        'RESOLUTION': {
            'WIDTH': 800,
            'HEIGHT': 600
        },
        'FPS_LIMIT': 120
    }
else:
    SETTINGS = util.load_settings_file()

DIMENSIONS = {
    'width': SETTINGS['RESOLUTION']['WIDTH'],
    'height': SETTINGS['RESOLUTION']['HEIGHT']
}

if SETTINGS['FULLSCREEN']:
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    DIMENSIONS['width'] = screensize[0]
    DIMENSIONS['height'] = screensize[1]
    screen = pygame.display.set_mode((DIMENSIONS['width'], DIMENSIONS['height']), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((DIMENSIONS['width'], DIMENSIONS['height']))

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
        'play':     gui.Button((DIMENSIONS['width'] / 2) - 64, ((DIMENSIONS['height'] / 2) - 32) - 128, 128, 64, "Play", Screens.GAME),
        'settings': gui.Button((DIMENSIONS['width'] / 2) - 64, ((DIMENSIONS['height'] / 2) - 32) - 64, 128, 64, "Settings", Screens.SETTINGS),
        'credits':  gui.Button((DIMENSIONS['width'] / 2) - 64, ((DIMENSIONS['height'] / 2) - 32), 128, 64, "Credits", Screens.CREDITS),
        'quit':     gui.Button((DIMENSIONS['width'] / 2) - 64, ((DIMENSIONS['height'] / 2) - 32) + 64, 128, 64, "Quit", Screens.QUIT),
    },
    "SETTINGS": {
        'back': gui.Button((DIMENSIONS['width'] / 2) + 16,         DIMENSIONS['height'] - 128, 128, 64, "Back", Screens.MAIN_MENU),
        'save': gui.Button((DIMENSIONS['width'] / 2) - (128 + 16), DIMENSIONS['height'] - 128, 128, 64, "Save", Screens.MAIN_MENU),
    },
    "CREDITS": {
        'back': gui.Button((DIMENSIONS['width'] / 2) - 64, DIMENSIONS['height'] - 128, 128, 64, "Back", Screens.MAIN_MENU),
    },
    "PAUSE": {
        'play':     gui.Button((DIMENSIONS['width'] / 2) - 64, ((DIMENSIONS['height'] / 2) - 32) - 128, 128, 64, "Back to game", Screens.GAME),
        'settings': gui.Button((DIMENSIONS['width'] / 2) - 64, ((DIMENSIONS['height'] / 2) - 32) - 64, 128, 64, "Settings", Screens.SETTINGS),
        'credits':  gui.Button((DIMENSIONS['width'] / 2) - 64, ((DIMENSIONS['height'] / 2) - 32), 128, 64, "Credits", Screens.CREDITS),
        'quit':     gui.Button((DIMENSIONS['width'] / 2) - 64, ((DIMENSIONS['height'] / 2) - 32) + 64, 128, 64, "Save andQuit", Screens.QUIT),
    }
}

CHECKBOXES = {
    'SETTINGS': {
        'fullscreen': gui.Checkbox((DIMENSIONS['width'] / 2) - 64, 128, 128, 32, "Fullscreen*", SETTINGS['FULLSCREEN']),
        'show_fps': gui.Checkbox((DIMENSIONS['width'] / 2) - 64, 164, 128, 32, "Show FPS", SETTINGS['SHOW_FPS'])
    }
}

CREDITS = {
    'LEAD_PROGRAMMER': gui.Credit(98, "Lead Programmer:", ['Nathan Dow']),
    'PROGRAMMING': gui.Credit(176, "Programming:", ['Bartosz Swieszkowski', 'Conner Hughes']),
    'LEAD_ARTIST': gui.Credit(270, "Lead Artist:", ['Conner Hughes']),
    "CONCEPT_ARTIST": gui.Credit(348, "Concept Artist:", ['Bartosz Swieszkowski'])
}
