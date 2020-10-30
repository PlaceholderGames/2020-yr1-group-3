"""
    Author:  Nathan Dow / Bitheral
    Created: 27/10/2020
"""

import pygame
import math
from pygame.locals import *
from consts import LOGGER
from enums import Direction
from util import bind

from random import randint, random

"""
class Player(pygame.Rect):

    def __init__(self):
        super().__init__((pygame.display.get_surface().get_size()[0] / 2, pygame.display.get_surface().get_size()[1] / 2), (32, 32))
        window_width, window_height = pygame.display.get_surface().get_size()
        self.x = window_width / 2
        self.y = window_height / 2
        self.speed = 1.4
        self.sprinting = False
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.attacking = False

    def move_player(self):
        if self.move_up:
            if self.sprinting:
                self.y -= (self.speed * 4)
            else:
                self.y -= self.speed

        if self.move_down:
            if self.sprinting:
                self.y += (self.speed * 4)
            else:
                self.y += self.speed

        if self.move_left:
            if self.sprinting:
                self.x -= (self.speed * 4)
            else:
                self.x -= self.speed

        if self.move_right:
            if self.sprinting:
                self.x += (self.speed * 4)
            else:
                self.x += self.speed

        if self.x + 16 > pygame.display.get_surface().get_size()[0]:
            self.x = pygame.display.get_surface().get_size()[0] - 16
        elif self.x - 16 < 0:
            self.x = 16

        if self.y + 16 > pygame.display.get_surface().get_size()[1]:
            self.y = pygame.display.get_surface().get_size()[1] - 16
        elif self.y - 16 < 0:
            self.y = 16

    def draw(self):
        if self.attacking:
            pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), (self.x + 16, self.y - 4, 32, 8))
        pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), (self.x - 16, self.y - 16, 32, 32))
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), (self.x - 2, self.y - 2, 4, 4))

"""


# Uses player as a rectangle
# https://stackoverflow.com/questions/32061507/moving-a-rectangle-in-pygame
class Player(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.health = 100
        self.attacking = 0
        self.rect = pygame.rect.Rect((self.screen.get_size()[0] / 2, self.screen.get_size()[1] / 2, 32, 32))
        self.atkr = pygame.rect.Rect((self.screen.get_size()[0] / 2, self.screen.get_size()[1] / 2, 16, 32))
        self.direction = Direction.RIGHT
        self.speed = 1.4

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.direction = Direction.LEFT
            self.rect.move_ip(-self.speed, 0)
            self.atkr.move_ip(-self.speed, 0)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.direction = Direction.RIGHT
            self.rect.move_ip(self.speed, 0)
            self.atkr.move_ip(self.speed, 0)
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.direction = Direction.UP
            self.rect.move_ip(0, -self.speed)
            self.atkr.move_ip(0, -self.speed)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.direction = Direction.DOWN
            self.rect.move_ip(0, self.speed)
            self.atkr.move_ip(0, self.speed)

    def handle_mouse(self):
        mouse = pygame.mouse.get_pressed()
        left = 0
        middle = 1
        right = 2

        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            self.attacking = 50
        # if mouse[left] == 1:
        #    self.attacking = True
        # else:
        #    self.attacking = False

    def draw(self):
        if self.attacking != 0:
            pygame.draw.rect(self.screen, (154, 154, 154), self.atkr)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)

    def update(self):
        if self.attacking != 0:
            self.attacking -= 1
        elif self.attacking < 0:
            self.attacking = 0

        if self.direction == Direction.RIGHT:
            self.atkr = pygame.rect.Rect((self.rect.x + 32, self.rect.y, 32, 32))
        elif self.direction == Direction.LEFT:
            self.atkr = pygame.rect.Rect((self.rect.x, self.rect.y, -32, 32))
        elif self.direction == Direction.UP:
            self.atkr = pygame.rect.Rect((self.rect.x, self.rect.y, 32, -32))
        elif self.direction == Direction.DOWN:
            self.atkr = pygame.rect.Rect((self.rect.x, self.rect.y + 32, 32, 32))

        if pygame.time.get_ticks() % 2000:
            if self.health < 100:
                self.health += 0.05


class Pedestrian(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.rect = pygame.rect.Rect(
            (randint(0, self.screen.get_size()[0]), randint(0, self.screen.get_size()[1]), 32, 32))

    def walk(self):
        pass
        # TODO: Implement a simple walking system for pedestrians

    def draw(self):
        pygame.draw.rect(self.screen, (0, 127, 127), self.rect)


class Enemy(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.health = 100
        self.rect = pygame.rect.Rect(
            (randint(0, self.screen.get_size()[0]), randint(0, self.screen.get_size()[1]), 32, 32))
        self.speed = 1
        self.hurting = 0

    def follow(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        if abs(dx) <= self.screen.get_size()[0] and abs(dy) <= self.screen.get_size()[1]:
            move_x = abs(dx) > abs(dy)
            if abs(dx) > self.speed and abs(dy) > self.speed:
                move_x = random() < 0.5
            if move_x:
                self.rect.x += min(dx, self.speed) if dx > 0 else max(dx, -self.speed)
            else:
                self.rect.y += min(dy, self.speed) if dy > 0 else max(dy, -self.speed)

    def draw(self):
        if self.hurting != 0:
            # Health bar - background
            pygame.draw.rect(self.screen, (24, 102, 19), (self.rect.x, self.rect.y - 32, 32, 16))
            pygame.draw.rect(self.screen, (58, 196, 51),
                             (self.rect.x, self.rect.y - 32, bind(self.health, 0, 100, 0, 32, True), 16))
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

    def update(self):
        if self.hurting != 0:
            self.hurting -= 1


class Game:

    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.pedestrians = []
        self.game_over = False
        self.paused = False
        pygame.mouse.set_visible(False)

        for enemy in range(1):
            self.enemies.append(Enemy())

        # TODO: See Pedestrian#walk()
        # for pedestrian in range(randint(6, 16)):
        #    self.pedestrians.append(Pedestrian())

    def get_player(self):
        return self.player

    def get_enemies(self):
        return len(self.enemies)

    def is_paused(self):
        return self.paused

    def pause(self, pause):
        self.paused = pause

    def is_game_over(self):
        return self.game_over

    def render(self):
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()

    def update(self):
        pygame.mouse.set_pos(0, 0)
        if self.player.health <= 0 or len(self.enemies) == 0:
            self.game_over = True
            LOGGER.info("VALHALLA", "Game over! Going back to MAIN_MENU")
            pygame.mouse.set_visible(True)

        self.player.update()
        self.player.handle_keys()
        self.player.handle_mouse()

        for index, enemy in enumerate(self.enemies):
            enemy.follow(self.player)
            enemy.update()
            if enemy.rect.colliderect(self.player.rect):
                self.player.health -= 0.1

            if enemy.rect.colliderect(self.player.atkr) or (
                    enemy.rect.colliderect(self.player.rect) and enemy.rect.colliderect(self.player.atkr)):
                enemy.hurting = 100
                enemy.health -= 0.5

            if enemy.health <= 0:
                self.enemies.pop(index)

        # TODO: See Pedestrian#walk()
        # for pedestrian in self.pedestrians:
        #    pedestrian.time_alive += 1
        #    pedestrian.walk()
        #    pedestrian.draw()
