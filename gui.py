"""
    Author:  Nathan Dow / Bitheral
    Created: 23/10/2020
"""
import pygame
import re
import consts
from enums import Screens
import util

pygame.font.init()
DEFAULT_FONT = pygame.font.Font("assets/fonts/Pixellari.ttf", 32)


def image(image_file):
    _image = pygame.image.load(image_file).convert_alpha()
    return _image


def text(_text, font, size):
    temp_font = pygame.font.Font(f"assets/fonts/{font}.ttf", size)
    return temp_font.render(_text, False, (255, 255, 255))


class Spritesheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            consts.LOGGER("Valhalla", f"Unable to load image as a spritesheet: {filename}")

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class Text:
    def __init__(self, _text, font_name, size, x, y):
        self.font = pygame.font.Font(f"assets/fonts/{font_name}.ttf", size)
        self.colour = (255, 255, 255)
        self.text = _text
        self.pos = (x, y)

    def render(self):
        return self.font.render(self.text, False, self.colour)

    def get_text(self):
        return self.text

    def get_size(self):
        return self.font.size(self.text)

    def get_pos(self):
        return self.pos

    def set_color(self, color):
        self.colour = color

    def set_text(self, text):
        self.text = text

    def set_pos(self, pos):
        self.pos = pos


class Button:
    def __init__(self, text_element, x, y):
        self.text = text_element
        self.pos = (x, y)
        self.size = (self.text.get_size()[0] * 2, self.text.get_size()[1] * 2)
        self.area = (self.pos[0] - self.text.get_size()[0] / 2, self.pos[1] - self.text.get_size()[1] / 2, self.size[0],
                     self.size[1])

    def render(self):
        usw_logo = image("assets/textures/gui/usw_logo.png")
        window_width, window_height = pygame.display.get_surface().get_size()
        if self.on_hover():
            pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), self.area)
        else:
            pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), self.area),

        if self.has_clicked():
            pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), self.area)
        return self.text.render()

    def get_pos(self):
        return self.pos

    def get_size(self):
        return self.size

    def set_pos(self, pos):
        self.pos = pos

    def set_action(self, action):
        self.action = action

    def on_hover(self):
        return self.area[0] < consts.MOUSE.get_pos()[0] < self.area[0] + self.area[2] and self.area[1] < consts.MOUSE.get_pos()[1] < self.area[1] + self.area[3]
        #return self.area[0] < consts.MOUSE.get_pos()[0] < self.area[2] and self.area[1] < consts.MOUSE.get_pos()[1] < self.area[3]

    def has_clicked(self):
        if self.on_hover():
            for event in pygame.event.get():
                return event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP

    def on_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), self.area)
        if self.area[0] < mouse_x < self.area[2] and self.area[1] < mouse_y < self.area[3]:
            self.action()


class GUIScreen(pygame.Surface):

    def __init__(self):
        super(GUIScreen, self).__init__(pygame.display.get_surface().get_size())
        self.components = []

    def add_element(self, element):
        self.components.append(element)

    def add_element_position(self, element, pos):
        self.components.append((element, pos))

    def click(self):
        for element in self.components:
            if isinstance(element, Button):
                element.on_click()

    def render(self):
        for component in self.components:
            if isinstance(component, tuple):
                pygame.display.get_surface().blit(component[0], component[1])
            elif isinstance(component, list):
                for element in component:
                    pygame.display.get_surface().blit(element.render(), element.get_pos())
            else:
                pygame.display.get_surface().blit(component.render(), component.get_pos())
            """
            if isinstance(element[0], list):
                
                for el in element[0]:
                    pygame.display.get_surface().blit(el, element[1])
            else:
                pygame.display.get_surface().blit(element[0], element[1])
            """


class DebugOverlay(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        debug_mode_str = f"DEBUG OVERLAY - Press F12 to disable"
        debug_mode_text = Text(debug_mode_str, "Pixellari", 26, 16, 16)
        debug_mode_text.set_color((255,0,0))

        caption_str = f"Mouse position: {consts.MOUSE.get_pos()}"
        caption_text = Text(caption_str, "Pixellari", 26, 16, 48)

        self.add_element(caption_text)
        self.add_element(debug_mode_text)


class SplashScreen(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        usw_logo = image("assets/textures/gui/usw_logo.png")
        usw_logo_width, usw_logo_height = usw_logo.get_size()
        self.add_element_position(usw_logo,
                                  (window_width / 2 - usw_logo_width / 2, window_height / 2 - usw_logo_height))

        caption_str = "A game created by students at the University of South Wales"
        caption_text = Text(caption_str, "Pixellari", 26, window_width / 2, window_height / 2)
        caption_text_width, caption_text_height = caption_text.get_size()
        caption_text.set_pos(((window_width / 2) - caption_text_width / 2, window_height / 2 - caption_text_height))
        self.add_element(caption_text)


class MainMenu(GUIScreen):

    def play(self):
        consts.LOGGER.debug("VALHALLA", "Play button pressed")

    def settings(self):
        consts.LOGGER.debug("VALHALLA", "Settings button pressed")

    def credits(self):
        consts.LOGGER.debug("VALHALLA", "Credits button pressed")

    def quit(self):
        consts.LOGGER.debug("VALHALLA", "Quit button pressed")
        util.quit_game()

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()
        play_offset = (0, -64)
        settings_offset = (-16, 0)
        credits_offset = (-14, 64)
        quit_offset = (0, 128)

        # self.add_element(text("Text", "Pixellari", 26))
        play_text = Text("Play", "Pixellari", 26, (window_width / 2) + play_offset[0],
                         (window_height / 2) + play_offset[1])
        play_button = Button(play_text, (window_width / 2) + play_offset[0], (window_height / 2) + play_offset[1])
        play_button.set_action(self.play)

        settings_text = Text("Settings", "Pixellari", 26, (window_width / 2) + settings_offset[0],
                             (window_height / 2) + settings_offset[1])
        settings_button = Button(settings_text, (window_width / 2) + settings_offset[0],
                                 (window_height / 2) + settings_offset[1])
        settings_button.set_action(self.settings)

        credits_text = Text("Credits", "Pixellari", 26, (window_width / 2) + credits_offset[0],
                            (window_height / 2) + credits_offset[1])
        credits_button = Button(credits_text, (window_width / 2) + credits_offset[0],
                                (window_height / 2) + credits_offset[1])
        credits_button.set_action(self.credits)

        quit_text = Text("Quit", "Pixellari", 26, (window_width / 2) + quit_offset[0],
                         (window_height / 2) + quit_offset[1])
        quit_button = Button(quit_text, (window_width / 2) + quit_offset[0], (window_height / 2) + quit_offset[1])
        quit_button.set_action(self.quit)

        self.add_element(play_button)
        self.add_element(settings_button)
        self.add_element(credits_button)
        self.add_element(quit_button)
