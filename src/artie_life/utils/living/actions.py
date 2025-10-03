"""Module containing utilities for living being's actions."""
from typing import TYPE_CHECKING
from enum import Enum
from utils.living.needs import Need

if TYPE_CHECKING:
    from typing import Tuple

class Action(Enum):
    """Enumerative class listing all possible actions."""
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3
    INTERACT = 4

    def get_direction(self) -> "Tuple[float, float]":
        """Computes the action's corresponding movement direction.
        
        Return:  
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
    HEAL = 0
    FEED = 1
    REST = 2
    NONE = 3

    def get_corresponding_need(self) -> "Need":
        """Translates an interaction type in the need that it fulfills.
        
        Return:  
        The desired `Need`. If no `Need` is fulfilled by the input action,
        a fictitious value of `NONE` is returned."""
        for need in Need:
            if self.value == need.value:
                return need
        return Need.NONE


class EntityType(Enum):
    """Enumerative class listing all entity types."""
    HEALING = 0
    FEEDING = 1
    RESTING = 2
    LIVING = 3
    PLAYGROUND = 4

    def walkable(self) -> "bool":
        """Checks if a living being can walk on this entity type."""
        return self != EntityType.LIVING

    def get_interaction(self) -> "InteractionType":
        """Translates itself to the corresponding `InteractionType`, from which
        the affected `Need` can be accessed.
        
        Return:  
        The desired `InteractionType`. If not interactive, it returns a fictitious
        value of `NONE`."""
        for interaction_type in InteractionType:
            if self.value == interaction_type.value:
                return interaction_type
        return InteractionType.NONE
