"""Module containing utilities for living being's needs."""
from typing import TYPE_CHECKING
from enum import Enum
from numpy import inf
from utils.living.genome import Gene

if TYPE_CHECKING:
    from typing import Dict

BASE_HUNGER: "float" = 0
BASE_LIFE: "float" = 0
BASE_TIREDNESS: "float" = 0
MAX_HUNGER: "float" = 100
MAX_TIREDNESS: "float" = 100
MAX_LIFE: "float" = 100

def compute_expected_lifetime(genome: "Dict[Gene, float]") -> "float":
    """Computes the expected lifetime of a given living being, knowing its genome.
    
    Positional arguments:  
     - `genome`: the living being's genome.
    
    Return:  
    A `float` value representing the amount of time the living being is expected to
    live if it took no actions at all."""
    lifetime: "float" = inf
    for need in Need:
        if need not in [Need.LIFE, Need.NONE]:
            lifetime = min(
                lifetime,
                (need.get_threshold() - need.get_base_value())
                    / genome[need.get_corresponding_gene()]
            )
    lifetime += (Need.LIFE.get_threshold() - Need.LIFE.get_base_value()) \
        / genome[Need.LIFE.get_corresponding_gene()]
    return lifetime

class Need(Enum):
    """Enumerative class listing all living being needs."""
    LIFE = 0
    HUNGER = 1
    TIREDNESS = 2
    NONE = 3

    def get_base_value(self) -> "float":
        """Getter for the need's starting value.
        
        Return:  
        The need's starting value as a `float`"""
        match self:
            case Need.LIFE:
                return BASE_LIFE
            case Need.HUNGER:
                return BASE_HUNGER
            case Need.TIREDNESS:
                return BASE_TIREDNESS
            case _:
                return 0

    def get_corresponding_gene(self) -> "Gene":
        """Translates a need in the gene representing the corresponding decay rate.
        
        Return:  
        The `Gene` representing the need's decay rate."""
        match self:
            case Need.LIFE:
                return Gene.LIFE_DECAY
            case Need.HUNGER:
                return Gene.HUNGER_DECAY
            case Need.TIREDNESS:
                return Gene.TIREDNESS_DECAY
            case _:
                return Gene.LIFE_DECAY # default value that should never be accessed.

    def get_threshold(self) -> "float":
        """Getter for a need's limit value.

        When `HUNGER` or `TIREDNESS` reach this value, they are considered to be saturated,  
        meaning that the individual starts hurting.  
        When `LIFE` reaches this value, the individual dies.
        
        Return:  
        The need's limit value as a `float`."""
        match self:
            case Need.LIFE:
                return MAX_LIFE
            case Need.HUNGER:
                return MAX_HUNGER
            case Need.TIREDNESS:
                return MAX_TIREDNESS
            case _:
                return 0
