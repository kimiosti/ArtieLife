"""Module containing enumeratives and other utility values."""
from enum import Enum

# View-related constants
BG_TO_SCREEN_HEIGHT_RATIO: float = 5 / 8
TOP_BLANK_TO_SCREEN_RATIO: float = 1 / 9

# Map dimension constants
MAP_WIDTH: float = 320.0
MAP_HEIGHT: float = 200.0
MAP_WTH_RATIO: float = MAP_WIDTH / MAP_HEIGHT

# Playground dimension constants
PLAYGROUND_WIDTH: float = 120.0
PLAYGROUND_HEIGHT: float = 100.0

# Interactive spots dimension and placing contants
SPOT_WIDTH: float = 30.0
SPOT_HEIGHT: float = 30.0
SPOT_TO_SIDE_OFFSET: float = 30.0

# Living being dimension constants
LIVING_WIDTH: float = 12.0
LIVING_HEIGHT: float = 20.0

# Enumerative types
class Action(Enum):
    """Enumerative class listing all possible actions."""
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3
    INTERACT = 4

class EntityType(Enum):
    """Enumerative class listing all entity types."""
    LIVING = 0
    HEALING = 1
    FEEDING = 2
    RESTING = 3
    PLAYGROUND = 4

    def walkable(self) -> bool:
        """Checks if a living being can walk on the entity type."""
        return self != EntityType.LIVING

    def interactive(self) -> bool:
        """Check if a living being can interact with the entity type."""
        return self != EntityType.PLAYGROUND
