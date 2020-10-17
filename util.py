"""
    Author:  Nathan Dow / Bitheral
    Created: 14/10/2020
"""

import pygame


# Loads image files into Pygame
def load_image(image_file):
    image = pygame.image.load(image_file).convert_alpha()
    return image


# Loads audio files into Pygame
def load_audio(audio_file):
    return pygame.mixer.Sound(audio_file)


# Loads font files into Pygame
def load_font(font_file, font_size, system_font=False):
    if system_font:
        return pygame.font.SysFont(font_file, font_size)
    else:
        return pygame.font.Font(font_file, font_size)


# Renders text with fonts
def text(_text, font, color=(255, 255, 255)):
    return font.render(_text, True, color)


# Allows stuff to be rendered such as images and text
def render(canvas, _render, x, y, area=None):
    canvas.blit(_render, (x, y), area)


# Creates a fade in effect
def fade_in(screen, canvas, time, render):
    for alpha in range(255, 0, -1):
        canvas.set_alpha(alpha)
        render()
        screen.blit(canvas, (0, 0))
        pygame.display.update()
        pygame.time.delay(time)


# Creates a fade out effect
def fade_out(screen, canvas, time, render):
    for alpha in range(0, 255):
        canvas.fill((0, 0, 0))
        canvas.set_alpha(alpha)
        render()
        screen.blit(canvas, (0, 0))
        pygame.display.update()
        pygame.time.delay(time)


def create_settings_file():
    import json
    from consts import SETTINGS

    with open("settings.json", 'w') as settingFile:
        json.dump(SETTINGS, settingFile)
    settingFile.close()


def save_settings():
    from consts import CHECKBOXES, SETTINGS
    import json

    SETTINGS['SHOW_FPS'] = CHECKBOXES['SETTINGS']['show_fps'].state
    SETTINGS['FULLSCREEN'] = CHECKBOXES['SETTINGS']['fullscreen'].state

    with open("settings.json", "w") as settingsFile:
        json.dump(SETTINGS, settingsFile)
    settingsFile.close()


def load_settings():
    import consts
    import json
    import os

    if os.path.exists("settings.json"):
        with open("settings.json", "r") as settingsFile:
            data = json.load(settingsFile)
            consts.CHECKBOXES['SETTINGS']['fullscreen'].state = data['FULLSCREEN']
            consts.CHECKBOXES['SETTINGS']['show_fps'].state = data['SHOW_FPS']
            consts.SETTINGS = data
        settingsFile.close()


def load_settings_file():
    import json
    import os

    if os.path.exists("settings.json"):
        with open("settings.json", 'r') as settingsFile:
            data = json.load(settingsFile)
        settingsFile.close()
        return data
