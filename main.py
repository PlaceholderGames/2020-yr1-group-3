"""
    Author:  Nathan Dow / Bitheral
    Created: 14/10/2020
"""
import pygame
import util
import os
from consts import screen, TEXTURES, FONTS, Screens, BUTTONS, DIMENSIONS, SETTINGS, CREDITS, CHECKBOXES

print("Checking for settings file")
if not os.path.exists("settings.json"):
    print("Settings file does not exist; Saving settings file with default settings")
    util.create_settings_file()
else:
    print("Settings file exists; Loading in settings from file")
    util.load_settings()

# Create pygame window with title and icon
canvas = pygame.Surface((DIMENSIONS['width'], DIMENSIONS['height']))
clock = pygame.time.Clock()
pygame.display.set_caption("The BeerZerker")

# Initialize pygame
pygame.init()


# Uncomment the following line once we have a icon for the game
# pygame.display.set_icon(TEXTURES['window_icon'])

# Starts game with splashscreen
def splashscreen():
    usw_logo_pos = {
        'x': (DIMENSIONS['width'] / 2),
        'y': (DIMENSIONS['height'] / 2)
    }

    util.render(screen, TEXTURES['usw_logo'], usw_logo_pos['x'] - (TEXTURES['usw_logo'].get_width() / 2), usw_logo_pos['y'] - (TEXTURES['usw_logo'].get_height()))


    # Splash text
    splash_text_str = "A game developed by students at the University of South Wales"
    splash_text_width, splash_text_height = FONTS['Pixellari'].size(splash_text_str)
    util.render(screen, util.text(splash_text_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (splash_text_width / 2), (DIMENSIONS['height'] / 2) - (splash_text_height / 2))
    #util.render(screen, util.text(usw_str, FONTS['Pixellari']), int(usw_logo_pos['x']), int(usw_logo_pos['y']))


util.fade_in(screen, canvas, 6, splashscreen)
util.fade_out(screen, canvas, 6, splashscreen)


# Function to display Main Menu screen content
def main_menu_screen():

    # Renders all buttons for the main menu
    for _buttons in BUTTONS['MAIN_MENU']:
        BUTTONS['MAIN_MENU'][_buttons].canvas = screen
        BUTTONS['MAIN_MENU'][_buttons].font = FONTS['Pixellari']
        BUTTONS['MAIN_MENU'][_buttons].draw()


# Function to display Setting screen content
def setting_screen():

    # Settings title
    #
    settings_title_str = "Settings"
    settings_title_width, settings_title_height = FONTS['Pixellari'].size(settings_title_str)
    util.render(screen, util.text(settings_title_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (settings_title_width / 2), 64)

    for _checkbox in CHECKBOXES['SETTINGS']:
        CHECKBOXES['SETTINGS'][_checkbox].canvas = screen
        CHECKBOXES['SETTINGS'][_checkbox].font = FONTS['Pixellari']
        CHECKBOXES['SETTINGS'][_checkbox].draw()

    for _buttons in BUTTONS['SETTINGS']:
        BUTTONS['SETTINGS'][_buttons].canvas = screen
        BUTTONS['SETTINGS'][_buttons].font = FONTS['Pixellari']
        BUTTONS['SETTINGS'][_buttons].draw()

    # Setting note
    #
    setting_note_str = "Settings marked with '*' will require a game restart"
    setting_note_width, setting_note_height = FONTS['Pixellari'].size(setting_note_str)
    util.render(screen, util.text(setting_note_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (setting_note_width / 2), DIMENSIONS['height'] - ((setting_note_height / 2) + 32))




# Function to display Credit screen content
def credit_screen():
    # Credit title
    #
    credits_title_str = "Credits"
    credits_title_width, credits_title_height = FONTS['Pixellari'].size(credits_title_str)
    util.render(screen, util.text(credits_title_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (credits_title_width / 2), 64)

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


def pause_menu():

    # Pause title
    #
    pause_title_str = "PAUSED"
    pause_title_width, pause_title_height = FONTS['Pixellari'].size(pause_title_str)
    util.render(screen, util.text(pause_title_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (pause_title_width / 2), 64)

    # Renders all buttons for the main menu
    for _buttons in BUTTONS['PAUSE']:
        BUTTONS['PAUSE'][_buttons].canvas = screen
        BUTTONS['PAUSE'][_buttons].font = FONTS['Pixellari']
        BUTTONS['PAUSE'][_buttons].draw()


def game():
    pass


# Determines whether if the game is running
is_running = True

# Determines if game is paused
is_paused = False

# Determine what screen to render
displaying = 0


# Changes what screen to render
def set_screen(destination):
    global displaying
    displaying = destination.value


# Game loop
while is_running:
    SETTINGS = util.load_settings_file()

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

    elif displaying == Screens.GAME.value:
        game()

        if is_paused:
            pause_menu()

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

                # Check for every button in the setting to see if it can be clicked on
                for button in BUTTONS['SETTINGS']:
                    if BUTTONS['SETTINGS'][button].can_click():
                        # Change screen to the button destination
                        set_screen(BUTTONS['SETTINGS'][button].destination)
                        if button == "save":
                            util.save_settings()
                        elif button == 'back':
                            util.load_settings()

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

            if displaying == Screens.GAME.value:

                if is_paused:
                    for button in BUTTONS['PAUSE']:
                        if BUTTONS['PAUSE'][button].can_click():

                            # Change screen to the button destination
                            if button == "play":
                                is_paused = False
                            set_screen(BUTTONS['PAUSE'][button].destination)

        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()

            if key[pygame.K_ESCAPE]:
                if displaying == Screens.MAIN_MENU.value:
                    is_running = False

                if displaying == Screens.GAME.value:
                    is_paused = not is_paused

        # Checks if window wants to close
        if event.type == pygame.QUIT:
            is_running = False

    # Display debug mode content
    if SETTINGS['SHOW_FPS']:
        # Renders FPS (frames per second)
        util.render(screen, util.text(f"{str(int(clock.get_fps()))}fps", FONTS['Pixellari']), 16, 16)

    # Renders the current screen that is being displayed
    util.render(screen, util.text(f"Current screen: {str(Screens(displaying).name)}", FONTS['Pixellari']), 16,
                37)

    # Renders the X and Y position of the mouse
    util.render(screen, util.text(f"Mouse position - X:{str(mouse[0])}, Y: {str(mouse[1])}", FONTS['Pixellari']),
                16, 58)

    #util.render(screen, util.text(f"{SETTINGS}", FONTS['Pixellari']), 16, screen.get_size()[1] - 32)

    # Update the display
    pygame.display.update()
    pygame.display.flip()

    # Limit the FPS to 120fps
    clock.tick(120)

if not is_running:
    quit()
