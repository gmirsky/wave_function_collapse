"""
Class Stack
"""


# pylint: disable=C0103
class Stack:
    """
    Class Stack
    """

    def __init__(self):
        """
        Constructor for Class Stack
        """
        self.items = []

    def is_empty(self):
        """
        Returns True if the stack is empty
        """
        return len(self.items) == 0

    def push(self, item):
        """
        Pushes an item to the stack
        """
        self.items.append(item)

    def pop(self):
        """
        Pops an item from the stack
        """
        if not self.is_empty():
            return self.items.pop()

        raise ValueError("pop from empty stack")

    def size(self):
        """
        Returns the size of the stack
        """
        return len(self.items)
