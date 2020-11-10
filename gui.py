"""
    Author:  Nathan Dow / Bitheral
    Created: 23/10/2020
"""
import pygame
import re
import consts
import util
import os

from enums import Screens
from game import Game

pygame.font.init()


# Initialize an image
# Probably replaced with a class soon
def image(image_file, transparency=False):
    _image = pygame.image.load(image_file)
    if transparency:
        transparency_color = _image.get_at((0, 0))
        _image.set_colorkey(transparency_color)
    return _image.convert_alpha()


class Checkbox:
    def __init__(self, text_element, position):
        self.text = text_element
        self.pos = position
        self.state = False
        self.area = (
            self.pos[0],
            self.pos[1],
            32,
            32
        )

        self.text.set_pos((
            (self.pos[0] + 40),
            (self.pos[1] + 18) - self.text.get_size()[1] / 2
        ))

        self.sprite = util.Spritesheet("assets/textures/gui/checkbox.png")

    def render(self):
        #     Base sprite (No hover)                  Hover sprite
        off = (self.sprite.image_at((0, 0, 32, 32), -1), self.sprite.image_at((32, 0, 32, 32), -1))
        on = (self.sprite.image_at((0, 32, 32, 32), -1), self.sprite.image_at((32, 32, 32, 32), -1))

        sprite = off, on
        return sprite[int(self.state)][int(self.on_hover())]

    def get_pos(self):
        return self.pos

    def set_state(self, state):
        self.state = state

    def set_pos(self, pos):
        self.pos = pos

    def toggle(self):
        self.state = not self.state

    def on_hover(self):
        return self.area[0] < consts.MOUSE.get_pos()[0] < self.area[0] + self.area[2] and self.area[1] < \
               consts.MOUSE.get_pos()[1] < self.area[1] + self.area[3]


class Text:
    def __init__(self, _text, font_name, size, font_type=None, x=0, y=0):
        if os.path.isdir(f"assets/fonts/{font_name}"):
            self.font = pygame.font.Font(f"assets/fonts/{font_name}/{font_type}.ttf")
        else:
            self.font = pygame.font.Font(f"assets/fonts/{font_name}.ttf", size)
        self.colour = (255, 255, 255)
        self.text = _text
        self.pos = (x, y)

        self.font_name = font_name
        self.font_size = size

    def render(self):
        return self.font.render(self.text, False, self.colour)

    def get_font(self):
        return self.font_name

    def get_font_size(self):
        return self.font_size

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
    def __init__(self, text_element, position, size):
        self.text = text_element
        self.pos = position
        self.size = size
        self.area = (
            self.pos[0],
            self.pos[1],
            self.size[0],
            self.size[1]
        )

        self.text.set_pos((
            (self.pos[0] + self.size[0] / 2) - self.text.get_size()[0] / 2,
            (self.pos[1] + self.size[1] / 2) - self.text.get_size()[1] / 2
        ))

        self.sprite = util.Spritesheet("assets/textures/gui/button.png")

    def render(self):
        normal = self.sprite.image_at((0, 0, 128, 32), -1)
        hover = self.sprite.image_at((0, 32, 128, 32), -1)

        sprite = normal, hover

        return pygame.transform.scale(sprite[self.on_hover()], self.get_size())

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
                elif isinstance(self.components[component], Checkbox):
                    checkbox = self.components[component]
                    if checkbox.on_hover():
                        checkbox.toggle()

    def render(self):
        for component in self.components:
            element = self.components[component]

            if isinstance(element, Button):
                # Button texture
                pygame.display.get_surface().blit(element.render(), element.get_pos())
                # Button text

                droptext = Text(
                    element.text.get_text(),
                    element.text.get_font(),
                    element.text.get_font_size(),
                    x=element.text.get_pos()[0] + 3,
                    y=element.text.get_pos()[1] + 3
                )
                droptext.set_color((20, 20, 20))

                pygame.display.get_surface().blit(droptext.render(), droptext.get_pos())
                pygame.display.get_surface().blit(element.text.render(), element.text.get_pos())
            elif isinstance(element, Checkbox):
                droptext = Text(
                    element.text.get_text(),
                    element.text.get_font(),
                    element.text.get_font_size(),
                    x=element.text.get_pos()[0] + 3,
                    y=element.text.get_pos()[1] + 3
                )
                droptext.set_color((20, 20, 20))

                pygame.display.get_surface().blit(element.render(), element.get_pos())  # Checkbox image
                pygame.display.get_surface().blit(droptext.render(), droptext.get_pos())
                pygame.display.get_surface().blit(element.text.render(), element.text.get_pos())  # Text
            elif isinstance(element, Text):
                droptext = Text(
                    element.get_text(),
                    element.get_font(),
                    element.get_font_size(),
                    x=element.get_pos()[0] + 3,
                    y=element.get_pos()[1] + 3
                )
                droptext.set_color((20, 20, 20))

                pygame.display.get_surface().blit(droptext.render(), droptext.get_pos())
                pygame.display.get_surface().blit(element.render(), element.get_pos())
            elif isinstance(element, tuple):
                pygame.display.get_surface().blit(element[0], element[1])
            else:
                pygame.display.get_surface().blit(element.render(), element.get_pos())


class DebugOverlay(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        debug_mode_str = f"DEBUG OVERLAY - Press F12 to disable"
        debug_mode_text = Text(debug_mode_str, "Pixellari", 26, x=16, y=16)
        debug_mode_text.set_color((255, 0, 0))

        debug_mode_warning_str = f"WARNING - Opening this menu will slow down gameplay"
        debug_mode_warning_text = Text(debug_mode_warning_str, "Pixellari", 18, x=16, y=48)
        debug_mode_warning_text.set_color((255, 0, 0))

        mouse_str = f"Mouse position: {consts.MOUSE.get_pos()}"
        mouse_text = Text(mouse_str, "Pixellari", 26, x=16, y=72)

        screen_str = f"Current screen: {Screens(consts.current_screen).name}"
        screen_text = Text(screen_str, "Pixellari", 26, x=16, y=104)

        self.add_element("Debug text", debug_mode_text)
        self.add_element("Debug warning", debug_mode_warning_text)
        self.add_element("Mouse position", mouse_text)
        self.add_element("Current Screen", screen_text)

    def render(self):
        super(DebugOverlay, self).render()
        self.components["Mouse position"].set_text(f"Mouse position: {consts.MOUSE.get_pos()}")
        self.components["Current Screen"].set_text(f"Current screen: {Screens(consts.current_screen).name}")
        if consts.game is not None:
            player_str = f"Player position: {(round(consts.game.get_player().rect[0], 2), round(consts.game.get_player().rect[1], 2))}"
            player_text = Text(player_str, "Pixellari", 26, x=16, y=136)

            attack_str = f"Player attacking? : {consts.game.get_player().attacking}"
            attack_text = Text(attack_str, "Pixellari", 26, x=16, y=170)

            self.add_element("Player position", player_text)
            self.add_element("Player attack", attack_text)


class GameOverlay(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        health_str = f"Health: {int(consts.game.get_player().health)}"
        health_text = Text(health_str, "Pixellari", 26, x=16, y=16)
        self.add_element("Health text", health_text)

    def render(self):
        super(GameOverlay, self).render()
        self.components["Health text"].set_text(f"Health: {int(consts.game.get_player().health)}")


class PauseOverlay(GUIScreen):

    def play_action(self):
        consts.LOGGER.debug("VALHALLA", "Going back to game")
        consts.game.paused = False

    def settings_action(self):
        consts.last_screen = Screens.GAME
        consts.current_screen = Screens.SETTINGS

    def credits_action(self):
        consts.last_screen = Screens.GAME
        consts.current_screen = Screens.CREDITS

    def quit_action(self):
        consts.current_screen = Screens.MAIN_MENU

    def __init__(self):
        super().__init__()

        play_offset = (-164, -64)
        settings_offset = (-160 - 4, 8)
        credits_offset = (4, 8)
        quit_offset = (-164, 80)

        window_width, window_height = pygame.display.get_surface().get_size()

        paused_text = Text("Paused", "Pixellari", 48, x=(window_width / 2) - 75, y=(window_width / 8))

        play_text = Text("Back to game", "Pixellari", 26)
        play_button = Button(
            play_text,
            (window_width / 2 + play_offset[0], window_height / 2 + play_offset[1]),
            (328, 64)
        )
        play_button.set_action(self.play_action)

        settings_text = Text("Settings", "Pixellari", 26)
        settings_button = Button(
            settings_text,
            (window_width / 2 + settings_offset[0], window_height / 2 + settings_offset[1]),
            (160, 64)
        )
        settings_button.set_action(self.settings_action)

        credits_text = Text("Credits", "Pixellari", 26)
        credits_button = Button(
            credits_text,
            (window_width / 2 + credits_offset[0], window_height / 2 + credits_offset[1]),
            (160, 64)
        )
        credits_button.set_action(self.credits_action)

        quit_text = Text("Quit to main menu", "Pixellari", 26)
        quit_button = Button(
            quit_text,
            (window_width / 2 + quit_offset[0], window_height / 2 + quit_offset[1]),
            (328, 64)
        )
        quit_button.set_action(self.quit_action)

        self.add_element("Paused text", paused_text)
        self.add_element("Play", play_button)
        self.add_element("Settings", settings_button)
        self.add_element("Credits", credits_button)
        self.add_element("Quit", quit_button)


class SplashScreen(GUIScreen):

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        usw_logo = image("assets/textures/gui/usw_logo.jpg")
        usw_logo = pygame.transform.scale(usw_logo, (192, 192))

        usw_logo_width, usw_logo_height = usw_logo.get_size()
        self.add_element_position("USW logo", usw_logo,
                                  (window_width / 2 - usw_logo_width / 2, window_height / 2 - (usw_logo_height / 2)))

        caption_str = "A game created by students at the"
        usw_str = "University of South Wales"

        caption_text = Text(caption_str, "Pixellari", 26)
        usw_text = Text(usw_str, "Pixellari", 26)

        caption_text_width, caption_text_height = caption_text.get_size()
        usw_text_width, usw_text_height = usw_text.get_size()

        caption_text.set_pos((
            window_width / 2 - caption_text_width / 2,
            (window_height / 2 + usw_logo_height / 2) + caption_text_height
            #window_height / 2 + (caption_text_height / 2
        ))
        usw_text.set_pos((
            window_width / 2 - usw_text_width / 2,
            (window_height / 2 + usw_logo_height / 2) + (usw_text_height / 2) + caption_text_height + 16))
        self.add_element("Caption", caption_text)
        self.add_element("USW", usw_text)


class MainMenu(GUIScreen):

    def continue_action(self):
        consts.LOGGER.debug("VALHALLA", "Continue button pressed")
        consts.current_screen = Screens.GAME
        consts.LOGGER.info("VALHALLA", "Initializing new game")

    def play_action(self):
        consts.LOGGER.debug("VALHALLA", "Play button pressed")
        consts.current_screen = Screens.GAME
        consts.LOGGER.info("VALHALLA", "Initializing new game")
        consts.game = Game()
        consts.start_time = pygame.time.get_ticks()

    def settings_action(self):
        consts.LOGGER.debug("VALHALLA", "Settings button pressed")
        consts.last_screen = Screens.MAIN_MENU
        consts.current_screen = Screens.SETTINGS

    def credits_action(self):
        consts.LOGGER.debug("VALHALLA", "Credits button pressed")
        consts.last_screen = Screens.MAIN_MENU
        consts.current_screen = Screens.CREDITS

    def quit_action(self):
        consts.LOGGER.debug("VALHALLA", "Quit button pressed")
        consts.current_screen = Screens.QUIT

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()

        # Buttons offset
        self.continue_offset = (-164, -128)
        self.play_offset = (-164, -64)
        self.settings_offset = (-160 - 4, 8)
        self.credits_offset = (4, 8)
        self.quit_offset = (-164, 80)

        # Text offset
        version_offset = (-166, -32)

        controls_title_offset = (6, -86)
        move_offset = (8, -56)
        attack_offset = (8, -32)

        logo_temp_text = Text("THE BEERZERKER", "Pixellari", 48, x=(window_width / 2) - 196, y=(window_height / 6))
        continue_text = Text("Continue", "Pixellari", 26)
        self.continue_button = Button(
            continue_text,
            (window_width / 2 + self.continue_offset[0], window_height / 2 + self.continue_offset[1]),
            (328, 64)
        )
        self.continue_button.set_action(self.continue_action)

        play_text = Text("Play", "Pixellari", 26)
        self.play_button = Button(
            play_text,
            (window_width / 2 + self.play_offset[0], window_height / 2 + self.play_offset[1]),
            (328, 64)
        )
        self.play_button.set_action(self.play_action)

        settings_text = Text("Settings", "Pixellari", 26)
        self.settings_button = Button(
            settings_text,
            (window_width / 2 + self.settings_offset[0], window_height / 2 + self.settings_offset[1]),
            (160, 64)
        )
        self.settings_button.set_action(self.settings_action)

        credits_text = Text("Credits", "Pixellari", 26)
        self.credits_button = Button(
            credits_text,
            (window_width / 2 + self.credits_offset[0], window_height / 2 + self.credits_offset[1]),
            (160, 64)
        )
        self.credits_button.set_action(self.credits_action)

        quit_text = Text("Quit", "Pixellari", 26)
        self.quit_button = Button(
            quit_text,
            (window_width / 2 + self.quit_offset[0], window_height / 2 + self.quit_offset[1]),
            (328, 64)
        )
        self.quit_button.set_action(self.quit_action)

        version_text = Text(f"Version {consts.version}", "Pixellari", 26, x=window_width + version_offset[0],
                            y=window_height + version_offset[1])

        controls_title_text = Text("Controls:", "Pixellari", 26, x=controls_title_offset[0],
                                   y=window_height + controls_title_offset[1])

        move_text = Text("WASD or arrow keys to move", "Pixellari", 26, x=move_offset[0],
                         y=window_height + move_offset[1])

        attack_text = Text("Left click to attack", "Pixellari", 26, x=attack_offset[0],
                           y=window_height + attack_offset[1])

        self.add_element("Logo", logo_temp_text)
        self.add_element("Play", self.play_button)
        self.add_element("Settings", self.settings_button)
        self.add_element("Credits", self.credits_button)
        self.add_element("Quit", self.quit_button)

        self.add_element("Version", version_text)
        self.add_element("Controls text", controls_title_text)
        self.add_element("Move controls text", move_text)
        self.add_element("Attack controls text", attack_text)

    def render(self):
        super(MainMenu, self).render()

        window_width, window_height = pygame.display.get_surface().get_size()
        if consts.game is None:
            self.play_offset = (-164, -64)
            self.settings_offset = (-160 - 4, 8)
            self.credits_offset = (4, 8)
            self.quit_offset = (-164, 80)
        else:
            self.add_element("Continue", self.continue_button)
            self.continue_offset = (-164, -64)
            self.play_offset = (-164, 8)
            self.settings_offset = (-164, 80)
            self.credits_offset = (4, 80)
            self.quit_offset = (-164, 152)

        continue_text = Text("Continue", "Pixellari", 26)
        self.continue_button = Button(
            continue_text,
            (window_width / 2 + self.continue_offset[0], window_height / 2 + self.continue_offset[1]),
            (328, 64)
        )
        self.continue_button.set_action(self.continue_action)

        play_text = Text("Play" if consts.game is None else "New game", "Pixellari", 26)
        self.play_button = Button(play_text,
                                  (window_width / 2 + self.play_offset[0], window_height / 2 + self.play_offset[1]),
                                  (328, 64))
        self.play_button.set_action(self.play_action)

        settings_text = Text("Settings", "Pixellari", 26)
        self.settings_button = Button(settings_text, (
            window_width / 2 + self.settings_offset[0], window_height / 2 + self.settings_offset[1]), (160, 64))
        self.settings_button.set_action(self.settings_action)

        credits_text = Text("Credits", "Pixellari", 26)
        self.credits_button = Button(credits_text, (
            window_width / 2 + self.credits_offset[0], window_height / 2 + self.credits_offset[1]), (160, 64))
        self.credits_button.set_action(self.credits_action)

        quit_text = Text("Quit", "Pixellari", 26)
        self.quit_button = Button(quit_text,
                                  (window_width / 2 + self.quit_offset[0], window_height / 2 + self.quit_offset[1]),
                                  (328, 64))
        self.quit_button.set_action(self.quit_action)

        self.add_element("Play", self.play_button)
        self.add_element("Settings", self.settings_button)
        self.add_element("Credits", self.credits_button)
        self.add_element("Quit", self.quit_button)


class SettingScreen(GUIScreen):

    def back_action(self):
        consts.LOGGER.debug("VALHALLA", "Back button pressed")
        consts.current_screen = consts.last_screen

    def save_action(self):
        consts.LOGGER.debug("VALHALLA", "Save button pressed")
        consts.SETTINGS = {
            "FULLSCREEN": self.fullscreen_checkbox.state
        }
        util.save_to_settings_file()
        consts.current_screen = consts.last_screen

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()
        fullscreen_checkbox_offset = (0,0)
        fullscreen_checkbox_text = Text("Fullscreen*", "Pixellari", 26)
        self.fullscreen_checkbox = Checkbox(
            fullscreen_checkbox_text,
            (window_width / 6 + fullscreen_checkbox_offset[0], window_height / 3 + fullscreen_checkbox_offset[1]),
        )
        self.fullscreen_checkbox.state = consts.SETTINGS['FULLSCREEN']

        title_offset = (-42, 0)

        note_text_offset = (-270, 0)
        note_2_text_offset = (-360, 34)

        back_offset = (-128, 192)
        save_offset = (32, 192)

        screen_title = Text("Settings", "Pixellari", 26, x=(window_width / 2) + title_offset[0],
                            y=(window_width / 12) + title_offset[1])

        note_text = Text("Settings marked with '*' require a game restart.", "Pixellari", 26,
                         x=(window_width / 2) + note_text_offset[0],
                         y=(window_width / 8) + note_text_offset[1])

        back_text = Text("Back", "Pixellari", 26)
        back_button = Button(
            back_text,
            (window_width / 2 + back_offset[0], window_height / 2 + back_offset[1]),
            (128, 64)
        )
        back_button.set_action(self.back_action)

        save_text = Text("Save", "Pixellari", 26)
        save_button = Button(
            save_text,
            (window_width / 2 + save_offset[0], window_height / 2 + save_offset[1]),
            (128, 64)
        )
        save_button.set_action(self.save_action)

        self.add_element("Settings title", screen_title)

        self.add_element("Note Text", note_text)
        #self.add_element("Note 2 Text", note_2_text)

        self.add_element("Back button", back_button)
        self.add_element("Save button", save_button)
        self.add_element("Checkbox test", self.fullscreen_checkbox)


class CreditScreen(GUIScreen):

    def back_action(self):
        consts.LOGGER.debug("VALHALLA", "Back button pressed")
        consts.current_screen = consts.last_screen

    def __init__(self):
        super().__init__()

        window_width, window_height = pygame.display.get_surface().get_size()
        title_offset = (-42, 0)

        credit_title_offset = ((window_width / 2) - 94, (window_width / 8))
        credit_person_offset = ((window_width / 2), (window_width / 8) + 32)

        back_offset = (-64, 192)
        screen_title = Text("Credits", "Pixellari", 26,
                            x=(window_width / 2) + title_offset[0],
                            y=(window_width / 12) + title_offset[1])

        lead_programmer_title = Text("Lead Programmer", "Pixellari", 26,
                                     x=credit_title_offset[0],
                                     y=credit_title_offset[1])
        lead_programmer_credit = Text("Nathan Dow", "Pixellari", 26,
                                      x=credit_person_offset[0] + (lead_programmer_title.get_pos()[0] / 2) - (128 + 90),
                                      y=lead_programmer_title.get_pos()[1] + 32)

        programmer_title = Text("Programmers", "Pixellari", 26,
                                x=credit_title_offset[0] + 16,
                                y=credit_title_offset[1] * 2)
        programmer_credit = Text("Bartosz Swieszkowski", "Pixellari", 26,
                                 x=credit_person_offset[0] + (programmer_title.get_pos()[0] / 2) - (256 + 32),
                                 y=programmer_title.get_pos()[1] + 32)

        artist_title = Text("Artists", "Pixellari", 26,
                            x=credit_title_offset[0] + 64,
                            y=credit_title_offset[1] * 3)
        artist_credit_1 = Text("Bartosz Swieszkowski", "Pixellari", 26,
                               x=credit_person_offset[0] + (artist_title.get_pos()[0] / 2) - (256 + 56),
                               y=artist_title.get_pos()[1] + 32)
        artist_credit_2 = Text("Conner Hughes", "Pixellari", 26,
                               x=credit_person_offset[0] + (artist_title.get_pos()[0] / 2 - (256 + 8)),
                               y=artist_title.get_pos()[1] + 64)

        back_text = Text("Back", "Pixellari", 26)
        back_button = Button(
            back_text,
            (window_width / 2 + back_offset[0], window_height / 2 + back_offset[1]),
            (128, 64)
        )
        back_button.set_action(self.back_action)

        self.add_element("Credit title", screen_title)

        self.add_element("Lead Programmer title", lead_programmer_title)
        self.add_element("Lead Programmer credit", lead_programmer_credit)

        self.add_element("Programmer title", programmer_title)
        self.add_element("Programmer credit", programmer_credit)

        self.add_element("Artist title", artist_title)
        self.add_element("Artist credit 1", artist_credit_1)
        self.add_element("Artist credit 2", artist_credit_2)

        self.add_element("Back button", back_button)
