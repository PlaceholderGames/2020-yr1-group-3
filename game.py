"""
    Author:  Nathan Dow / Bitheral
    Created: 27/10/2020
"""

import pygame
import cmath

import consts
from enums import Direction, Scenes
from util import bind, Spritesheet, lerp, Image

from random import randint, random


class Entity(object):

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.health = 100
        self.screen = pygame.display.get_surface()
        self.rect = pygame.rect.Rect((self.screen.get_size()[0] / 2, self.screen.get_size()[1] / 2, 32, 32))
        self.rect_colour = (255, 255, 255)
        self.speed = 1.4

    def get_health(self):
        return self.health

    def take_damage(self, damage):
        self.health -= damage

    def heal(self, healing):
        self.health += healing

    def draw(self):
        pygame.draw.rect(self.screen, self.rect_colour, self.rect)

    def update(self):
        self.clock.tick(120)
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y <= 0:
            self.rect.y = 0

        if self.rect.x + 32 >= self.screen.get_size()[0]:
            self.rect.x = self.screen.get_size()[0] - 32
        if self.rect.y + 32 >= self.screen.get_size()[1]:
            self.rect.y = self.screen.get_size()[1] - 32

        if self.get_health() < 100:
            if int(consts.time_since_start / 1000) % 2 == 0:
                self.heal(0.01)

    def collides(self, other):
        if self is not other:
            return self.rect.colliderect(other.rect)


# Uses player as a rectangle
# https://stackoverflow.com/questions/32061507/moving-a-rectangle-in-pygame
class Player(Entity):
    def __init__(self):
        super().__init__()
        self.items = []
        self.attacking = 0
        self.atkr = pygame.rect.Rect((self.screen.get_size()[0] / 2, self.screen.get_size()[1] / 2, 16, 32))
        self.facing_direction = Direction.RIGHT
        self.attack_direction = Direction.RIGHT
        self.drunkenness = 100
        self.speed = 1.6
        self.rect_colour = (81, 81, 81)

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.facing_direction = Direction.LEFT
            self.rect.move_ip(-self.speed, 0)
            self.atkr.move_ip(-self.speed, 0)
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.facing_direction = Direction.RIGHT
            self.rect.move_ip(self.speed, 0)
            self.atkr.move_ip(self.speed, 0)
        if key[pygame.K_UP] or key[pygame.K_w]:
            self.facing_direction = Direction.UP
            self.rect.move_ip(0, -self.speed)
            self.atkr.move_ip(0, -self.speed)
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            self.facing_direction = Direction.DOWN
            self.rect.move_ip(0, self.speed)
            self.atkr.move_ip(0, self.speed)

    def handle_mouse(self):
        mouse = pygame.mouse.get_pos()

        if pygame.event.get(pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pressed()[0]:
            self.attacking = 50

    def draw(self):
        super(Player, self).draw()
        if self.attacking != 0:
            pygame.draw.rect(self.screen, (56, 56, 56), self.atkr)

    def update(self):
        super(Player, self).update()
        self.attack_rects = {
            "UP": pygame.rect.Rect((self.rect.x, self.rect.y - self.rect.height, self.rect.width, self.rect.height)),
            "RIGHT": pygame.rect.Rect((self.rect.x + self.rect.width, self.rect.y, self.rect.width, self.rect.height)),
            "DOWN": pygame.rect.Rect((self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height)),
            "LEFT": pygame.rect.Rect((self.rect.x - self.rect.width, self.rect.y, self.rect.width, self.rect.height)),
        }

        if self.attacking != 0:
            self.attacking -= 1
        elif self.attacking < 0:
            self.attacking = 0

        self.atkr = self.attack_rects[self.facing_direction.name]
        self.drunkenness -= 0.05

        if self.drunkenness > 100:
            self.drunkenness = 100

        if self.drunkenness < 90:
            for index, item in enumerate(self.items):
                if type(item) == Bottle:
                    if consts.SETTINGS["HUMAN_SOUNDS"]["VALUE"]:
                        pygame.mixer.Sound("assets/audio/sounds/game/drink_use.ogg").play()
                    self.items.pop(index)
                    self.drunkenness += 20

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        for index, item_entity in enumerate(self.items):
            if item_entity == item:
                self.items.pop(index)

    def get_items_by_type(self, classType):
        item_list = []
        for item in self.items:
            if type(item) == classType:
                item_list.append(item)
        return item_list

class Enemy(Entity):
    def __init__(self):
        super().__init__()
        # Limit enemy spawn to window size
        self.rect = pygame.rect.Rect(
            (
                randint(0, self.screen.get_size()[0] - 32),
                randint(0, self.screen.get_size()[1] - 32),
                32,
                32
            )
        )
        self.rect_colour = (255, 0, 0)
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
        super(Enemy, self).draw()
        healthPercent = self.health
        if self.hurting != 0:
            # Health bar - background
            pygame.draw.rect(self.screen, (24, 102, 19), (self.rect.x, self.rect.y - 32, 32, 16))
            pygame.draw.rect(self.screen, (58, 196, 51),
                             (self.rect.x, self.rect.y - 32, bind(healthPercent, 0, 100, 0, 32, True), 16))
        # pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

    def update(self):
        super(Enemy, self).update()
        if self.hurting != 0:
            # consts.LOGGER.debug("VALHALLA", f"Enemy health: {self.health}")
            self.hurting -= 1


class DroppedItem(Entity):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.rect = pygame.rect.Rect((
            randint(0, self.screen.get_size()[0] - 32),
            randint(0, self.screen.get_size()[1] - 32),
            32, 32
        ))
        self.rect_colour = (0, 255, 0)

    def draw(self):
        super(DroppedItem, self).draw()

    def picked_up(self, player):
        return player.rect.colliderect(self.rect)


class Bottle(DroppedItem):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.rect = pygame.rect.Rect((
            randint(0, self.screen.get_size()[0] - 32),
            randint(0, self.screen.get_size()[1] - 32),
            32, 32
        ))
        self.rect_colour = (0, 255, 0)

        self.sprite = Image("assets/textures/sprites/beer_bottle.png", transparency=True)

    def draw(self):
        # super(Bottle, self).draw()
        self.screen.blit(self.sprite.render(), (self.rect.x, self.rect.y))


class Collidable(object):
    def __init__(self, rect, inverse=False, show_collider=True):
        self.draw_rect = pygame.rect.Rect(rect)
        self.inverse = inverse
        self.show = show_collider
        self.collisionThickness = 2
        self.collideEdges = {
            "TOP": pygame.rect.Rect((self.draw_rect.x + self.collisionThickness, self.draw_rect.y,
                                     self.draw_rect.width - self.collisionThickness, self.collisionThickness)),
            "RIGHT": pygame.rect.Rect((self.draw_rect.x + (self.draw_rect.width - self.collisionThickness),
                                       self.draw_rect.y + self.collisionThickness,
                                       self.collisionThickness, self.draw_rect.height - self.collisionThickness)),
            "BOTTOM": pygame.rect.Rect((self.draw_rect.x + self.collisionThickness,
                                        self.draw_rect.y + (self.draw_rect.height - self.collisionThickness),
                                        self.draw_rect.width - self.collisionThickness, self.collisionThickness)),
            "LEFT": pygame.rect.Rect((self.draw_rect.x, self.draw_rect.y + self.collisionThickness,
                                      self.collisionThickness, self.draw_rect.height - self.collisionThickness)),
            "TOP_LEFT": pygame.rect.Rect((self.draw_rect.x, self.draw_rect.y,
                                          self.collisionThickness, self.collisionThickness)),
            "TOP_RIGHT": pygame.rect.Rect(
                (self.draw_rect.x + (self.draw_rect.width - self.collisionThickness), self.draw_rect.y,
                 self.collisionThickness, self.collisionThickness)),
            "BOTTOM_LEFT": pygame.rect.Rect(
                (self.draw_rect.x, self.draw_rect.y + (self.draw_rect.height - self.collisionThickness),
                 self.collisionThickness, self.collisionThickness)),
            "BOTTOM_RIGHT": pygame.rect.Rect((self.draw_rect.x + (self.draw_rect.width - self.collisionThickness),
                                              self.draw_rect.y + (self.draw_rect.height - self.collisionThickness),
                                              self.collisionThickness, self.collisionThickness))

        }

    def update(self, entity):

        for edge in self.collideEdges:
            collisionEdge = self.collideEdges[edge]
            if collisionEdge.colliderect(entity.rect):
                if edge == "TOP":
                    if not self.inverse:
                        entity.rect.y = self.draw_rect.y - entity.rect.height
                    else:
                        entity.rect.y = self.draw_rect.y + self.collisionThickness
                elif edge == "RIGHT":
                    if not self.inverse:
                        entity.rect.x = self.draw_rect.x + self.draw_rect.width
                    else:
                        entity.rect.x = (self.draw_rect.x + self.draw_rect.width) - (
                                entity.rect.width + self.collisionThickness)
                elif edge == "BOTTOM":
                    if not self.inverse:
                        entity.rect.y = self.draw_rect.y + self.draw_rect.height
                    else:
                        entity.rect.y = ((
                                                 self.draw_rect.y + self.draw_rect.height) - self.collisionThickness) - entity.rect.height
                elif edge == "LEFT":
                    if not self.inverse:
                        entity.rect.x = self.draw_rect.x - entity.rect.width
                    else:
                        entity.rect.x = self.draw_rect.x + self.collisionThickness
                elif edge == "TOP_LEFT":
                    entity.rect.x = self.draw_rect.x - entity.rect.width
                    entity.rect.y = self.draw_rect.y - entity.rect.height
                elif edge == "TOP_RIGHT":
                    entity.rect.x = self.draw_rect.x + self.draw_rect.width
                    entity.rect.y = self.draw_rect.y - entity.rect.height
                elif edge == "BOTTOM_LEFT":
                    entity.rect.x = self.draw_rect.x - entity.rect.width
                    entity.rect.y = self.draw_rect.y + self.draw_rect.height
                elif edge == "BOTTOM_RIGHT":
                    entity.rect.x = self.draw_rect.x + entity.rect.width
                    entity.rect.y = self.draw_rect.y + self.draw_rect.height

    def is_colliding(self, entity):
        return self.draw_rect.colliderect(entity.rect)

    def draw(self):
        surface = pygame.display.get_surface()
        if self.show:
            pygame.draw.rect(surface, (0, 0, 255), self.draw_rect)
        if consts.SETTINGS['DEBUG_OVERLAY']:
            for edge in self.collideEdges:
                collisonEdge = self.collideEdges[edge]
                pygame.draw.rect(surface, (255, 127, 127), collisonEdge)


class Portal(object):

    def __init__(self, rect, target_scene, target_pos):
        self.rect = pygame.rect.Rect(rect)
        self.target_scene = target_scene
        self.target_coords = target_pos

    def update(self, player):
        if self.rect.colliderect(player.rect):
            consts.current_scene = self.target_scene
            player.rect.x, player.rect.y = self.target_coords

    def render(self):
        surface = pygame.display.get_surface()
        pygame.draw.rect(surface, (128, 0, 255), self.rect)


class Scene(object):

    def __init__(self, entities, collisions, portals, background_img=None):
        self.entities = entities
        self.collisions = collisions
        self.portals = portals
        self.last_player_pos = (0, 0)
        self.background_image = background_img
        if self.background_image is not None:
            self.background = pygame.transform.scale(self.background_image.render(),
                                                     pygame.display.get_surface().get_size())

    def remaining_enemies(self):
        return len(self.entities["ENEMY"])

    def get_entities(self):
        return self.entities

    def get_entities_by_type(self, type):
        return self.entities[type]

    def update(self, player):
        self.last_player_pos = (player.rect.x, player.rect.y)

        for items in self.entities["ITEMS"]:
            for collision in self.collisions:
                if items.rect.colliderect(collision.draw_rect):
                    items.rect.x = randint(0, pygame.display.get_surface().get_size()[0])
                    items.rect.y = randint(0, pygame.display.get_surface().get_size()[1])

        for portal in self.portals:
            portal.update(player)

        for entityType in self.entities:
            for index, entity in enumerate(self.entities[entityType]):
                for collision in self.collisions:
                    if type(entity) == Enemy or type(entity) == DroppedItem or type(entity) == Bottle:
                        collision.update(entity)
                    collision.update(player)

                if type(entity) == Enemy:
                    entity.follow(player)
                    if entity.collides(player) or player.collides(entity):
                        player.take_damage(0.1)

                    if player.attacking != 0:
                        if entity.rect.colliderect(player.atkr) or (
                                entity.rect.colliderect(player.rect) and entity.rect.colliderect(player.atkr)):
                            entity.hurting = 100
                            entity.health -= 0.5

                    if entity.health <= 0:
                        self.entities["ENEMY"].pop(index)

                if type(entity) == DroppedItem or type(entity) == Bottle:
                    if entity.picked_up(player):
                        pygame.mixer.Sound("assets/audio/sounds/game/bottle_pickup.ogg").play()
                        player.add_item(entity)
                        self.entities["ITEMS"].pop(index)

                if type(entity) == Enemy or type(entity) == DroppedItem or type(entity) == Bottle:
                    entity.update()

    def render(self):
        for portal in self.portals:
            portal.render()

        for collision in self.collisions:
            collision.draw()

        for item in self.entities["ITEMS"]:
            if type(item) == DroppedItem or type(item) == Bottle:
                item.draw()

        for enemy in self.entities["ENEMY"]:
            if type(enemy) == Enemy:
                enemy.draw()


class Game:

    def __init__(self):
        self.player = Player()
        consts.current_scene = Scenes.TUTORIAL

        self.scenes = [
            Scene(
                {
                    "ENEMY": [Enemy(), Enemy()],
                    "ITEMS": [Bottle(), Bottle(), Bottle(), Bottle(), Bottle(), Bottle()],
                    "PEDESTRIAN": []},
                [
                    # Border wall
                    Collidable((0, 0, 320, 10), show_collider=False),
                    Collidable((0, 0, 20, pygame.display.get_surface().get_size()[1]), show_collider=False),
                    Collidable((0, pygame.display.get_surface().get_size()[1] - 20, 372, 20), show_collider=False),
                    Collidable((470, pygame.display.get_surface().get_size()[1] - 20, 330, 20), show_collider=False),
                    Collidable((pygame.display.get_surface().get_size()[0] - 28, 192, 28, 408), show_collider=False),
                    Collidable((pygame.display.get_surface().get_size()[0] - 80, 192, 80, 18), show_collider=False),
                    Collidable((pygame.display.get_surface().get_size()[0] - 280, 192, 100, 18), show_collider=False),
                    Collidable((pygame.display.get_surface().get_size()[0] - 280, 0, 16, 210), show_collider=False),
                    Collidable((418, 0, 115, 10), show_collider=False),

                    # Buildings
                    Collidable((428, 9, 92, 202)),
                    Collidable((340, 89, 60, 118))
                ],
                [
                    Portal((320, 0, 98, 8), Scenes.LEVEL_1, (400, pygame.display.get_surface().get_size()[1] - 40))
                ],
                Image("assets/textures/scenes/tutorial.png", transparency=False)
            ),
            Scene(
                {"ENEMY": [Enemy()], "ITEMS": [DroppedItem()], "PEDESTRIAN": []},
                [Collidable((428, 9, 92, 202))],
                [Portal((372, pygame.display.get_surface().get_size()[1] - 8, 98, 8), Scenes.TUTORIAL,
                        (360, 8))],
                Image("assets/textures/scenes/tutorial.png", transparency=False)
            )
        ]

        self.game_over = False
        self.paused = False

    def get_player(self):
        return self.player

    def is_paused(self):
        return self.paused

    def pause(self, pause):
        self.paused = pause

    def is_game_over(self):
        return self.game_over

    def render(self):
        surface = pygame.display.get_surface()

        if self.scenes[consts.current_scene.value].background_image is not None:
            surface.blit(self.scenes[consts.current_scene.value].background, (0, 0))
        self.player.draw()
        self.scenes[consts.current_scene.value].render()

    def update(self):
        consts.time_since_start = pygame.time.get_ticks() - consts.start_time
        currentScene = self.scenes[consts.current_scene.value]

        self.scenes[consts.current_scene.value].update(self.player)

        if self.player.health <= 0 or currentScene.remaining_enemies() == 0 or self.player.drunkenness <= 0:
            self.game_over = True
            consts.LOGGER.info("VALHALLA", "Game over! Going back to MAIN_MENU")

        self.player.update()
        self.player.handle_keys()
        self.player.handle_mouse()
