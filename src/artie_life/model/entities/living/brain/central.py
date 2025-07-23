"""Module containing the brain implementation."""
from typing import TYPE_CHECKING
from numpy import array
from numpy.random import choice
from controller.log import LivingLogger
from model.entities.living.needs import NeedsTracker, PerceptionTracker
from model.entities.living.brain.attention import Attention
from utils.living.actions import Action

if TYPE_CHECKING:
    from typing import Dict
    from pygame.rect import Rect
    from controller.world.world_controllers import DistanceController
    from utils.living.genome import Gene
    from utils.living.actions import InteractionType

class Brain:
    """Generic implementation for the living beings' brain."""
    def __init__(self, distance_controller: "DistanceController", living_id: "int",
                 genome: "Dict[Gene, float]") -> "None":
        """Instantiates the living being's brain.
        
        Arguments:  
        `distance_controller`: the `DistanceController` tracking the living being's
        perception of the world's space.
        `living_id`: the living being's in-game ID.
        `genome`: the living being's genome."""
        self.perception_tracker = PerceptionTracker(distance_controller, living_id)
        self.genome = genome
        self.needs_tracker = NeedsTracker(living_id, self.genome)
        self.action: "Action" = choice(array(Action))
        self.logger: "LivingLogger" = LivingLogger(living_id)
        self.logger.record_spawn(self.genome)
        self.attention: "Attention" = Attention(self.genome)

    def update(self, elapsed_time: "float", hitbox: "Rect") -> "bool":
        """Updates the brain, decaying vital parameters.

        Arguments:  
        `elapsed_time`: the amount of time since last brain update, in seconds.  
        `hitbox`: the current position of the living being.

        Returns:  
        A `bool` representing whether the living being is still alive."""
        self.action: Action = choice(array(Action))
        self.perception_tracker.record(hitbox)
        self.attention.update(elapsed_time, self.perception_tracker.perception)
        self.logger.dump_focus_object(self.attention.focus)
        self.logger.dump_action(self.action)
        return self.needs_tracker.decay(elapsed_time)

    def actuate(self, interaction: "InteractionType") -> "None":
        """Actuates a given interaction on the living being's vital parameters.
        
        Arguments:  
        `interaction`: the type of the interaction to be made effective."""
        self.needs_tracker.actuate(interaction.get_corresponding_need())
