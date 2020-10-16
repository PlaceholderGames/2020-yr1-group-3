"""
    Author:  Nathan Dow / Bitheral
    Created: 14/10/2020
"""
import pygame
import util
from consts import TEXTURES, FONTS, Screens, BUTTONS, DIMENSIONS, SETTINGS, CREDITS, CHECKBOXES
import json
import os

# Create pygame window with title and icon
screen = pygame.display.set_mode((DIMENSIONS['width'], DIMENSIONS['height']))
canvas = pygame.Surface((DIMENSIONS['width'], DIMENSIONS['height']))
clock = pygame.time.Clock()
pygame.display.set_caption("The BeerZerker")

# Initialize pygame
pygame.init()

if not os.path.exists("settings.json"):
    util.save_settings()


# Uncomment the following line once we have a icon for the game
# pygame.display.set_icon(TEXTURES['window_icon'])

# Starts game with splashscreen
def splashscreen():
    usw_logo_pos = {
        'x': (DIMENSIONS['width'] / 2) - 128,
        'y': (DIMENSIONS['height'] / 2) - 192
    }
    usw_str = "Made by students at The University of South Wales"
    util.render(screen, TEXTURES['usw_logo'], int(usw_logo_pos['x']), int(usw_logo_pos['y']))
    util.render(screen, util.text(usw_str, FONTS['Pixellari']), int(usw_logo_pos['x']), int(usw_logo_pos['y']))


util.fade_in(screen, canvas, 6, splashscreen)
util.fade_out(screen, canvas, 6, splashscreen)


# Function to display Main Menu screen content
def main_menu_screen():
    ## Renders play button for Main Menu
    BUTTONS['MAIN_MENU']['play'].canvas = screen
    BUTTONS['MAIN_MENU']['play'].font = FONTS['Pixellari']
    BUTTONS['MAIN_MENU']['play'].draw()

    ## Renders settings button for Main Menu
    BUTTONS['MAIN_MENU']['settings'].canvas = screen
    BUTTONS['MAIN_MENU']['settings'].font = FONTS['Pixellari']
    BUTTONS['MAIN_MENU']['settings'].draw()

    ## Renders credits button for Main Menu
    BUTTONS['MAIN_MENU']['credits'].canvas = screen
    BUTTONS['MAIN_MENU']['credits'].font = FONTS['Pixellari']
    BUTTONS['MAIN_MENU']['credits'].draw()

    ## Renders quit button for Main Menu
    BUTTONS['MAIN_MENU']['quit'].canvas = screen
    BUTTONS['MAIN_MENU']['quit'].font = FONTS['Pixellari']
    BUTTONS['MAIN_MENU']['quit'].draw()


# Function to display Setting screen content
def setting_screen():
    util.render(screen, util.text(f"Settings", FONTS['Pixellari']), (DIMENSIONS['width'] / 2) - len("Settings"), 16)

    CHECKBOXES['SETTINGS']['fullscreen'].canvas = screen
    CHECKBOXES['SETTINGS']['fullscreen'].font = FONTS['Pixellari']
    CHECKBOXES['SETTINGS']['fullscreen'].draw()


# Function to display Credit screen content
def credit_screen():
    # Credit title
    #
    credits_title_str = "Credits"
    credits_title_width, credits_title_height = FONTS['Pixellari'].size(credits_title_str)
    util.render(screen, util.text(credits_title_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (credits_title_width / 2), 64)

    """
    # Lead Programmer
    #
    lead_programmer_str = "Lead Programmer:"
    lead_programmer_width, lead_programmer_height = FONTS["Pixellari"].size(lead_programmer_str)
    util.render(screen, util.text(lead_programmer_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (lead_programmer_width / 2), 128)

    lead_programmer_person_str = "Nathan Dow / Bitheral"
    lead_programmer_person_width, lead_programmer_person_height = FONTS["Pixellari"].size(lead_programmer_person_str)
    util.render(screen, util.text(lead_programmer_person_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (lead_programmer_person_width / 2), 132 + lead_programmer_height)
    """

    CREDITS['LEAD_PROGRAMMER'].canvas = screen
    CREDITS['LEAD_PROGRAMMER'].draw()

    CREDITS['PROGRAMMING'].canvas = screen
    CREDITS['PROGRAMMING'].draw()

    CREDITS['LEAD_ARTIST'].canvas = screen
    CREDITS['LEAD_ARTIST'].draw()

    CREDITS['CONCEPT_ARTIST'].canvas = screen
    CREDITS['CONCEPT_ARTIST'].draw()

    # Renders back button for credits
    #
    BUTTONS['CREDITS']['back'].canvas = screen
    BUTTONS['CREDITS']['back'].font = FONTS['Pixellari']
    BUTTONS['CREDITS']['back'].draw()


# Determines whether if the game is running
is_running = True

# Determine what screen to render
displaying = 0


# Changes what screen to render
def set_screen(destination):
    global displaying
    displaying = destination.value


# Game loop
while is_running:
    with open("settings.json") as settingFile:
        _settings = json.load(settingFile)
        debug_mode = SETTINGS["DEBUG_MODE"]
        settingFile.close()

    # Set mouse variable to the current mouse position
    mouse = pygame.mouse.get_pos()

    # Set the background of the window to black
    screen.fill((0, 0, 0))

    # Check what screen to render based on displaying value
    #
    if displaying == Screens.MAIN_MENU.value:
        main_menu_screen()

    elif displaying == Screens.SETTINGS.value:
        setting_screen()

    elif displaying == Screens.CREDITS.value:
        credit_screen()

    # Gets all events in pygame
    for event in pygame.event.get():

        # If player clicks mouse, execute statements
        if event.type == pygame.MOUSEBUTTONDOWN:

            # If the screen is currently on Main Menu
            if displaying == Screens.MAIN_MENU.value:

                # Check for every button in the main menu to see if it can be clicked on
                for button in BUTTONS['MAIN_MENU']:
                    if BUTTONS['MAIN_MENU'][button].can_click():
                        # Change screen to the button destination
                        set_screen(BUTTONS['MAIN_MENU'][button].destination)

            if displaying == Screens.SETTINGS.value:

                # Check for every checkbox in the settings to see if it can be clicked
                for checkbox in CHECKBOXES['SETTINGS']:
                    if CHECKBOXES['SETTINGS'][checkbox].can_click():
                        # Invert state
                        CHECKBOXES['SETTINGS'][checkbox].state = not CHECKBOXES['SETTINGS'][checkbox].state

            # If the screen is currently on the Credits
            if displaying == Screens.CREDITS.value:

                # Check for every button in the credits to see if it can be clicked on
                for button in BUTTONS['CREDITS']:
                    if BUTTONS['CREDITS'][button].can_click():
                        # Change screen to button destination
                        set_screen(BUTTONS['CREDITS'][button].destination)

            if displaying == Screens.QUIT.value:
                is_running = False

        # Checks if window wants to close
        if event.type == pygame.QUIT:
            is_running = False

    # Display debug mode content
    if debug_mode:
        # Renders FPS (frames per second)
        util.render(screen, util.text(f"{str(int(clock.get_fps()))}fps", FONTS['Pixellari']), 16, 16)

        # Renders the current screen that is being displayed
        util.render(screen, util.text(f"Current screen: {str(Screens(displaying).name)}", FONTS['Pixellari']), 16,
                    37)

        # Renders the X and Y position of the mouse
        util.render(screen, util.text(f"Mouse position - X:{str(mouse[0])}, Y: {str(mouse[1])}", FONTS['Pixellari']),
                    16, 58)

    # Update the display
    pygame.display.update()
    pygame.display.flip()

    # Limit the FPS to 120fps
    clock.tick(120)

if not is_running:
    quit()
