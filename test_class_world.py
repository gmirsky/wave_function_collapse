"""
This code provides for testing the World class.
"""
import pytest
from class_world import World


# Test the initialization of the World class
@pytest.mark.parametrize(
    "size_x, size_y, id",
    [
        (5, 5, "happy_path_5x5"),  # Happy path with square world
        (5, 10, "happy_path_5x10"),  # Happy path with rectangular world
        (0, 0, "edge_case_empty_world"),  # Edge case with no tiles
        (
            -1,
            -1,
            "error_case_negative_dimensions",
        ),  # Error case with negative dimensions
    ],
)
def test_world_initialization(size_x, size_y, error_case):
    """
    Test the initialization of the World class.
    """
    # Arrange
    if error_case == "error_case_negative_dimensions":
        with pytest.raises(ValueError):
            World(size_x, size_y)
    else:
        # Act
        world = World(size_x, size_y)

        # Assert
        assert world.cols == size_x
        assert world.rows == size_y
        assert len(world.tile_rows) == size_y
        for row in world.tile_rows:
            assert len(row) == size_x


# Test the get_entrophy method
@pytest.mark.parametrize(
    "x, y, id",
    [
        (0, 0, "happy_path_top_left"),  # Happy path with top left tile
        (4, 4, "happy_path_bottom_right"),  # Happy path with bottom right tile
        (
            -1,
            -1,
            "error_case_negative_coordinates",
        ),  # Error case with negative coordinates
        (
            10,
            10,
            "error_case_out_of_bounds",
        ),  # Error case with coordinates out of bounds
    ],
)
def test_get_entrophy(x, y, error_case):
    """
    Test the get_entrophy method of the World class.
    """
    # Arrange
    world = World(5, 5)

    if error_case in ["error_case_negative_coordinates",
                      "error_case_out_of_bounds"]:
        with pytest.raises(IndexError):
            world.get_entrophy(x, y)
    else:
        # Act
        entropy = world.get_entrophy(x, y)

        # Assert
        assert entropy >= 0


# Continue with similar tests for the other methods in the World class
