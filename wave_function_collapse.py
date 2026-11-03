"""Executable entry point for the WFC pygame demo.

The main loop performs these phases:
1. Initialize pygame and rendering surfaces.
2. Build the world model and renderer.
3. Repeatedly execute one collapse step per frame until complete.
4. Redraw the frame and process user quit input.
5. Cleanly shut down pygame.
"""

import pygame
from class_world import World
from class_draw_world import DrawWorld
from constants import WORLD_X, WORLD_Y, TILE_SIZE, TILE_SCALE


def main():
    """Run the interactive world-generation demo and return an exit code."""

    # ``done`` tracks whether the solver has finished collapsing the full grid.
    done = False
    # ``is_running`` controls the window/event loop lifecycle.
    is_running = True

    # Initialize pygame subsystems.
    pygame.init()  # pylint: disable=E1101

    # Frame-rate limiter.
    clock = pygame.time.Clock()

    # Create the application window sized to scaled world dimensions.
    display_surface = pygame.display.set_mode(
        (WORLD_X * TILE_SIZE * TILE_SCALE, WORLD_Y * TILE_SIZE * TILE_SCALE)
    )

    # Set window title shown by the OS.
    pygame.display.set_caption("Wave Function Collapse")

    # Construct model and renderer, then draw initial state.
    world = World(WORLD_X, WORLD_Y)
    draw_world = DrawWorld(world)
    draw_world.update()

    while is_running:
        # Poll input events and handle quit keys/window close events.
        for event in pygame.event.get():
            # Exit when ESC is pressed or when the user closes the window.
            if (
                event.type == pygame.KEYDOWN  # pylint: disable=E1101
                and event.key == pygame.K_ESCAPE  # pylint: disable=E1101
            ) or event.type == pygame.QUIT:  # pylint: disable=E1101
                is_running = False

        # Advance generation one step per frame until complete.
        if not done:
            results = world.wave_function_collapse()
            if results == 0:
                done = True

        # Render the latest world state.
        draw_world.update()
        draw_world.draw(display_surface)

        # Present the frame and cap frame rate.
        pygame.display.flip()
        clock.tick(60)

    # Shutdown pygame cleanly if still initialized.
    if pygame.get_init():  # pylint: disable=E1101
        pygame.quit()  # pylint: disable=E1101

    return 0


if __name__ == "__main__":
    main()
