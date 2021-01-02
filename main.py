"""
    Author:  Nathan Dow / Bitheral
    Created: 23/10/2020
"""
import pygame
import consts
import os
import util
import datetime
import platform
import ctypes

from gui import MainMenu, SplashScreen, DebugOverlay, GameOverlay, CreditScreen, PauseOverlay, SettingScreen, \
    GameOverOverlay, DisturbingSoundScreen
from enums import Screens

def main():

    # Setup pygame
    consts.clock = pygame.time.Clock()
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    consts.LOGGER.info("Pygame", "Pygame and its components have been initialized")

    # Check for settings file before initializing Pygame window
    if os.path.exists("settings.json"):
        consts.LOGGER.info("Valhalla", "Settings file already exists; ")
        util.load_settings_file()
    else:
        consts.LOGGER.warning("Valhalla", "Settings file could not be found; Creating new settings file...")
        util.create_settings_file()
        util.save_to_settings_file()

    if platform.system() == 'Linux':
        displays = os.popen('xrandr | grep " connected primary"').read()
        displays_str = str(displays)
        resolution = displays_str.split(" ")[3][:-4]
        resolution_tuple = tuple(int(res) for res in resolution.split('x'))
    elif platform.system("Windows"):
        resolution_tuple = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))


    # Checks if fullscreen setting is true
    if consts.SETTINGS['FULLSCREEN']:
        # Makes window fullscreen to screen resolution if so
        # Windows
        window = pygame.display.set_mode(resolution_tuple, pygame.FULLSCREEN)

        # linux
    else:

        # Makes window to specified screen resolution in settings file
        window = pygame.display.set_mode(
            (consts.SETTINGS['RESOLUTION']['WIDTH'], consts.SETTINGS['RESOLUTION']['HEIGHT']))

    # Creates window
    pygame.display.set_caption("The BeerZerker")
    pygame.display.set_icon(util.Image("assets/textures/sprites/beer_bottle.png").render())
    consts.LOGGER.info("Pygame", "Created window")

    start_time = pygame.time.get_ticks()

    #
    # Initialize all GUIScreens
    splash_screen = SplashScreen()
    main_menu = MainMenu()
    settings_screen = SettingScreen()
    credit_screen = CreditScreen()
    debug_overlay = DebugOverlay()
    sound_warning_screen = DisturbingSoundScreen()

    while consts.running:
        if consts.game is not None:
            game_result = GameOverOverlay()
            game_overlay = GameOverlay()
            game_pause = PauseOverlay()

        # Probably unneccessary to have a Mouse constant, just use pygame.mouse
        consts.MOUSE.update(pygame.mouse.get_pos())
        consts.LOGGER.launch_time = datetime.datetime.now()

        # Reset the screen everyframe so that we
        # don't have a transparent background each frame refresh
        window.fill((0, 0, 0))

        # Stores the current screen in a temporary value
        # to report to logger when the screen has changed
        temp_screen = consts.current_screen

        # Render splashscreen
        #
        if consts.current_screen == Screens.SPLASHSCREEN:
            if not splash_screen.loaded():
                splash_screen.render()
            else:
                consts.current_screen = Screens.MAIN_MENU

        # Render Main menu
        #
        elif consts.current_screen == Screens.MAIN_MENU:
            main_menu.render()
            main_menu.handle_mouse_event()

        # Render Settings screen
        #
        elif consts.current_screen == Screens.SETTINGS:
            settings_screen.render()
            settings_screen.handle_mouse_event()

        # Render Credits screen
        #
        elif consts.current_screen == Screens.CREDITS:
            credit_screen.render()
            credit_screen.handle_mouse_event()

        # Render game screen
        #
        elif consts.current_screen == Screens.GAME:

            # Initialize game overlays

            # Check if game has ended
            if consts.game.is_game_over():

                consts.game.render()
                game_result.handle_mouse_event()
                game_result.render()
            else:

                # Render game whilst the game hasn't ended
                consts.game.render()

                if consts.SETTINGS['DEBUG_OVERLAY']:
                    debug_overlay.render()
                else:
                    game_overlay.render()

                if not consts.game.paused:
                    consts.game.update()
                else:
                    game_pause.handle_mouse_event()
                    game_pause.render()

        # Quit game if player screen reaches Screens.QUIT
        #
        elif consts.current_screen == Screens.QUIT:
            if not pygame.mixer.get_busy():
                consts.LOGGER.info("VALHALLA", "QUIT Screen recognised. Quitting game...")
                util.quit_game()

        elif consts.current_screen == Screens.SOUND_WARNING:
            sound_warning_screen.render()
            sound_warning_screen.handle_mouse_event()

        # Show debug overlay
        if consts.SETTINGS['DEBUG_OVERLAY']:
            debug_overlay.render()

        # Perform all event checks while the player
        # isn't on the splashscreen
        if not consts.current_screen == Screens.SPLASHSCREEN:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    # Toggle debug overlay if F12 key is pressed
                    if event.key == pygame.K_F12:
                        if consts.SETTINGS['DEBUG_OVERLAY']:
                            consts.LOGGER.debug("Valhalla", "Hiding debug overlay")
                        else:
                            consts.LOGGER.debug("Valhalla", "Showing debug overlay")
                        consts.SETTINGS['DEBUG_OVERLAY'] = not consts.SETTINGS['DEBUG_OVERLAY']

                    if consts.game is not None:
                        # Pause/unpause the game if escape button is pressed
                        if event.key == pygame.K_ESCAPE:
                            consts.game.pause(not consts.game.paused)
                            # pygame.mouse.set_visible(consts.game.paused)
                            # pygame.mouse.set_pos(int(window.get_size()[0] / 2), int(window.get_size()[1] / 2))

                # If window "x" button pressed, close the game
                if event.type == pygame.QUIT:
                    util.quit_game()

            # Log updated screen
            if temp_screen != consts.current_screen:
                consts.LOGGER.info("Valhalla",
                                   f"Switched screens from {Screens(temp_screen).name} to {Screens(consts.current_screen).name}")

        pygame.display.update()

        # Limit framerate to 120fps - Should we remove?
        consts.clock.tick()


try:
    main()
except util.ValhallaException as e:
    consts.LOGGER.write_message("")
    consts.LOGGER.write_message("=======================================================================")
    consts.LOGGER.write_message("To report this bug, please give this log to the developers")
    consts.LOGGER.write_message("")
    traces = []
    tb = e.__traceback__
    while tb is not None:
        traces.append({
            "filename": tb.tb_frame.f_code.co_filename,
            "name": tb.tb_frame.f_code.co_name,
            "lineno": tb.tb_lineno
        })
        tb = tb.tb_next

    for trace in traces:
        file_dir = trace['filename'].split('/')
        traceStr = f"File {file_dir[len(file_dir) - 1]}:{trace['lineno']} in {trace['name']}"
        consts.LOGGER.error("VALHALLA", traceStr)
    consts.LOGGER.error("VALHALLA", e)
    consts.LOGGER.stop()
