from enum import Enum

class Direction(Enum):
    # Made this way for easier logic
    RIGHT = 1
    LEFT = 2
    UP = 4
    DOWN = 5

class Actions(Enum):
    STRAIGHT = 1
    LEFT = 2
    RIGHT = 3
