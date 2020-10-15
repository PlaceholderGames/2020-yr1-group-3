"""
    Author:  Nathan Dow / Bitheral
    Created: 14/10/2020
"""
import pygame
import util
from consts import TEXTURES, FONTS, Screens, BUTTONS

dimensions = {
    'width': 800,
    'height': 600
}

# Create pygame window with title and icon
screen = pygame.display.set_mode((dimensions['width'], dimensions['height']))
canvas = pygame.Surface((dimensions['width'], dimensions['height']))
clock = pygame.time.Clock()
pygame.display.set_caption("The BeerZerker")

# Initialize pygame
pygame.init()


# Uncomment the following line once we have a icon for the game
# pygame.display.set_icon(TEXTURES['window_icon'])

### SPLASHSCREEN START
def splashscreen():
    usw_logo_pos = {
        'x': (dimensions['width'] / 2) - 128,
        'y': (dimensions['height'] / 2) - 192
    }
    usw_str = "Made by students at The University of South Wales"
    util.render(screen, TEXTURES['usw_logo'], int(usw_logo_pos['x']), int(usw_logo_pos['y']))
    util.render(screen, util.text(usw_str, FONTS['Pixellari']), int(usw_logo_pos['x']), int(usw_logo_pos['y']))


canvas.fill((0, 0, 0))
util.fade_in(screen, canvas, 6, splashscreen)
util.fade_out(screen, canvas, 6, splashscreen)
### END SPLAHSCREEN

is_running = True
show_fps = True
displaying = 0

# Game loop
while is_running:
    screen.fill((0, 0, 0))
    if show_fps:
        util.render(screen, util.text(f"{str(int(clock.get_fps()))}fps", FONTS['Pixellari']), 16, 16)
        util.render(screen, util.text(f"Current screen: {str(Screens(displaying).name)}", FONTS['Pixellari']), 16, 37)

    if displaying == Screens.MAIN_MENU.value:
        BUTTONS['mm_play'].canvas = screen
        BUTTONS['mm_play'].font = FONTS['Pixellari']
        BUTTONS['mm_play'].draw()

        # pygame.draw.rect(screen, (255, 0, 0), (128, 16, 100, 16))

    for event in pygame.event.get():

        # Checks if window wants to close
        if event.type == pygame.QUIT:
            is_running = False

    # Update the display
    pygame.display.update()
    pygame.display.flip()
    clock.tick()

if not is_running:
    quit()
