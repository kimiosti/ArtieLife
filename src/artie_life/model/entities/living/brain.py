"""Module containing the brain implementation."""
from typing import TYPE_CHECKING
from numpy.random import randint
from model.entities.living.needs import NeedsTracker, PerceptionTracker
from controller.log import LivingLogger
from utils.living.needs import BASE_DECISION_RATE
from utils.living.actions import Action, InteractionType

if TYPE_CHECKING:
    from pygame.rect import Rect
    from controller.world.world_controllers import DistanceController

class Brain:
    """Generic implementation for the living beings' brain."""
    def __init__(self, distance_controller: "DistanceController", living_id: "int") -> "None":
        """Instantiates the living being's brain.
        
        Arguments:  
        `distance_controller`: the `DistanceController` tracking the living being's
        perception of the world's space."""
        self.needs_tracker = NeedsTracker(living_id)
        self.perception_tracker = PerceptionTracker(distance_controller, living_id)
        self.time_since_last_decision: "float" = 0
        self.action: "Action" = Action.INTERACT
        self.logger: "LivingLogger" = LivingLogger(living_id)
        self.logger.record_spawn()

    def compute_new_action(self, hitbox: "Rect") -> "None":
        """Computes the next action to be performed."""
        action_idx = randint(5)
        for action in Action:
            if action.value == action_idx:
                self.action = action
        self.needs_tracker.record()
        self.perception_tracker.record(hitbox)
        self.logger.dump_action(self.action)
        self.time_since_last_decision = 0

    def update(self, elapsed_time: "float", hitbox: "Rect") -> "bool":
        """Updates the brain, decaying vital parameters.

        Arguments:  
        `elapsed_time`: the amount of time since last brain update, in seconds.  
        `hitbox`: the current position of the living being.

        Returns:  
        A `bool` representing whether the living being is still alive."""
        self.time_since_last_decision += elapsed_time
        if self.time_since_last_decision >= BASE_DECISION_RATE:
            self.compute_new_action(hitbox)
        return self.needs_tracker.decay(elapsed_time)

    def get_action(self) -> "Action":
        """Gets the next action to be performed by the living being.
        
        Returns:  
        An `Action` value representing the desired action."""
        return self.action

    def actuate(self, interaction: "InteractionType") -> "None":
        """Actuates a given interaction on the living being's vital parameters.
        
        Arguments:  
        `interaction`: the type of the interaction to be made effective."""
        self.needs_tracker.actuate(interaction.get_corresponding_need())
