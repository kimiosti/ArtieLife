"""Module containing living being's implementation."""
from typing import TYPE_CHECKING
from model.entities.non_living import Entity
from model.entities.living.brain import Brain
from utils import Action, InteractionType, LIVING_BASE_SPEED

if TYPE_CHECKING:
    from pygame.rect import Rect
    from controller.world.world_controllers import ActionsController, DistanceController

class LivingBeing(Entity):
    """Living being implementation, for characters."""
    def __init__(self, hitbox: "Rect", action_controller: "ActionsController",
                 distance_controller: "DistanceController", living_id: "int") -> "None":
        """Instantiates a living being.
        
        Arguments:  
        `hitbox`: the initial hitbox for the living being.  
        `controller`: the `ActionsController` for the living being's actions actuation.  
        `id`: the in-game living being identifier."""
        super().__init__(hitbox)
        self.controller = action_controller
        self.speed: "float" = LIVING_BASE_SPEED
        self.brain: "Brain" = Brain(distance_controller, living_id)
        self.selected: "bool" = False
        self.game_id = living_id

    def compute_movement(self, movement: "float", elapsed_time: "int") -> "float":
        """Computes the living being direction along one axis, given a movement and
        the living being's speed multiplier.
        
        Arguments:  
        `movement`: the base value of the desired movement along the axis.  
        `elapsed_time`: the amount of time elapsed since last update."""
        return self.speed * elapsed_time * movement

    def update(self, elapsed_time: "int") -> "bool":
        """Updates the living being, performing the desired action.
        
        Arguments:  
        `elapsed_time`: the amount of time elapsed since last update.
        
        Returns:  
        A `bool` representing whether the living being is still alive."""
        action: "Action" = self.brain.get_action()

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
        return self.brain.update(elapsed_time, self.hitbox)
