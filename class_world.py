"""
Class representing the world to be generated
"""

import itertools
import random
from class_tile import Tile
from class_stack import Stack
from constants import NORTH, EAST, SOUTH, WEST, tile_rules


class World:
    """

    Class representing the world

    Attributes:
        cols (int): Number of columns in the world
        rows (int): Number of rows in the world
        tile_rows (list): List of lists of tiles

    """

    def __init__(self, size_x, size_y):
        """
        Constructor for the World class
        """
        self.cols = size_x
        self.rows = size_y

        self.tile_rows = []

        # Create tiles
        for y in range(size_y):
            tiles = []
            for x in range(size_x):
                tile = Tile(x, y)
                tiles.append(tile)
            self.tile_rows.append(tiles)

        # Add adjacent tiles
        for y in range(size_y):
            for x in range(size_x):
                tile = self.tile_rows[y][x]
                if y > 0:
                    tile.add_adjacent_tile(NORTH, self.tile_rows[y - 1][x])
                if x < size_x - 1:
                    tile.add_adjacent_tile(EAST, self.tile_rows[y][x + 1])
                if y < size_y - 1:
                    tile.add_adjacent_tile(SOUTH, self.tile_rows[y + 1][x])
                if x > 0:
                    tile.add_adjacent_tile(WEST, self.tile_rows[y][x - 1])

    def get_entrophy(self, x, y):
        """
        Returns the entropy of the tile at the given coordinates
        """
        return self.tile_rows[y][x].entropy

    def get_type(self, x, y):
        """
        Returns the type of the tile at the given coordinates
        """
        return self.tile_rows[y][x].possibilities[0]

    def get_the_lowest_entrophy(self):
        """
        Returns the lowest entropy of all tiles in the world
        """
        lowest_entrophy = len(list(tile_rules.keys()))
        for y, x in itertools.product(range(self.rows), range(self.cols)):
            if 0 < self.tile_rows[y][x].entropy < lowest_entrophy:
                lowest_entrophy = self.tile_rows[y][x].entropy
        return lowest_entrophy

    def get_tiles_with_the_lowest_entrophy(self):
        """
        Returns a list of tiles with the lowest entropy
        """
        lowest_entrophy = len(list(tile_rules.keys()))
        tile_list = []

        for y, x in itertools.product(range(self.rows), range(self.cols)):
            entrophy_of_the_tile = self.tile_rows[y][x].entropy
            if entrophy_of_the_tile > 0:
                if entrophy_of_the_tile < lowest_entrophy:
                    tile_list.clear()
                    lowest_entrophy = entrophy_of_the_tile
                if entrophy_of_the_tile == lowest_entrophy:
                    tile_list.append(self.tile_rows[y][x])
        return tile_list

    def wave_function_collapse(self):
        """
        Performs one iteration of the wave function collapse algorithm

        Returns:
            int: Number of tiles collapsed (1)
        """
        tiles_with_the_lowest_entrophy = self.get_tiles_with_the_lowest_entrophy()

        if not tiles_with_the_lowest_entrophy:
            return 0

        tile_to_be_collapsed = random.choice(
            tiles_with_the_lowest_entrophy
        )  # nosec b311
        tile_to_be_collapsed.collapse()

        stack = Stack()
        stack.push(tile_to_be_collapsed)

        while not stack.is_empty():
            tile = stack.pop()
            possible_tiles = tile.get_possible_tiles_to_place_adjacently()
            directions = tile.get_possible_directions()

            for direction in directions:
                neighbour = tile.get_adjacent_tile(direction)
                if neighbour.entropy != 0 and neighbour.constrain(
                    possible_tiles, direction
                ):
                    stack.push(neighbour)

        return 1
