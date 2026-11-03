"""Tile model for the Wave Function Collapse grid.

Each tile keeps:
* the set of currently valid tile types (``possibilities``),
* the number of possibilities still available (``entropy``),
* references to neighboring tiles by cardinal direction.

The solver repeatedly collapses one tile and then constrains neighboring tiles
until no further reductions can be made.
"""

import random
import constants


class Tile:
    """Represents one grid cell in the WFC world."""

    def __init__(self, x: int, y: int) -> None:
        """Create a tile initialized with all rule-defined tile types.

        Args:
            x: Tile x-coordinate (unused by current logic, retained for parity
                with existing constructor callers).
            y: Tile y-coordinate (unused by current logic, retained for parity
                with existing constructor callers).
        """
        # Start unconstrained: every tile type is allowed.
        self.possibilities: list[int] = list(constants.tile_rules.keys())
        # Entropy is represented as the count of remaining possibilities.
        self.entropy: int = len(self.possibilities)
        # Neighbor references indexed by NORTH/EAST/SOUTH/WEST.
        self.neighbours = {}
        # Coordinates are currently not stored on instances, but callers pass
        # them and tests construct tiles with positional arguments.
        _ = x
        _ = y

    def add_adjacent_tile(self, direction: int, tile: "Tile") -> None:
        """Register one adjacent tile in a specific direction."""
        self.neighbours[direction] = tile

    def get_adjacent_tile(self, direction: int):
        """Return the neighbor tile in ``direction``."""
        return self.neighbours[direction]

    def get_possible_directions(self):
        """Return directions that currently have neighbor links."""
        return list(self.neighbours.keys())

    def get_possible_tiles_to_place_adjacently(self) -> list[int]:
        """Return this tile's currently valid tile-type possibilities."""
        return self.possibilities

    def collapse(self) -> None:
        """Collapse this tile to one weighted-random possibility.

        The tile weights from ``constants.tile_weight`` bias the random choice,
        which steers generation toward more common terrain patterns.
        """
        # Build a weight list aligned with current possibilities.
        weights: list[int] = [constants.tile_weight[possibility] for possibility in self.possibilities]
        self.possibilities: list[int] = random.choices(
            self.possibilities,
            weights=weights,
            k=1,  # nosec b311
        )
        # Entropy 0 indicates this tile is fixed to a single type.
        self.entropy = 0

    def constrain(self, adjacent_possibilities: list[int], direction: int) -> bool:
        """Reduce possibilities using one neighbor's current possibilities.

        Args:
            adjacent_possibilities: Tile types the adjacent tile can still take.
            direction: Direction of the adjacent tile relative to ``self``.

        Returns:
            ``True`` if at least one possibility was removed, otherwise ``False``.
        """
        reduced = False

        if self.entropy > 0:
            # Collect all connector edge values that the adjacent tile could
            # expose toward this tile on ``direction``.
            connectors = [
                constants.tile_rules[possible_adjacent_tiles][direction]
                for possible_adjacent_tiles in adjacent_possibilities
            ]
            # Determine which side of this tile faces that adjacent tile.
            if direction == constants.NORTH:
                opposite: int = constants.SOUTH
            elif direction == constants.EAST:
                opposite: int = constants.WEST
            elif direction == constants.SOUTH:
                opposite: int = constants.NORTH
            elif direction == constants.WEST:
                opposite: int = constants.EAST

            # Remove any possibility whose connector does not match any allowed
            # connector from the adjacent tile.
            for possibility in self.possibilities.copy():
                if constants.tile_rules[possibility][opposite] not in connectors:
                    self.possibilities.remove(possibility)
                    reduced = True

            # Keep entropy synchronized with the updated possibility count.
            self.entropy: int = len(self.possibilities)

        return reduced
