"""
Project: World Generation using Wave Function Collapse Algorithm and Pygame

Author: Gregory Mirsky

Revision: 1.0

Description: Wave Function Collapse Algorithm demonstrator. This program
takes no input and generates a world using the Wave Function.

Notes:

Wave Function Collapse is a very independent-minded algorithm and needs
almost no outside help or instruction. You feed it an example to start with
and it figures everything else out for itself using the supplied set of
rules that you have provided.

A random tile is chosen from the set of possible tiles to place in a given
location. The tile is then collapsed to a single possibility based on the
weights of the tiles in the set. The weights are determined by the number of
times a tile appears in the set of possible tiles to place in a given
location.

For a good explanation of the algorithm, see:
https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/

Many of the algorithms and code have been taken from various repositories
on GitHub and the internet, Most of the code has been modified to work
with this project and to pass pylint and bandit security checks.

Overrides for pylint and bandit have been added to the code to allow for
the use of the random.choices() function, which is a false positive flagged
as a security issue by bandit and pylint.

"""

import pygame
from class_world import World
from class_draw_world import DrawWorld
from constants import WORLD_X, WORLD_Y, TILE_SIZE, TILE_SCALE


def main():
    """
    Main function for the Wave Function Collapse Algorithm demonstrator.
    """

    done = False
    is_running = True

    # initialize pygame
    pygame.init()  # pylint: disable=E1101

    # set up the clock
    clock = pygame.time.Clock()

    # set up the display
    display_surface = pygame.display.set_mode(
        (WORLD_X * TILE_SIZE * TILE_SCALE, WORLD_Y * TILE_SIZE * TILE_SCALE)
    )

    # set the window title
    pygame.display.set_caption("Wave Function Collapse")

    # create the world
    world = World(WORLD_X, WORLD_Y)
    draw_world = DrawWorld(world)
    draw_world.update()

    while is_running:
        # poll for events
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked ESC to close the window
            if (
                event.type == pygame.KEYDOWN  # pylint: disable=E1101
                and event.key == pygame.K_ESCAPE  # pylint: disable=E1101
            ) or event.type == pygame.QUIT:  # pylint: disable=E1101
                is_running = False
        if not done:
            results = world.wave_function_collapse()
            if results == 0:
                done = True

        draw_world.update()
        draw_world.draw(display_surface)

        pygame.display.flip()
        clock.tick(60)

    if pygame.get_init():  # pylint: disable=E1101
        pygame.quit()  # pylint: disable=E1101

    return 0


if __name__ == "__main__":
    main()
