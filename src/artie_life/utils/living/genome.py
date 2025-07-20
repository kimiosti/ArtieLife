"""Module containing utilities for genome."""
from enum import Enum
from utils.map import MAP_WIDTH

class Gene(Enum):
    """Enumerative class listing all genes."""
    LIFE_DECAY = 0
    HUNGER_DECAY = 1
    TIREDNESS_DECAY = 2
    MATING_DRIVE_DECAY = 3
    SPEED = 4

    def min(self) -> "float":
        """Returns the minimum possible value for a given gene."""
        match self:
            case Gene.LIFE_DECAY:
                return 5
            case Gene.HUNGER_DECAY:
                return 7
            case Gene.TIREDNESS_DECAY:
                return 7
            case Gene.MATING_DRIVE_DECAY:
                return 5
            case Gene.SPEED:
                return MAP_WIDTH / 7

    def max(self) -> "float":
        """Returns the maximum possible value for a given gene."""
        match self:
            case Gene.LIFE_DECAY:
                return 2
            case Gene.HUNGER_DECAY:
                return 3
            case Gene.TIREDNESS_DECAY:
                return 3
            case Gene.MATING_DRIVE_DECAY:
                return 2
            case Gene.SPEED:
                return MAP_WIDTH / 4
