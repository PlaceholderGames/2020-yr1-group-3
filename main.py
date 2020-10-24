"""
    Author:  Nathan Dow / Bitheral
    Created: 23/10/2020
"""
import pygame
import consts
import os
import util

from gui import MainMenu, SplashScreen
from enums import Screens

pygame.init()
pygame.font.init()
consts.LOGGER.info("Pygame", "Pygame and its components have been initialized")

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("The BeerZerker")
consts.LOGGER.info("Pygame", "Created window")

if os.path.exists("settings.json"):
    consts.LOGGER.info("Valhalla", "Settings file already exists; Loading settings file...")
    util.load_settings_file()
else:
    consts.LOGGER.warning("Valhalla", "Settings file could not be found; Creating new settings file...")
    util.create_settings_file()

running = True
displayCount = 0

start_time = pygame.time.get_ticks()

splash_screen = SplashScreen()

while running:
    window.fill((0, 0, 0))
    temp_screen = consts.current_screen

    if consts.current_screen == Screens.SPLASHSCREEN.value:
        if pygame.time.get_ticks() < start_time + 3000:
            splash_screen.render()
        else:
            consts.current_screen = Screens.MAIN_MENU.value

    elif consts.current_screen == Screens.MAIN_MENU.value:
        main_menu = MainMenu()
        main_menu.render()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            consts.LOGGER.info("Valhalla", "Stopping...")
            consts.LOGGER.stop()
            quit()

        if event.type != 4:
            consts.LOGGER.info("Pygame", f"{str(pygame.event.event_name(event.type))} Event received.")

    if temp_screen != consts.current_screen:
        consts.LOGGER.info("Valhalla",
                           f"Switched screens from {Screens(temp_screen).name} to {Screens(consts.current_screen).name}")
    pygame.display.update()

consts.LOGGER.stop()
quit()
