"""Renderer for the wave-function-collapse world grid.

This class converts the ``World`` model into a pygame surface by drawing either:
* entropy overlays for unresolved tiles, or
* terrain sprites for collapsed tiles.
"""

import itertools
from typing import Any, TYPE_CHECKING
import pygame
import constants

if TYPE_CHECKING:
    from class_world import World


class DrawWorld:
    """Draw and update a visual representation of the world."""

    def __init__(self, world: "World") -> None:
        """Initialize drawing resources.

        Args:
            world: The ``World`` instance to render.
        """
        # Fonts sized for different entropy digit widths.
        self.font_16 = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.font_10 = pygame.font.Font(pygame.font.get_default_font(), 10)
        self.font_8 = pygame.font.Font(pygame.font.get_default_font(), 8)

        # Load the sprite atlas once and reuse it for all frame updates.
        self.spritesheet = pygame.image.load(constants.SPRITE_SHEET_PATH).convert_alpha()
        self.world: Any = world

        # Off-screen surface used as the composed world image.
        self.world_surface = pygame.Surface(
            (constants.WORLD_X * constants.TILE_SIZE * constants.TILE_SCALE, constants.WORLD_Y * constants.TILE_SIZE * constants.TILE_SCALE)
        )

    def update(self) -> None:
        """Redraw the world surface from current world state."""
        # Highlight lowest-entropy unresolved tiles for easier visual debugging.
        lowest_entropy = self.world.get_the_lowest_entrophy()

        # Draw every world tile in row-major order.
        for y, x in itertools.product(range(constants.WORLD_Y), range(constants.WORLD_X)):
            tile_entropy = self.world.get_entrophy(x, y)
            tile_type = self.world.get_type(x, y)

            # Unresolved tile: draw entropy as text.
            if tile_entropy > 0:
                tile_image = pygame.Surface((constants.TILE_SIZE, constants.TILE_SIZE))
                # Use progressively smaller fonts as entropy values grow.
                if tile_entropy == 27:
                    text_surface = self.font_8.render(
                        str(tile_entropy), True, constants.DARK_GREY
                    )
                    tile_image.blit(text_surface, (3, 3))
                elif tile_entropy >= 10:
                    text_surface = self.font_10.render(str(tile_entropy), True, constants.GREY)
                    tile_image.blit(text_surface, (2, 3))
                else:
                    text_surface = (
                        self.font_16.render(str(tile_entropy), True, constants.GREEN)
                        if tile_entropy == lowest_entropy
                        else self.font_16.render(str(tile_entropy), True, constants.WHITE)
                    )
                    tile_image.blit(text_surface, (4, 1))

            # Collapsed non-forest tile: draw sprite directly.
            elif tile_type < constants.TILE_FOREST_N:
                pos: tuple[int, int] = constants.sprite_tiles[tile_type]
                tile_image = self.spritesheet.subsurface(
                    pygame.Rect(pos[0], pos[1], constants.TILE_SIZE, constants.TILE_SIZE)
                )

            # Forest tile: draw grass base first, then forest overlay sprite.
            else:
                pos: tuple[int, int] = constants.sprite_tiles[constants.TILE_GRASS]
                tile_image = self.spritesheet.subsurface(
                    pygame.Rect(pos[0], pos[1], constants.TILE_SIZE, constants.TILE_SIZE)
                )
                tile_image = pygame.transform.scale_by(
                    tile_image, (constants.TILE_SCALE, constants.TILE_SCALE)
                )
                self.world_surface.blit(
                    tile_image, (x * constants.TILE_SIZE * constants.TILE_SCALE, y * constants.TILE_SIZE * constants.TILE_SCALE)
                )
                pos: tuple[int, int] = constants.sprite_tiles[tile_type]
                tile_image = self.spritesheet.subsurface(
                    pygame.Rect(pos[0], pos[1], constants.TILE_SIZE, constants.TILE_SIZE)
                )

            # Scale each tile to display size and blit to world surface.
            tile_image = pygame.transform.scale_by(tile_image, (constants.TILE_SCALE, constants.TILE_SCALE))
            self.world_surface.blit(
                tile_image, (x * constants.TILE_SIZE * constants.TILE_SCALE, y * constants.TILE_SIZE * constants.TILE_SCALE)
            )

    def draw(self, display_surface: pygame.Surface) -> None:
        """Blit the prepared world surface to the active display surface."""
        display_surface.blit(self.world_surface, (0, 0))
