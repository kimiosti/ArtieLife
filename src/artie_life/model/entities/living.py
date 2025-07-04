"""Module containing living being's implementation."""
from typing import TYPE_CHECKING
from numpy.random import randint
from model.entities.non_living import Entity
from model.entities.brain import Brain
from utils import Action, InteractionType, LIVING_BASE_SPEED

if TYPE_CHECKING:
    from pygame.rect import Rect
    from controller.world.world_controllers import ActionsController

class LivingBeing(Entity):
    """Living being implementation, for characters."""
    def __init__(self, hitbox: "Rect", controller: "ActionsController") -> "None":
        """Instantiates a living being.
        
        Arguments:  
        `hitbox`: the initial hitbox for the living being."""
        super().__init__(hitbox)
        self.controller = controller
        self.speed: "float" = LIVING_BASE_SPEED
        self.brain: "Brain" = Brain()

    def compute_movement(self, movement: "float", elapsed_time: "int") -> "float":
        """Computes the living being direction along one axis, given a movement and
        the living being's speed multiplier.
        
        Arguments:  
        `movement`: the base value of the desired movement along the axis.  
        `elapsed_time`: the amount of time elapsed since last update."""
        return self.speed * elapsed_time * movement

    def update(self, elapsed_time: "int") -> "None":
        """Updates the living being, performing the desired action.
        
        Arguments:  
        `elapsed_time`: the amount of time elapsed since last update."""
        action_idx = randint(5)
        action: "Action" = Action.INTERACT
        for item in Action:
            if item.value == action_idx:
                action = item

        if action != Action.INTERACT:
            move_x, move_y = action.get_direction()
            moved_hitbox = self.hitbox.move(
                self.compute_movement(move_x, elapsed_time),
                self.compute_movement(move_y, elapsed_time)
            )
            if self.controller.can_move(moved_hitbox, id(self)):
                self.hitbox = moved_hitbox
        else:
            interaction: "InteractionType" = self.controller.interact(self.hitbox, id(self))
            self.brain.actuate(interaction)
