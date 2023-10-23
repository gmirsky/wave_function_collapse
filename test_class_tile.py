"""
This test suite covers all the methods in the Tile class.
It tests the path for each method, as well as some
edge cases such as an invalid direction in the constrain
method.

The constrain method is parametrized to test all possible
directions, as well as an invalid direction. Each test
case has a unique ID for easy identification.
"""
import pytest
from class_tile import Tile
from constants import tile_rules, tile_weight, NORTH, EAST, SOUTH, WEST


# Test the constructor
def test_constructor():
    # Arrange
    x, y = 0, 0

    # Act
    tile = Tile(x, y)

    # Assert
    assert tile.possibilities == list(tile_rules.keys())
    assert tile.entropy == len(tile.possibilities)
    assert tile.neighbours == {}


# Test add_adjacent_tile method
def test_add_adjacent_tile():
    # Arrange
    tile1 = Tile(0, 0)
    tile2 = Tile(1, 0)

    # Act
    tile1.add_adjacent_tile(NORTH, tile2)

    # Assert
    assert tile1.get_adjacent_tile(NORTH) == tile2


# Test get_possible_directions method
def test_get_possible_directions():
    # Arrange
    tile = Tile(0, 0)
    tile.add_adjacent_tile(NORTH, Tile(0, 1))

    # Act
    directions = tile.get_possible_directions()

    # Assert
    assert directions == [NORTH]


# Test get_possible_tiles_to_place_adjacently method
def test_get_possible_tiles_to_place_adjacently():
    # Arrange
    tile = Tile(0, 0)

    # Act
    possibilities = tile.get_possible_tiles_to_place_adjacently()

    # Assert
    assert possibilities == list(tile_rules.keys())


# Test collapse method
def test_collapse():
    # Arrange
    tile = Tile(0, 0)

    # Act
    tile.collapse()

    # Assert
    assert tile.entropy == 0
    assert len(tile.possibilities) == 1


# Test constrain method
@pytest.mark.parametrize(
    "direction, expected_reduced",
    [
        (NORTH, True),
        (EAST, True),
        (SOUTH, True),
        (WEST, True),
        ("INVALID_DIRECTION", False),
    ],
    ids=["north", "east", "south", "west", "invalid"],
)
def test_constrain(direction, expected_reduced):
    # Arrange
    tile = Tile(0, 0)
    adjacent_possibilities = list(tile_rules.keys())

    # Act
    reduced = tile.constrain(adjacent_possibilities, direction)

    # Assert
    assert reduced == expected_reduced
