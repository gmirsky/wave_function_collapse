"""Unit tests for Stack."""

import pytest

from class_stack import Stack


def test_stack_starts_empty():
    """A new stack has no items."""
    stack = Stack()
    assert stack.is_empty() is True
    assert stack.size() == 0


def test_push_updates_size_and_empty_state():
    """Pushing items grows the stack."""
    stack = Stack()
    stack.push("a")
    stack.push("b")

    assert stack.is_empty() is False
    assert stack.size() == 2


def test_pop_returns_last_pushed_item():
    """Stack uses LIFO semantics."""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    popped = stack.pop()

    assert popped == 3
    assert stack.size() == 2


def test_pop_empty_stack_raises_value_error():
    """Popping from an empty stack raises a helpful error."""
    stack = Stack()
    with pytest.raises(ValueError, match="pop from empty stack"):
        stack.pop()
