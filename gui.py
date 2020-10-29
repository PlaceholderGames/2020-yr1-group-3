"""
    Author:  Nathan Dow / Bitheral
    Created: 23/10/2020
"""
import pygame
import re
import consts
from enums import Screens
from game import Game
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
        self.area = (
            self.pos[0] - self.text.get_size()[0] / 2,
            self.pos[1] - self.text.get_size()[1] / 2,
            self.size[0],
            self.size[1]
        )

    def render(self):
        if self.on_hover():
            pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), self.area)
        else:
            pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), self.area)

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
        return self.area[0] < consts.MOUSE.get_pos()[0] < self.area[0] + self.area[2] and self.area[1] < \
               consts.MOUSE.get_pos()[1] < self.area[1] + self.area[3]


class GUIScreen(pygame.Surface):

    def __init__(self):
        super(GUIScreen, self).__init__(pygame.display.get_surface().get_size())
        self.components = {}

    def add_element(self, name, element):
        self.components[name] = element
        # self.components.append(element)

    def add_element_position(self, name, element, pos):
        self.components[name] = (element, pos)
        # self.components.append((element, pos))

    def handle_mouse_event(self):
        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            for component in self.components:
                if isinstance(self.components[component], Button):
                    button = self.components[component]
                    if button.on_hover():
                        button.action()

    def render(self):
        for component in self.components:
            if isinstance(self.components[component], tuple):
                pygame.display.get_surface().blit(self.components[component][0], self.components[component][1])
            else:
                pygame.display.get_surface().blit(self.components[component].render(),
                                                  self.components[component].get_pos())


class DebugOverlay(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        debug_mode_str = f"DEBUG OVERLAY - Press F12 to disable"
        debug_mode_text = Text(debug_mode_str, "Pixellari", 26, 16, 16)
        debug_mode_text.set_color((255, 0, 0))

        debug_mode_warning_str = f"WARNING - Opening this menu will slow down gameplay"
        debug_mode_warning_text = Text(debug_mode_warning_str, "Pixellari", 18, 16, 48)
        debug_mode_warning_text.set_color((255, 0, 0))

        mouse_str = f"Mouse position: {consts.MOUSE.get_pos()}"
        mouse_text = Text(mouse_str, "Pixellari", 26, 16, 72)

        screen_str = f"Current screen: {Screens(consts.current_screen).name}"
        screen_text = Text(screen_str, "Pixellari", 26, 16, 104)

        self.add_element("Debug text", debug_mode_text)
        self.add_element("Debug warning", debug_mode_warning_text)
        self.add_element("Mouse position", mouse_text)
        self.add_element("Current Screen", screen_text)

    def render(self):
        super(DebugOverlay, self).render()
        self.components["Mouse position"].set_text(f"Mouse position: {consts.MOUSE.get_pos()}")
        self.components["Current Screen"].set_text(f"Current screen: {Screens(consts.current_screen).name}")
        if consts.game is not None:
            player_str = f"Player position: {(round(consts.game.get_player().x, 2), round(consts.game.get_player().y, 2))}"
            player_text = Text(player_str, "Pixellari", 26, 16, 136)

            self.add_element("Player position", player_text)


class GameOverlay(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        health_str = f"Health: {int(consts.game.get_player().health)}"
        health_text = Text(health_str, "Pixellari", 26, 16, 16)

        self.add_element("Health text", health_text)

    def render(self):
        super(GameOverlay, self).render()
        self.components["Health text"].set_text(f"Health: {int(consts.game.get_player().health)}")


class SplashScreen(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        usw_logo = image("assets/textures/gui/usw_logo.png")
        usw_logo_width, usw_logo_height = usw_logo.get_size()
        self.add_element_position("USW logo", usw_logo,
                                  (window_width / 2 - usw_logo_width / 2, window_height / 2 - usw_logo_height))

        caption_str = "A game created by students at the University of South Wales"
        caption_text = Text(caption_str, "Pixellari", 26, window_width / 2, window_height / 2)
        caption_text_width, caption_text_height = caption_text.get_size()
        caption_text.set_pos(((window_width / 2) - caption_text_width / 2, window_height / 2 - caption_text_height))
        self.add_element("Caption", caption_text)


class MainMenu(GUIScreen):

    def play_action(self):
        consts.LOGGER.debug("VALHALLA", "Play button pressed")
        consts.current_screen = Screens.GAME
        consts.LOGGER.info("VALHALLA", "Initializing new game")
        consts.game = Game()

    def settings_action(self):
        consts.LOGGER.debug("VALHALLA", "Settings button pressed")

    def credits_action(self):
        consts.LOGGER.debug("VALHALLA", "Credits button pressed")
        consts.current_screen = Screens.CREDITS

    def quit_action(self):
        consts.LOGGER.debug("VALHALLA", "Quit button pressed")
        consts.current_screen = Screens.QUIT

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()
        play_offset = (0, -64)
        settings_offset = (-16, 0)
        credits_offset = (-14, 64)
        quit_offset = (0, 128)

        logo_temp_text = Text("THE BEERZERKER", "Pixellari", 48, (window_width / 2) - 160,
                         (window_width / 8))

        play_text = Text("Play", "Pixellari", 26, (window_width / 2) + play_offset[0],
                         (window_height / 2) + play_offset[1])
        play_button = Button(play_text, (window_width / 2) + play_offset[0], (window_height / 2) + play_offset[1])
        play_button.set_action(self.play_action)

        settings_text = Text("Settings", "Pixellari", 26, (window_width / 2) + settings_offset[0],
                             (window_height / 2) + settings_offset[1])
        settings_button = Button(settings_text, (window_width / 2) + settings_offset[0],
                                 (window_height / 2) + settings_offset[1])
        settings_button.set_action(self.settings_action)

        credits_text = Text("Credits", "Pixellari", 26, (window_width / 2) + credits_offset[0],
                            (window_height / 2) + credits_offset[1])
        credits_button = Button(credits_text, (window_width / 2) + credits_offset[0],
                                (window_height / 2) + credits_offset[1])
        credits_button.set_action(self.credits_action)

        quit_text = Text("Quit", "Pixellari", 26, (window_width / 2) + quit_offset[0],
                         (window_height / 2) + quit_offset[1])
        quit_button = Button(quit_text, (window_width / 2) + quit_offset[0], (window_height / 2) + quit_offset[1])
        quit_button.set_action(self.quit_action)

        self.add_element("Logo", logo_temp_text)
        self.add_element("Play", play_button)
        self.add_element("Settings", settings_button)
        self.add_element("Credits", credits_button)
        self.add_element("Quit", quit_button)


class CreditScreen(GUIScreen):

    def back_action(self):
        consts.LOGGER.debug("VALHALLA", "Back button pressed")
        consts.current_screen = Screens.MAIN_MENU

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()
        title_offset = (-14, 0)

        lead_programmer_title_offset = (-70, 0)
        lead_programmer_credit_offset = (-40, 32)

        programmer_title_offset = (-48, 16)
        programmer_credit_offset = (-104, 48)

        back_offset = (0, 192)

        screen_title = Text("Credits", "Pixellari", 26, (window_width / 2) + title_offset[0],
                            (window_width / 12) + title_offset[1])

        lead_programmer_title = Text("Lead Programmer", "Pixellari", 26,
                                     (window_width / 2) + lead_programmer_title_offset[0],
                                     (window_width / 6) + lead_programmer_title_offset[1])
        lead_programmer_credit = Text("Nathan Dow", "Pixellari", 26,
                                      (window_width / 2) + lead_programmer_credit_offset[0],
                                      (window_width / 6) + lead_programmer_credit_offset[1])

        programmer_title = Text("Programmers", "Pixellari", 26,
                                     (window_width / 2) + programmer_title_offset[0],
                                     (window_width / 4) + programmer_title_offset[1])
        programmer_credit = Text("Bartosz Swieszkowski", "Pixellari", 26,
                                      (window_width / 2) + programmer_credit_offset[0],
                                      (window_width / 4) + programmer_credit_offset[1])

        back_text = Text("Back", "Pixellari", 26, (window_width / 2) + back_offset[0],
                         (window_height / 2) + back_offset[1])
        back_button = Button(back_text, (window_width / 2) + back_offset[0], (window_height / 2) + back_offset[1])
        back_button.set_action(self.back_action)

        self.add_element("Credit title", screen_title)

        self.add_element("Lead Programmer title", lead_programmer_title)
        self.add_element("Lead Programmer credit", lead_programmer_credit)

        self.add_element("Programmer title", programmer_title)
        self.add_element("Programmer credit", programmer_credit)

        self.add_element("Back button", back_button)
