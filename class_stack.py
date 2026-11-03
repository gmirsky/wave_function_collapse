"""Small LIFO stack helper used by wave propagation.

The world-collapse routine performs a depth-first style propagation pass after
collapsing one tile. This class keeps that propagation state explicit and easy
to test instead of relying on recursion.
"""


# pylint: disable=C0103
class Stack:
    """Minimal last-in/first-out container."""

    def __init__(self) -> None:
        """Create an empty stack."""
        self.items = []

    def is_empty(self) -> bool:
        """Return ``True`` when there are no items to pop."""
        return len(self.items) == 0

    def push(self, item: object) -> None:
        """Push an item to the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Pop and return the most recently pushed item.

        Raises:
            ValueError: If the stack is empty.
        """
        if not self.is_empty():
            return self.items.pop()

        raise ValueError("pop from empty stack")

    def size(self) -> int:
        """Return the current number of stored items."""
        return len(self.items)
