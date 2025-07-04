"""Module containing enumeratives and other utility values."""
from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from typing import Tuple

# View-related constants
BG_TO_SCREEN_HEIGHT_RATIO: "float" = 5 / 8
TOP_BLANK_TO_SCREEN_RATIO: "float" = 1 / 9

# Map dimension constants
MAP_WIDTH: "float" = 320.0
MAP_HEIGHT: "float" = 200.0
MAP_WTH_RATIO: "float" = MAP_WIDTH / MAP_HEIGHT

# Playground dimension constants
PLAYGROUND_WIDTH: "float" = 120.0
PLAYGROUND_HEIGHT: "float" = 100.0

# Interactive spots dimension and placing contants
SPOT_WIDTH: "float" = 30.0
SPOT_HEIGHT: "float" = 30.0
SPOT_TO_SIDE_OFFSET: "float" = 30.0

# Living being dimension and movement constants
LIVING_WIDTH: "float" = 12.0
LIVING_HEIGHT: "float" = 20.0
LIVING_BASE_SPEED: "float" = 0.1

# Living being vital parameters constants
BASE_HUNGER: "float" = 0
BASE_LIFE: "float" = 100
BASE_TIREDNESS: "float" = 0
BASE_MATING_DRIVE: "float" = 0
BASE_HUNGER_DECAY: "float" = 0.008
BASE_LIFE_DECAY: "float" = -0.008
BASE_TIREDNESS_DECAY: "float" = 0.008
BASE_MATING_DRIVE_DECAY: "float" = 0.007
MAX_HUNGER: "float" = 100
MAX_TIREDNESS: "float" = 100
MIN_LIFE: "float" = 0
BASE_DECISION_RATE: "int" = 100

# Enumerative types
class Action(Enum):
    """Enumerative class listing all possible actions."""
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3
    INTERACT = 4

    def get_direction(self) -> "Tuple[float, float]":
        """Computes the action's corresponding movement direction.
        
        Returns:  
        A `Tuple` containing two `float` values representing the movement along  
        the two axes."""
        x: "float" = 1 if self == Action.RIGHT else (
            -1 if self == Action.LEFT else 0
        )
        y: "float" = 1 if self == Action.DOWN else (
            -1 if self == Action.UP else 0
        )
        return (x, y)


class InteractionType(Enum):
    """Enumerative class listing all possbile interaction results."""
    MATE = 0
    HEAL = 1
    FEED = 2
    REST = 3
    NONE = 4


class EntityType(Enum):
    """Enumerative class listing all entity types."""
    LIVING = 0
    HEALING = 1
    FEEDING = 2
    RESTING = 3
    PLAYGROUND = 4

    def walkable(self) -> "bool":
        """Checks if a living being can walk on the entity type."""
        return self != EntityType.LIVING

    def get_interaction(self) -> "InteractionType":
        """Check if a living being can interact with the entity type."""
        for entity_type in EntityType:
            for interaction_type in InteractionType:
                if entity_type.value == interaction_type.value:
                    return interaction_type
        return InteractionType.NONE
