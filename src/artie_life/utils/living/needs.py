"""Module containing utilities for living being's needs."""
from enum import Enum

BASE_HUNGER: "float" = 0
BASE_LIFE: "float" = 0
BASE_TIREDNESS: "float" = 0
BASE_MATING_DRIVE: "float" = 0
BASE_HUNGER_DECAY: "float" = 0.008
BASE_LIFE_DECAY: "float" = 0.008
BASE_TIREDNESS_DECAY: "float" = 0.008
BASE_MATING_DRIVE_DECAY: "float" = 0.007
MAX_HUNGER: "float" = 100
MAX_TIREDNESS: "float" = 100
MAX_MATING_DRIVE: "float" = 100
MAX_LIFE: "float" = 100
BASE_DECISION_RATE: "int" = 100

class Need(Enum):
    """Enumerative class listing all living being needs."""
    LIFE = 1
    HUNGER = 2
    TIREDNESS = 3
    MATING_DRIVE = 0
    NONE = 4

    def get_base_value(self) -> "float":
        """Getter for the need's base value.
        
        Returns:  
        The need's base value as a `float`"""
        match self:
            case Need.MATING_DRIVE:
                return BASE_MATING_DRIVE
            case Need.LIFE:
                return BASE_LIFE
            case Need.HUNGER:
                return BASE_HUNGER
            case Need.TIREDNESS:
                return BASE_TIREDNESS
            case _:
                return 0

    def get_base_decay(self) -> "float":
        """Getter for the base decay rate of a need.
        
        Returns:  
        The need's base decay rate as a `float`."""
        match self:
            case Need.MATING_DRIVE:
                return BASE_MATING_DRIVE_DECAY
            case Need.LIFE:
                return BASE_LIFE_DECAY
            case Need.HUNGER:
                return BASE_HUNGER_DECAY
            case Need.TIREDNESS:
                return BASE_TIREDNESS_DECAY
            case _:
                return 0

    def get_threshold(self) -> "float":
        """Getter for a need's limit value.
        
        Returns:  
        The need's limit value as a `float`."""
        match self:
            case Need.MATING_DRIVE:
                return MAX_MATING_DRIVE
            case Need.LIFE:
                return MAX_LIFE
            case Need.HUNGER:
                return MAX_HUNGER
            case Need.TIREDNESS:
                return MAX_TIREDNESS
            case _:
                return 0
