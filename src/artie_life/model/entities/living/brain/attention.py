"""Module containing attention lobe implementations."""
from typing import TYPE_CHECKING
from random import choice
from utils.living.genome import Gene
from utils.living.actions import EntityType

if TYPE_CHECKING:
    from typing import Dict

def pick_random_focus() -> "EntityType":
    """Randomly computes a new acceptable value for the entity's focus."""
    next_focus: "EntityType" = choice(list(EntityType))
    while next_focus in [EntityType.LIVING, EntityType.PLAYGROUND]:
        next_focus = choice(list(EntityType))
    return next_focus

class Attention:
    """Implementation of a random-behaving attention lobe."""

    def __init__(self, genome: "Dict[Gene, float]") -> "None":
        """Instantiates the attention lobe.
        
        Positional arguments:  
         - `genome`: the livign being's genome.  
         - `living_id`: the in-game living being's ID."""
        self.genome = genome
        self.focus = pick_random_focus()

    def update(self) -> "None":
        """Performs a single random-behaving attention step."""
        self.focus = pick_random_focus()


class LearningAttention(Attention):
    """Implementation of a learning attention lobe."""
    def update(self) -> "None":
        pass
