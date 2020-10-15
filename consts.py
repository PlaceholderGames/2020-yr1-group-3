"""
    Author:  Nathan Dow / Bitheral
    Created: 15/10/2020
"""

import pygame
import util
import enum

pygame.font.init()

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

BUTTONS = {
    'mm_play': util.Button(16, 64, 128, 64, "Play"),
    'mm_settings': util.Button(16, 64, 128, 64, "Settings"),
    'mm_credits': util.Button(16, 64, 128, 64, "Credits"),
    'mm_quit': util.Button(16, 64, 128, 64, "Quit")
}



class Screens(enum.Enum):
    MAIN_MENU = 0
    SETTINGS = 1
    CREDITS = 2
    GAME = 3
