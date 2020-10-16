"""
    Author:  Nathan Dow / Bitheral
    Created: 14/10/2020
"""
import pygame
import util
from consts import TEXTURES, FONTS, Screens, BUTTONS, DIMENSIONS

# Create pygame window with title and icon
screen = pygame.display.set_mode((DIMENSIONS['width'], DIMENSIONS['height']))
canvas = pygame.Surface((DIMENSIONS['width'], DIMENSIONS['height']))
clock = pygame.time.Clock()
pygame.display.set_caption("The BeerZerker")

# Initialize pygame
pygame.init()


# Uncomment the following line once we have a icon for the game
# pygame.display.set_icon(TEXTURES['window_icon'])

### SPLASHSCREEN START
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


### END SPLAHSCREEN


def main_menu_screen():
    BUTTONS['MAIN_MENU']['play'].canvas = screen
    BUTTONS['MAIN_MENU']['play'].font = FONTS['Pixellari']
    BUTTONS['MAIN_MENU']['play'].draw()

    BUTTONS['MAIN_MENU']['settings'].canvas = screen
    BUTTONS['MAIN_MENU']['settings'].font = FONTS['Pixellari']
    BUTTONS['MAIN_MENU']['settings'].draw()

    BUTTONS['MAIN_MENU']['credits'].canvas = screen
    BUTTONS['MAIN_MENU']['credits'].font = FONTS['Pixellari']
    BUTTONS['MAIN_MENU']['credits'].draw()

    BUTTONS['MAIN_MENU']['quit'].canvas = screen
    BUTTONS['MAIN_MENU']['quit'].font = FONTS['Pixellari']
    BUTTONS['MAIN_MENU']['quit'].draw()


def setting_screen():
    util.render(screen, util.text(f"Settings", FONTS['Pixellari']), (DIMENSIONS['width'] / 2) - len("Settings"), 16)


def credit_screen():
    credits_title_str = "Credits"
    credits_title_width, credits_title_height = FONTS['Pixellari'].size(credits_title_str)
    util.render(screen, util.text(credits_title_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (credits_title_width / 2), 64)

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

    # Programming
    #
    programming_str = "Programming:"
    programming_width, programming_height = FONTS["Pixellari"].size(programming_str)
    util.render(screen, util.text(programming_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (programming_width / 2), 210)

    programmer_person_1_str = "Bartosz Swieszkowski"
    programmer_person_1_width, programmer_person_1_height = FONTS["Pixellari"].size(programmer_person_1_str)
    util.render(screen, util.text(programmer_person_1_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (programmer_person_1_width / 2), 214 + programmer_person_1_height)

    programmer_person_2_str = "Conner Hughes"
    programmer_person_2_width, programmer_person_2_height = FONTS["Pixellari"].size(programmer_person_2_str)
    util.render(screen, util.text(programmer_person_2_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (programmer_person_2_width / 2), 242 + programmer_person_2_height)

    # Lead Artist
    #
    lead_artist_str = "Lead Artist:"
    lead_artist_width, lead_artist_height = FONTS["Pixellari"].size(lead_artist_str)
    util.render(screen, util.text(lead_artist_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (lead_artist_width / 2), 320)

    lead_artist_person_str = "Conner Hughes"
    lead_artist_person_width, lead_artist_person_height = FONTS["Pixellari"].size(lead_artist_person_str)
    util.render(screen, util.text(lead_artist_person_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (lead_artist_person_width / 2), 324 + lead_artist_height)

    # Concept Artist
    #
    concept_artist_str = "Concept Artist:"
    concept_artist_width, concept_artist_height = FONTS["Pixellari"].size(concept_artist_str)
    util.render(screen, util.text(concept_artist_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (concept_artist_width / 2), 402)

    concept_artist_person_str = "Bartosz Swieszkowski"
    concept_artist_person_width, concept_artist_person_height = FONTS["Pixellari"].size(concept_artist_person_str)
    util.render(screen, util.text(concept_artist_person_str, FONTS['Pixellari']),
                (DIMENSIONS['width'] / 2) - (concept_artist_person_width / 2), 406 + concept_artist_height)

    BUTTONS['CREDITS']['back'].canvas = screen
    BUTTONS['CREDITS']['back'].font = FONTS['Pixellari']
    BUTTONS['CREDITS']['back'].draw()


is_running = True
debug_mode = True
displaying = 0


def button_click(destination):
    global displaying
    displaying = destination.value


# Game loop
while is_running:
    mouse = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))

    if displaying == Screens.MAIN_MENU.value:
        main_menu_screen()

    elif displaying == Screens.SETTINGS.value:
        setting_screen()

    elif displaying == Screens.CREDITS.value:
        credit_screen()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:

            if displaying == Screens.MAIN_MENU.value:
                for button in BUTTONS['MAIN_MENU']:
                    if BUTTONS['MAIN_MENU'][button].can_click():
                        button_click(BUTTONS['MAIN_MENU'][button].destination)
            if displaying == Screens.CREDITS.value:
                for button in BUTTONS['CREDITS']:
                    if BUTTONS['CREDITS'][button].can_click():
                        button_click(BUTTONS['CREDITS'][button].destination)

        # Checks if window wants to close
        if event.type == pygame.QUIT:
            is_running = False

    if debug_mode:
        util.render(screen, util.text(f"{str(int(clock.get_fps()))}fps", FONTS['Pixellari']), 16, 16)
        util.render(screen, util.text(f"Current screen: {str(Screens(displaying).name)}", FONTS['Pixellari']), 16,
                    37)
        util.render(screen, util.text(f"Mouse position - X:{str(mouse[0])}, Y: {str(mouse[1])}", FONTS['Pixellari']),
                    16, 58)

    # Update the display
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

if not is_running:
    print("I am quitting")
    quit()
