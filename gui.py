"""
    Author:  Nathan Dow / Bitheral
    Created: 16/10/2020
"""
import pygame


class Credit:
    def __init__(self, y, title, members):
        self.canvas = None
        self.y = y
        self.title = title
        self.members = members

        from consts import FONTS
        self.title_width, self.title_height = FONTS["Pixellari"].size(self.title)

    def draw(self):
        import util
        from consts import DIMENSIONS, FONTS
        util.render(self.canvas, util.text(self.title, FONTS['Pixellari']),
                    (DIMENSIONS['width'] / 2) - (self.title_width / 2), self.y)

        for index, member in enumerate(self.members):
            # print(member)
            member_width, member_height = FONTS["Pixellari"].size(member)
            if len(self.members) > 1:
                util.render(self.canvas, util.text(member, FONTS['Pixellari']),
                            (DIMENSIONS['width'] / 2) - (member_width / 2), (self.y + (member_height * (index + 1))))
            else:
                util.render(self.canvas, util.text(member, FONTS['Pixellari']),
                            (DIMENSIONS['width'] / 2) - (member_width / 2), ((self.y + 4) + self.title_height))


# Code obtained from https://www.pygame.org/wiki/Spritesheet
class Spritesheet(object):
    def __init__(self, filename):
        try:
            import util
            self.sheet = util.load_image(filename)
        except pygame.error as message:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(message)

    def convert(self):
        self.sheet = self.sheet.convert()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle):
        "Loads image from x,y,x+offset,y+offset"
        import util
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        util.render(image, self.sheet, 0, 0, rect)
        # image.blit(self.sheet, (0, 0), rect)
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


"""
   ____ _   _ ___   _____ _                           _
  / ___| | | |_ _| | ____| | ___ _ __ ___   ___ _ __ | |_ ___
 | |  _| | | || |  |  _| | |/ _ \ '_ ` _ \ / _ \ '_ \| __/ __|
 | |_| | |_| || |  | |___| |  __/ | | | | |  __/ | | | |_\__ \
  \____|\___/|___| |_____|_|\___|_| |_| |_|\___|_| |_|\__|___/

"""


class Button:
    # Initializes and assigns parameters to Button instance
    def __init__(self, x, y, width, height, text, destination):
        self.font = None
        self.color = (1, 1, 1)
        self.position = {
            'x': x,
            'y': y,
        }
        self.size = {
            'width': width,
            'height': height
        }
        self.text = text
        self.canvas = None
        self.destination = destination

    # Returns the area of the button
    def get_area(self):
        return {
            'x': self.position['x'],
            'y': self.position['y'],
            'width': self.size['width'],
            'height': self.size['height']
        }

    # Returns true or false depending if mouse is in the button area
    def can_click(self):
        mouse = pygame.mouse.get_pos()
        return (self.get_area()['x'] < mouse[0] < self.get_area()['x'] + self.get_area()['width']) and (
                self.get_area()['y'] < mouse[1] < self.get_area()['y'] + self.get_area()['height'])

    def click(self, function):
        if self.can_click():
            function

    # Draws the button with the button texture and button text
    def draw(self):
        from consts import TEXTURES, DIMENSIONS
        from util import render, text
        render(self.canvas, pygame.transform.scale(TEXTURES['button'], (self.size['width'], self.size['height'])),
               int(self.position['x']), int(self.position['y']))

        text_width, text_height = self.font.size(self.text)
        render(self.canvas, text(self.text, self.font), (self.position['x'] + (self.size['width'] / 2)) - (text_width / 2),
               (self.position['y'] + (self.size['height'] / 2)) - (text_height / 2) + 4)


class Checkbox:

    # Initializes and assigns parameters to Button instance
    def __init__(self, x, y, width, height, text, state):
        from consts import FONTS
        self.text = text

        self.position = {
            'x': x,
            'y': y,
        }
        self.size = {
            'width': 32,
            'height': height
        }
        self.canvas = None
        self.state = state

    # Returns the area of the button
    def get_area(self):
        return {
            'x': self.position['x'],
            'y': self.position['y'],
            'width': self.size['width'],
            'height': self.size['height']
        }

    # Returns true or false depending if mouse is in the button area
    def can_click(self):
        mouse = pygame.mouse.get_pos()
        return (self.get_area()['x'] < mouse[0] < self.get_area()['x'] + self.get_area()['width']) and (
                self.get_area()['y'] < mouse[1] < self.get_area()['y'] + self.get_area()['height'])

    # Draws the button with the button texture and button text
    def draw(self):
        from consts import TEXTURES, FONTS
        from util import render, text

        checkbox_on = TEXTURES['checkbox'].image_at((0, 0, 32, 32))
        checkbox_off = TEXTURES['checkbox'].image_at((0, 32, 32, 64))
        pygame.draw.rect(self.canvas, (255, 0, 0),
                         (self.position['x'], self.position['y'], self.size['width'], self.size['height']))

        render(self.canvas, checkbox_on if self.state else checkbox_off, int(self.position['x']),
               int(self.position['y']))
        render(self.canvas, text(f"{self.text}", FONTS['Pixellari']), self.position['x'] + 40,
               self.position['y'] + (self.size['height'] / 2 - (FONTS['Pixellari'].size(self.text)[1] / 2)) + 2)
