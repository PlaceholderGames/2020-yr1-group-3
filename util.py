"""
    Author:  Nathan Dow / Bitheral
    Created: 14/10/2020
"""

import pygame


# Loads image files into Pygame
def load_image(image_file):
    return pygame.image.load(image_file)


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


def save_settings():
    with open("settings.json", "w") as settingsFile:
        from consts import SETTINGS
        import json
        json.dump(SETTINGS, settingsFile)
        settingsFile.close()
