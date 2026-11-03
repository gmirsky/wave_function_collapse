"""Unit tests for Tile."""

from class_tile import Tile
from constants import NORTH, SOUTH, tile_rules


def test_tile_constructor_sets_defaults():
    """A tile starts with all possibilities and matching entropy."""
    tile = Tile(0, 0)

    assert tile.possibilities == list(tile_rules.keys())
    assert tile.entropy == len(tile_rules)
    assert tile.neighbours == {}


def test_add_and_get_adjacent_tile():
    """Adjacent tile mapping is retrievable by direction."""
    tile = Tile(0, 0)
    north_tile = Tile(0, 1)

    tile.add_adjacent_tile(NORTH, north_tile)

    assert tile.get_adjacent_tile(NORTH) is north_tile
    assert tile.get_possible_directions() == [NORTH]


def test_collapse_reduces_to_single_possibility():
    """Collapse resolves the tile to one possible type."""
    tile = Tile(0, 0)

    tile.collapse()

    assert tile.entropy == 0
    assert len(tile.possibilities) == 1
    assert tile.possibilities[0] in tile_rules


def test_constrain_reduces_possibilities_for_valid_direction():
    """Constraining with specific neighbor choices can reduce entropy."""
    tile = Tile(0, 0)
    before = set(tile.possibilities)

    reduced = tile.constrain([1], NORTH)

    assert reduced is True
    assert tile.entropy < len(before)
    assert set(tile.possibilities).issubset(before)


def test_constrain_noop_when_already_collapsed():
    """Collapsed tiles are not constrained further."""
    tile = Tile(0, 0)
    tile.possibilities = [tile.possibilities[0]]
    tile.entropy = 0

    reduced = tile.constrain([1], SOUTH)

    assert reduced is False
    assert tile.entropy == 0
