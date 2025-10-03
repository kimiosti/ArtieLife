"""Module containing the brain implementation."""
from typing import TYPE_CHECKING
from model.entities.living.needs import NeedsTracker, PerceptionTracker
from model.entities.living.brain.attention import Attention, LearningAttention
from model.entities.living.brain.reason import Reason, LearningReason
from controller.log import log_genome

if TYPE_CHECKING:
    from typing import Dict
    from pygame.rect import Rect
    from controller.world.world_controllers import DistanceController
    from utils.living.genome import Gene
    from utils.living.actions import InteractionType

class Brain:
    """Implementation for the living being's central brain lobe. Its function is to
    coordinate the behavior of the `Attention` and `Reason` lobes."""
    def __init__(self, distance_controller: "DistanceController", living_id: "int",
                 genome: "Dict[Gene, float]", learning_enable: "bool") -> "None":
        """Instantiates the living being's central lobe.
        
        Positional arguments:  
         - `distance_controller`: the `DistanceController` tracking the living being's \
        perception of the world's space.
         - `living_id`: the living being's in-game ID.
         - `genome`: the living being's genome.
         - `learning_enable`: a `bool` representing if the living being should learn \
        or act randomly."""
        log_genome(living_id, genome)
        self.perception_tracker = PerceptionTracker(distance_controller)
        self.needs_tracker = NeedsTracker(genome)
        self.attention: "Attention" = \
            LearningAttention(genome) if learning_enable else Attention(genome)
        self.reason: "Reason" = \
            LearningReason(genome) if learning_enable else Reason(genome)

    def update(self, elapsed_time: "float", hitbox: "Rect") -> "bool":
        """Updates the brain, decaying vital parameters.

        Positional arguments:  
         - `elapsed_time`: the amount of time since last brain update, in seconds.
         - `hitbox`: the current position of the living being.

        Return:  
        `True` if the living being is still alive after the update, `False` otherwise."""

        # pylint: disable=locally-disabled, unidiomatic-typecheck
        # Warnings disabled because the behavior of type is the desired behavior, since it allows
        # to distinguish the subclass from the superclass.

        self.perception_tracker.record(hitbox)
        if type(self.attention) is Attention:
            self.attention.update()
        else:
            self.attention.update() # TODO - add relevant arguments
        if type(self.attention) is Reason:
            self.reason.update()
        else:
            self.reason.update() # TODO - add relevant arguments
        return self.needs_tracker.decay(elapsed_time)

    def actuate(self, interaction: "InteractionType") -> "None":
        """Actuates the effect of a given interaction on the living being's needs.
        
        Positional arguments:  
         - `interaction`: the type of the interaction to be made effective."""
        self.needs_tracker.actuate(interaction.get_corresponding_need())
