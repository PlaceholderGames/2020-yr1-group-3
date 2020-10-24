"""
    Author:  Nathan Dow / Bitheral
    Created: 23/10/2020
"""
import pygame
import re
import consts
from enums import Screens

pygame.font.init()
DEFAULT_FONT = pygame.font.Font("assets/fonts/Pixellari.ttf", 32)


def image(image_file):
    _image = pygame.image.load(image_file).convert_alpha()
    return _image


def text(_text, font, size):
    temp_font = pygame.font.Font(f"assets/fonts/{font}.ttf", size)
    return temp_font.render(_text, False, (255, 255, 255))


class Text:
    def __init__(self, _text, font_name, size):
        self.font = pygame.font.Font(f"assets/fonts/{font_name}.ttf", size)
        self.colour = (255, 255, 255)
        self.text = _text

    def set_color(self, color):
        self.colour = color

    def get_size(self):
        return self.font.size(self.text)

    def render(self):
        return self.font.render(self.text, False, self.colour)


class GUIScreen(pygame.Surface):

    def __init__(self):
        super(GUIScreen, self).__init__(pygame.display.get_surface().get_size())
        self.components = []

    def add_element(self, element, pos):
        temp_el = (element, pos)
        self.components.append(temp_el)

    def render(self):
        for element in self.components:
            pygame.display.get_surface().blit(element[0], element[1])


class SplashScreen(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        usw_logo = image("assets/textures/gui/usw_logo.png")
        usw_logo_width, usw_logo_height = usw_logo.get_size()
        self.add_element(usw_logo, (window_width / 2 - usw_logo_width / 2, window_height / 2 - usw_logo_height))

        caption_str = "A game created by students at the University of South Wales"
        caption_text = Text(caption_str, "Pixellari", 26)
        caption_width, caption_height = caption_text.get_size()
        self.add_element(caption_text.render(), (window_width / 2 - caption_width / 2, window_height / 2 - caption_height / 2))


class MainMenu(GUIScreen):

    def __init__(self):
        super().__init__()

        self.add_element(text("Text", "Pixellari", 26), (16, 16))
