"""
Class DrawWorld is used to draw the world to the screen.
"""
# Importing modules
import itertools
import pygame
from constants import SPRITE_SHEET_PATH, TILE_SIZE, TILE_SCALE
from constants import WORLD_X, WORLD_Y, TILE_GRASS, TILE_FOREST_N, sprite_tiles
from constants import DARK_GREY, GREY, GREEN, WHITE


class DrawWorld:
    """
    Class DrawWorld is used to draw the world to the screen.
    """

    def __init__(self, world):
        """
        Constructor for Class DrawWorld
        """
        self.font_16 = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.font_10 = pygame.font.Font(pygame.font.get_default_font(), 10)
        self.font_8 = pygame.font.Font(pygame.font.get_default_font(), 8)
        self.spritesheet = pygame.image.load(SPRITE_SHEET_PATH).convert_alpha()
        self.world = world
        self.world_surface = pygame.Surface(
            (WORLD_X * TILE_SIZE * TILE_SCALE, WORLD_Y * TILE_SIZE * TILE_SCALE)
        )

    def update(self):
        """
        Updates the world surface
        """
        lowest_entropy = self.world.get_the_lowest_entrophy()
        # Draw the world
        for y, x in itertools.product(range(WORLD_Y), range(WORLD_X)):
            tile_entropy = self.world.get_entrophy(x, y)
            tile_type = self.world.get_type(x, y)
            # Draw the tile
            if tile_entropy > 0:
                tile_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
                # set the alpha value of the surface
                if tile_entropy == 27:
                    text_surface = self.font_8.render(
                        str(tile_entropy), True, DARK_GREY
                    )
                    tile_image.blit(text_surface, (3, 3))
                elif tile_entropy >= 10:
                    text_surface = self.font_10.render(str(tile_entropy), True, GREY)
                    tile_image.blit(text_surface, (2, 3))
                else:
                    text_surface = (
                        self.font_16.render(str(tile_entropy), True, GREEN)
                        if tile_entropy == lowest_entropy
                        else self.font_16.render(str(tile_entropy), True, WHITE)
                    )
                    tile_image.blit(text_surface, (4, 1))
            elif tile_type < TILE_FOREST_N:
                pos = sprite_tiles[tile_type]
                tile_image = self.spritesheet.subsurface(
                    pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
                )
            else:  # Forest needs a grass tile to be drawn first
                pos = sprite_tiles[TILE_GRASS]
                tile_image = self.spritesheet.subsurface(
                    pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
                )
                tile_image = pygame.transform.scale_by(
                    tile_image, (TILE_SCALE, TILE_SCALE)
                )
                self.world_surface.blit(
                    tile_image, (x * TILE_SIZE * TILE_SCALE, y * TILE_SIZE * TILE_SCALE)
                )
                pos = sprite_tiles[tile_type]
                tile_image = self.spritesheet.subsurface(
                    pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
                )

            tile_image = pygame.transform.scale_by(tile_image, (TILE_SCALE, TILE_SCALE))
            self.world_surface.blit(
                tile_image, (x * TILE_SIZE * TILE_SCALE, y * TILE_SIZE * TILE_SCALE)
            )

    def draw(self, display_surface):
        """
        Draws the world to the screen
        """
        display_surface.blit(self.world_surface, (0, 0))
