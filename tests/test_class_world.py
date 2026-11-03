"""Unit tests for World."""

import class_world
from class_world import World
from constants import EAST, NORTH, SOUTH, WEST


def test_world_initialization_builds_grid():
    """World stores dimensions and creates the expected tile grid."""
    world = World(3, 2)

    assert world.cols == 3
    assert world.rows == 2
    assert len(world.tile_rows) == 2
    assert all(len(row) == 3 for row in world.tile_rows)


def test_world_wires_tile_neighbours():
    """Tiles know their valid adjacent tiles."""
    world = World(2, 2)
    top_left = world.tile_rows[0][0]
    bottom_right = world.tile_rows[1][1]

    assert set(top_left.get_possible_directions()) == {EAST, SOUTH}
    assert set(bottom_right.get_possible_directions()) == {NORTH, WEST}


def test_get_entropy_and_type_from_coordinates():
    """World proxies tile entropy and type by coordinate."""
    world = World(1, 1)
    tile = world.tile_rows[0][0]
    tile.possibilities = [42]
    tile.entropy = 1

    assert world.get_entrophy(0, 0) == 1
    assert world.get_type(0, 0) == 42


def test_get_the_lowest_entropy_ignores_collapsed_tiles():
    """Lowest entropy uses only tiles with entropy greater than zero."""
    world = World(2, 1)
    world.tile_rows[0][0].entropy = 0
    world.tile_rows[0][1].entropy = 2

    assert world.get_the_lowest_entrophy() == 2


def test_wave_function_collapse_returns_zero_when_complete():
    """No work is done when every tile is already collapsed."""
    world = World(2, 2)
    for row in world.tile_rows:
        for tile in row:
            tile.entropy = 0
            tile.possibilities = [tile.possibilities[0]]

    assert world.wave_function_collapse() == 0


def test_wave_function_collapse_collapses_one_tile(monkeypatch):
    """A single WFC step collapses one candidate tile."""
    world = World(2, 1)
    target = world.tile_rows[0][0]
    other = world.tile_rows[0][1]

    target.possibilities = [target.possibilities[0]]
    target.entropy = 1
    other.entropy = 0
    other.possibilities = [other.possibilities[0]]

    monkeypatch.setattr(class_world.random, "choice", lambda seq: seq[0])

    collapsed = world.wave_function_collapse()

    assert collapsed == 1
    assert target.entropy == 0
