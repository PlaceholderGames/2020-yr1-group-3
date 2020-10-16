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


def text(_text, font, color=(255, 255, 255)):
    return font.render(_text, True, color)


def render(canvas, _render, x, y):
    canvas.blit(_render, (x, y))


def fade_in(screen, canvas, time, render):
    for alpha in range(255, 0, -1):
        canvas.set_alpha(alpha)
        render()
        screen.blit(canvas, (0, 0))
        pygame.display.update()
        pygame.time.delay(time)


def fade_out(screen, canvas, time, render):
    for alpha in range(0, 255):
        canvas.fill((0, 0, 0))
        canvas.set_alpha(alpha)
        render()
        screen.blit(canvas, (0, 0))
        pygame.display.update()
        pygame.time.delay(time)


class Button:
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

    def get_area(self):
        return {
            'x': self.position['x'],
            'y': self.position['y'],
            'width': self.size['width'],
            'height': self.size['height']
        }

    def can_click(self):
        mouse = pygame.mouse.get_pos()
        return (self.get_area()['x'] < mouse[0] < self.get_area()['x'] + self.get_area()['width']) and (
                self.get_area()['y'] < mouse[1] < self.get_area()['y'] + self.get_area()['height'])

    def draw(self):
        from consts import TEXTURES
        render(self.canvas, pygame.transform.scale(TEXTURES['button'], (self.size['width'], self.size['height'])), int(self.position['x']), int(self.position['y']))
        render(self.canvas, text(self.text, self.font), self.position['x'], (self.position['y'] + (self.size['height'] / 2)))
        # pygame.draw.rect(self.canvas, (255, 255, 255), (self.position['x'], self.position['y'], self.size['width'], self.size['height']))


