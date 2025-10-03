"""Module containing living being's implementation."""
from typing import TYPE_CHECKING
from controller.world.world_controllers import ActionsController, DistanceController
from model.entities.non_living import Entity
from model.entities.living.brain.central import Brain
from utils.living.actions import Action, InteractionType
from utils.living.genome import Gene

if TYPE_CHECKING:
    from typing import Dict
    from pygame.rect import Rect
    from controller.game_controller import GameController

class LivingBeing(Entity):
    """Implementation of the game's living beings."""
    def __init__(self, hitbox: "Rect", genome: "Dict[Gene, float]",
                 game_controller: "GameController", living_id: "int",
                 learning_enable: "bool") -> "None":
        """Instantiates a living being.
        
        Positional arguments:  
         - `hitbox`: the initial hitbox for the living being.
         - `genome`: the living being's genome.
         - `game_controller`: the game world controller.
         - `living_id`: the in-game living being identifier.
         - `learning_enable`: a `bool` representing if the living being should learn or \
        act randomly."""
        super().__init__(hitbox)
        self.controller = ActionsController(game_controller)
        self.genome = genome
        self.brain: "Brain" = Brain(
            DistanceController(game_controller),
            living_id,
            self.genome,
            learning_enable
        )
        self.selected: "bool" = False
        self.game_id = living_id

    def compute_movement(self, movement: "float", elapsed_time: "float") -> "float":
        """Computes the living being direction along one axis, given a movement and
        the living being's speed multiplier.
        
        Positional arguments:  
         - `movement`: the base value of the desired movement along the axis.
         - `elapsed_time`: the amount of time elapsed since last update.
        
        Return:  
        A `float` representing how much has the living being moved along the desired axis.
        The sign of the returned value is consistent with the game world coordinates, and
        dictates the direction of the movement."""
        return self.genome[Gene.SPEED] * elapsed_time * movement

    def update(self, elapsed_time: "float") -> "bool":
        """Performs a single update step for the living being, actuating its eventual action.
        
        Positional arguments:  
         - `elapsed_time`: the amount of time elapsed since last update, in seconds.
        
        Return:  
        `True` if the living being is still alive after the update step, `False` otherwise."""
        action: "Action" = self.brain.reason.action

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
