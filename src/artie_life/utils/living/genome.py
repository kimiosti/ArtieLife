"""Module containing utilities for genome."""
from typing import TYPE_CHECKING
from enum import Enum, auto

if TYPE_CHECKING:
    from typing import Dict, Tuple

MUTATION_RATE: "float" = 0.05

class Gene(Enum):
    """Enumerative class listing all genes."""
    LIFE_DECAY = auto()
    HUNGER_DECAY = auto()
    TIREDNESS_DECAY = auto()
    MATING_DRIVE_DECAY = auto()
    SPEED = auto()
    ATTENTION_ALPHA = auto()
    ATTENTION_DECISION_PERIOD = auto()
    ATTENTION_USER_REWARD_MULTIPLIER = auto()
    ATTENTION_SELF_REWARD_MULTIPLIER = auto()

    def min(self) -> "float":
        """Returns the minimum possible value for a given gene."""
        return THRESHOLDS[self][0]

    def max(self) -> "float":
        """Returns the maximum possible value for a given gene."""
        return THRESHOLDS[self][1]


THRESHOLDS: "Dict[Gene, Tuple[float, float]]" = {
    Gene.LIFE_DECAY: (2, 5),
    Gene.HUNGER_DECAY: (3, 7),
    Gene.TIREDNESS_DECAY: (3, 7),
    Gene.MATING_DRIVE_DECAY: (2, 5),
    Gene.SPEED: (45, 80),
    Gene.ATTENTION_ALPHA: (1e-6, 1e-1),
    Gene.ATTENTION_GAMMA: (1e-2, 1),
    Gene.ATTENTION_DECISION_PERIOD: (1, 2),
    Gene.ATTENTION_USER_REWARD_MULTIPLIER: (0.8, 3),
    Gene.ATTENTION_SELF_REWARD_MULTIPLIER: (0.2, 0.6)
}
