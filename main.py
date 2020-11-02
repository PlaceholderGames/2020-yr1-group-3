"""
    Author:  Nathan Dow / Bitheral
    Created: 23/10/2020
"""
import pygame
import consts
import os
import util
import datetime
import ctypes

from gui import MainMenu, SplashScreen, DebugOverlay, GameOverlay, CreditScreen, PauseOverlay, SettingScreen
from enums import Screens

def main():
    clock = pygame.time.Clock()
    pygame.init()
    pygame.font.init()
    consts.LOGGER.info("Pygame", "Pygame and its components have been initialized")

    if os.path.exists("settings.json"):
        consts.LOGGER.info("Valhalla", "Settings file already exists; ")
        util.load_settings_file()
    else:
        consts.LOGGER.warning("Valhalla", "Settings file could not be found; Creating new settings file...")
        util.create_settings_file()

    if consts.SETTINGS['FULLSCREEN']:
        window = pygame.display.set_mode((ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)), pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode(
            (consts.SETTINGS['RESOLUTION']['WIDTH'], consts.SETTINGS['RESOLUTION']['HEIGHT']))
    pygame.display.set_caption("The BeerZerker")
    consts.LOGGER.info("Pygame", "Created window")

    displayCount = 0

    start_time = pygame.time.get_ticks()
    splash_screen = SplashScreen()
    main_menu = MainMenu()
    settings_screen = SettingScreen()
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
        elif consts.current_screen == Screens.SETTINGS:
            settings_screen.render()
            settings_screen.handle_mouse_event()
        elif consts.current_screen == Screens.CREDITS:
            credit_screen.render()
            credit_screen.handle_mouse_event()
        elif consts.current_screen == Screens.GAME:
            game_overlay = GameOverlay()
            game_pause = PauseOverlay()

            if consts.game.is_game_over():
                if consts.game.get_enemies() == 0:
                    consts.LOGGER.info("VALHALLA", "You won!")
                else:
                    consts.LOGGER.info("VALHALLA", "You lost!")

                consts.current_screen = Screens.MAIN_MENU
                consts.game = None
            else:
                consts.game.render()

                if not consts.game.paused:
                    consts.game.update()
                else:
                    game_pause.handle_mouse_event()
                    game_pause.render()
                if consts.SETTINGS['DEBUG_OVERLAY']:
                    debug_overlay.render()
                else:
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
                        if consts.SETTINGS['DEBUG_OVERLAY']:
                            consts.LOGGER.debug("Valhalla", "Hiding debug overlay")
                        else:
                            consts.LOGGER.debug("Valhalla", "Showing debug overlay")
                        consts.SETTINGS['DEBUG_OVERLAY'] = not consts.SETTINGS['DEBUG_OVERLAY']

                    if consts.game is not None:
                        if event.key == pygame.K_ESCAPE:
                            consts.game.pause(not consts.game.paused)
                            #pygame.mouse.set_visible(consts.game.paused)
                            #pygame.mouse.set_pos(int(window.get_size()[0] / 2), int(window.get_size()[1] / 2))

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
