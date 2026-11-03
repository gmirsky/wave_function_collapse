"""World model and Wave Function Collapse step implementation.

The ``World`` owns a 2D grid of ``Tile`` objects and the neighbor links between
them. It also exposes helper methods used by rendering and by the collapse loop.
"""

import itertools
import random
from typing import Any
import class_tile
import class_stack
import constants


class World:
    """Mutable world state for a generated tile map."""

    def __init__(self, size_x: int, size_y: int) -> None:
        """Create the tile grid and wire all cardinal neighbors.

        Args:
            size_x: Number of columns.
            size_y: Number of rows.
        """
        self.cols: Any = size_x
        self.rows: Any = size_y

        self.tile_rows = []

        # Create the 2D tile array (row-major order).
        for y in range(size_y):
            tiles = []
            for x in range(size_x):
                tile = class_tile.Tile(x, y)
                tiles.append(tile)
            self.tile_rows.append(tiles)

        # Register adjacency links so each tile can constrain its neighbors.
        for y in range(size_y):
            for x in range(size_x):
                tile = self.tile_rows[y][x]
                if y > 0:
                    tile.add_adjacent_tile(constants.NORTH, self.tile_rows[y - 1][x])
                if x < size_x - 1:
                    tile.add_adjacent_tile(constants.EAST, self.tile_rows[y][x + 1])
                if y < size_y - 1:
                    tile.add_adjacent_tile(constants.SOUTH, self.tile_rows[y + 1][x])
                if x > 0:
                    tile.add_adjacent_tile(constants.WEST, self.tile_rows[y][x - 1])

    def get_entrophy(self, x: int, y: int):
        """Return entropy for tile at ``(x, y)``."""
        return self.tile_rows[y][x].entropy

    def get_type(self, x: int, y: int):
        """Return resolved tile type for tile at ``(x, y)``."""
        return self.tile_rows[y][x].possibilities[0]

    def get_the_lowest_entrophy(self):
        """Return smallest non-zero entropy currently present in the grid."""
        lowest_entrophy: int = len(list(constants.tile_rules.keys()))
        for y, x in itertools.product(range(self.rows), range(self.cols)):
            if 0 < self.tile_rows[y][x].entropy < lowest_entrophy:
                lowest_entrophy = self.tile_rows[y][x].entropy
        return lowest_entrophy

    def get_tiles_with_the_lowest_entrophy(self):
        """Return all non-collapsed tiles tied for lowest entropy."""
        lowest_entrophy: int = len(list(constants.tile_rules.keys()))
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

    def wave_function_collapse(self) -> int:
        """Perform one WFC step: collapse one tile then propagate constraints.

        Returns:
            0 when all tiles are already collapsed, otherwise 1.
        """
        # Candidate set consists of all tiles with minimal non-zero entropy.
        tiles_with_the_lowest_entrophy = self.get_tiles_with_the_lowest_entrophy()

        if not tiles_with_the_lowest_entrophy:
            return 0

        # Randomly pick one minimum-entropy tile and collapse it.
        tile_to_be_collapsed = random.choice(tiles_with_the_lowest_entrophy)  # nosec b311
        tile_to_be_collapsed.collapse()

        # Propagate constraints through neighbors using an explicit stack.
        stack = class_stack.Stack()
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
                    # If a neighbor was reduced, it may further reduce its own
                    # neighbors and must be revisited.
                    stack.push(neighbour)

        return 1
