"""Module containing utilities for genome."""
from typing import TYPE_CHECKING
from enum import Enum, auto

if TYPE_CHECKING:
    from typing import Dict, Tuple

MUTATION_RATE: "float" = 0.1

class Gene(Enum):
    """Enumerative class listing all genes."""
    LIFE_DECAY = auto()
    HUNGER_DECAY = auto()
    TIREDNESS_DECAY = auto()
    SPEED = auto()
    ATTENTION_GAMMA = auto()
    ATTENTION_LEARNING_RATE = auto()
    ATTENTION_STARTING_EPSILON = auto()
    ATTENTION_EPSILON_DECAY = auto()
    ATTENTION_MIN_EPSILON = auto()
    ATTENTION_UPDATE_PERIOD = auto()
    ATTENTION_TARGET_UPDATE_PERIOD = auto()
    REASON_GAMMA = auto()
    REASON_LEARNING_RATE = auto()
    REASON_STARTING_EPSILON = auto()
    REASON_EPSILON_DECAY = auto()
    REASON_MIN_EPSILON = auto()
    REASON_UPDATE_PERIOD = auto()
    REASON_TARGET_UPDATE_PERIOD = auto()

    def min(self) -> "float":
        """Returns the minimum possible value for a given gene."""
        return THRESHOLDS[self][0]

    def max(self) -> "float":
        """Returns the maximum possible value for a given gene."""
        return THRESHOLDS[self][1]


THRESHOLDS: "Dict[Gene, Tuple[float, float]]" = {
    Gene.LIFE_DECAY: (0.5, 3),
    Gene.HUNGER_DECAY: (0.8, 4),
    Gene.TIREDNESS_DECAY: (0.8, 4),
    Gene.SPEED: (45, 80),
    Gene.ATTENTION_GAMMA: (0.8, 0.99),
    Gene.ATTENTION_LEARNING_RATE: (1e-5, 0.1),
    Gene.ATTENTION_STARTING_EPSILON: (0.95, 1),
    Gene.ATTENTION_EPSILON_DECAY: (0.98, 0.999),
    Gene.ATTENTION_MIN_EPSILON: (0.05, 0.2),
    Gene.ATTENTION_UPDATE_PERIOD: (0.8, 2),
    Gene.ATTENTION_TARGET_UPDATE_PERIOD: (2, 5),
    Gene.REASON_GAMMA: (0.8, 0.99),
    Gene.REASON_LEARNING_RATE: (1e-5, 0.1),
    Gene.REASON_STARTING_EPSILON: (0.95, 1),
    Gene.REASON_EPSILON_DECAY: (0.98, 0.999),
    Gene.REASON_MIN_EPSILON: (0.05, 0.2),
    Gene.REASON_UPDATE_PERIOD: (0.8, 2),
    Gene.REASON_TARGET_UPDATE_PERIOD: (2, 5)
}
