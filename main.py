"""
    Author:  Nathan Dow / Bitheral
    Created: 23/10/2020
"""
import pygame
import consts
import os
import util
import datetime

from gui import MainMenu, SplashScreen, DebugOverlay, GameOverlay, CreditScreen
from enums import Screens


def main():
    clock = pygame.time.Clock()
    pygame.init()
    pygame.font.init()
    consts.LOGGER.info("Pygame", "Pygame and its components have been initialized")

    window = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("The BeerZerker")
    consts.LOGGER.info("Pygame", "Created window")

    if os.path.exists("settings.json"):
        consts.LOGGER.info("Valhalla", "Settings file already exists; ")
        util.load_settings_file()
    else:
        consts.LOGGER.warning("Valhalla", "Settings file could not be found; Creating new settings file...")
        util.create_settings_file()

    displayCount = 0

    start_time = pygame.time.get_ticks()
    splash_screen = SplashScreen()
    main_menu = MainMenu()
    credit_screen = CreditScreen()
    debug_overlay = DebugOverlay()

    while consts.running:
        consts.MOUSE.update(pygame.mouse.get_pos())
        consts.LOGGER.launch_time = datetime.datetime.now()
        window.fill((0, 0, 0))
        temp_screen = consts.current_screen

        if consts.current_screen == Screens.SPLASHSCREEN:
            if pygame.time.get_ticks() < start_time + 3000:
                splash_screen.render()
            else:
                consts.current_screen = Screens.MAIN_MENU

        elif consts.current_screen == Screens.MAIN_MENU:
            main_menu.render()
            main_menu.handle_mouse_event()

        elif consts.current_screen == Screens.CREDITS:
            credit_screen.render()
            credit_screen.handle_mouse_event()

        elif consts.current_screen == Screens.GAME:
            game_overlay = GameOverlay()

            if consts.game.is_game_over():
                consts.current_screen = Screens.MAIN_MENU
                consts.game = None
            else:
                consts.game.update()
                game_overlay.render()


        elif consts.current_screen == Screens.QUIT:
            consts.LOGGER.info("VALHALLA", "QUIT Screen recognised. Quitting game...")
            util.quit_game()

        if consts.SETTINGS['DEBUG_OVERLAY']:
            debug_overlay.render()

        if not consts.current_screen == Screens.SPLASHSCREEN:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F12:
                        consts.LOGGER.debug("Valhalla", "Hiding debug overlay") if consts.SETTINGS[
                            'DEBUG_OVERLAY'] else consts.LOGGER.debug("Valhalla", "Showing debug overlay")
                        consts.SETTINGS['DEBUG_OVERLAY'] = not consts.SETTINGS['DEBUG_OVERLAY']

                if consts.game is not None:
                    pass

                if event.type == pygame.QUIT:
                    util.quit_game()

            if temp_screen != consts.current_screen:
                consts.LOGGER.info("Valhalla",
                                   f"Switched screens from {Screens(temp_screen).name} to {Screens(consts.current_screen).name}")

        pygame.display.update()
        clock.tick(120)


# try:
main()
# except Exception as e:
#    consts.LOGGER.error("VALHALLA", e)
