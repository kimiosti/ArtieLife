"""Module containing implementations for the reason lobes."""
from typing import TYPE_CHECKING
from random import choice
from utils.living.genome import Gene
from utils.living.actions import Action

if TYPE_CHECKING:
    from typing import Dict

class Reason:
    """Implementation of a random-acting reason lobe."""

    def __init__(self, genome: "Dict[Gene, float]") -> "None":
        """Instantiates the reason lobe.
        
        Positional arguments:  
         - `genome`: the living being's genome."""
        self.genome = genome
        self.action: "Action" = choice(list(Action))

    def update(self) -> "None":
        """Performs a single decision step."""
        self.action = choice(list(Action))


class LearningReason(Reason):
    """Implementation of a learning reason lobe."""
    def update(self) -> "None":
        pass
