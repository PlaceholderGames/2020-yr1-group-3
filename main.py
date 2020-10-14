"""
    Author:  Nathan Dow / Bitheral
    Created: 14/10/2020
"""

import pygame
import util

resolution = [800, 600]
is_running = True

# Create pygame window with title and icon
screen = pygame.display.set_mode((resolution[0], resolution[1]))
pygame.display.set_caption("The BeerZerker")

# All textures (inclusive and exclusive of gameplay) get initialized and assigned
TEXTURES = {
    # 'window_icon': util.load_image("assets/textures/gui/icon.png")
    # 'player_spritesheet': util.load_image("assets/textures/spritesheets/player.png")
}

"""
# All sounds get initialized and assigned
SOUNDS = {
    
}
"""

# Initialize pygame
pygame.init()

# Uncomment the following line once we have a icon for the game
# pygame.display.set_icon(TEXTURES['window_icon'])

# Game loop
while is_running:
    for event in pygame.event.get():

        # Checks if window wants to close
        if event.type == pygame.QUIT:
            is_running = False

    # Update the display
    pygame.display.update()

if not is_running:
    quit()