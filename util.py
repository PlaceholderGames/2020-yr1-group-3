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
def load_font(font_file):
    return pygame.font.Font(font_file)
