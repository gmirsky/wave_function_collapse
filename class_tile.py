"""
Class Tile is used to represent a single tile in the wave function collapse algorithm.
"""

import random
from constants import tile_rules, tile_weight, NORTH, EAST, SOUTH, WEST


class Tile:
    """
    Class Tile is used to represent a single tile in the wave function collapse algorithm.
    """

    def __init__(self, x, y):
        """
        Constructor for the Tile class
        """
        self.possibilities = list(tile_rules.keys())
        self.entropy = len(self.possibilities)
        self.neighbours = {}
        _ = x
        _ = y

    def add_adjacent_tile(self, direction, tile):
        """
        Adds an adjacent tile to the tile
        """
        self.neighbours[direction] = tile

    def get_adjacent_tile(self, direction):
        """
        Returns the adjacent tile in the given direction
        """
        return self.neighbours[direction]

    def get_possible_directions(self):
        """
        Returns a list of possible directions for the tile to be placed in
        """
        return list(self.neighbours.keys())

    def get_possible_tiles_to_place_adjacently(self):
        """
        Returns a list of possible tiles to place adjacently to the current tile
        """
        return self.possibilities

    def collapse(self):
        """
        Collapses the tile to a single possibility

        The possibility is chosen based on the weight of the possibility
        """
        weights = [tile_weight[possibility] for possibility in self.possibilities]
        self.possibilities = random.choices(
            self.possibilities, weights=weights, k=1  # nosec b311
        )
        self.entropy = 0

    def constrain(self, adjacent_possibilities, direction):
        """
        Constrains the tile based on the given neighbour possibilities and direction

        Returns True if the tile was reduced, False otherwise
        """
        reduced = False

        if self.entropy > 0:
            connectors = [
                tile_rules[possible_adjacent_tiles][direction]
                for possible_adjacent_tiles in adjacent_possibilities
            ]
            # check opposite side
            if direction == NORTH:
                opposite = SOUTH
            elif direction == EAST:
                opposite = WEST
            elif direction == SOUTH:
                opposite = NORTH
            elif direction == WEST:
                opposite = EAST

            for possibility in self.possibilities.copy():
                if tile_rules[possibility][opposite] not in connectors:
                    self.possibilities.remove(possibility)
                    reduced = True

            self.entropy = len(self.possibilities)

        return reduced
