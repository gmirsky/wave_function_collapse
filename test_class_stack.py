"""
In these tests:

The test_stack_size function tests the size method of the Stack class.
It checks whether the size of the stack is as expected after pushing a
number of items onto it.

The test_stack_is_empty function tests the is_empty method of the Stack
class. It checks whether the stack is empty or not after pushing a number
of items onto it.

The test_stack_pop function tests the pop method of the Stack class.
It checks whether the item popped from the stack is as expected.

The test_pop_from_empty_stack function is an edge case test that
checks whether the pop method raises a ValueError when trying to pop
from an empty stack.
"""
import pytest
from class_stack import Stack


@pytest.mark.parametrize(
    "items,expected_size",
    [
        ([], 0, "empty_stack"),
        ([1], 1, "single_item_stack"),
        ([1, 2, 3], 3, "multiple_items_stack"),
    ],
)
def test_stack_size(items, expected_size):
    """
    Test the size method of the Stack class.
    """
    # Arrange
    stack = Stack()
# sourcery skip: no-loop-in-tests
    for item in items:
        stack.push(item)

    # Act
    size = stack.size()

    # Assert
    assert size == expected_size


@pytest.mark.parametrize(
    "items,expected_is_empty",
    [
        ([], True, "empty_stack"),
        ([1], False, "single_item_stack"),
        ([1, 2, 3], False, "multiple_items_stack"),
    ],
)
def test_stack_is_empty(items, expected_is_empty):
    """
    Test the is_empty method of the Stack class.
    """
    # Arrange
    stack = Stack()
# sourcery skip: no-loop-in-tests
    for item in items:
        stack.push(item)

    # Act
    is_empty = stack.is_empty()

    # Assert
    assert is_empty == expected_is_empty


@pytest.mark.parametrize(
    "items,expected_item",
    [
        ([1], 1, "single_item_stack"),
        ([1, 2, 3], 3, "multiple_items_stack"),
    ],
)
def test_stack_pop(items, expected_item):
    """
    Test the pop method of the Stack class.
    """
    # Arrange
    stack = Stack()
# sourcery skip: no-loop-in-tests
    for item in items:
        stack.push(item)

    # Act
    item = stack.pop()

    # Assert
    assert item == expected_item


# Edge case tests
def test_pop_from_empty_stack():
    """
    Test the pop method of the Stack class when trying to pop from an
    empty stack.
    """
    # Arrange
    stack = Stack()

    # Act & Assert
    with pytest.raises(ValueError, match="pop from empty stack"):
        stack.pop()
