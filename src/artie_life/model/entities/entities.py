"""Module containing all entities implementations."""
from typing import Tuple
from numpy.random import uniform
from numpy.random import randint
from pygame import Rect
from controller.world.world_controllers import ActionsController
from utils import Action
from utils import LIVING_WIDTH
from utils import LIVING_HEIGHT
from utils import LIVING_BASE_SPEED

class Entity:
    """Base class for entities."""
    def __init__(self, hitbox: Rect) -> None:
        """Instantiates a generic entity.
        
        Arguments:  
        `hitbox`: the entity's hitbox.  
        `walkable`: whether living beings can walk on this entity.  
        `interactive`: whether living beings can interact with this entity."""
        self.hitbox: Rect = hitbox

    def is_colliding(self, hitbox: Rect) -> bool:
        """Checks if the entity is colliding with the given hitbox.
        
        Arguments:  
        `hitbox`: the hitbox to be checked for collision."""
        return self.hitbox.colliderect(hitbox)


class Playground(Entity):
    """Playground implementation."""

    def get_random_inner_spot(self) -> Tuple[float, float]:
        """Returns a random coordinate inside the playground."""
        return (
            uniform(self.hitbox.x, self.hitbox.x + self.hitbox.width - LIVING_WIDTH),
            uniform(self.hitbox.y, self.hitbox.y + self.hitbox.height - LIVING_HEIGHT)
        )


class InteractiveSpot(Entity):
    """Interactive spot implementation."""


class LivingBeing(Entity):
    """Living being implementation, for characters."""
    def __init__(self, hitbox: Rect, controller: ActionsController) -> None:
        """Instantiates a living being.
        
        Arguments:  
        `hitbox`: the initial hitbox for the living being."""
        super().__init__(hitbox)
        self.controller = controller
        self.speed: float = LIVING_BASE_SPEED

    def compute_movement(self, movement: float, elapsed_time: int) -> float:
        return self.speed * elapsed_time * movement

    def update(self, elapsed_time: int) -> None:
        """Updates the living being, performing the desired action.
        
        Arguments:  
        `elapsed_time`: the amount of time since last update."""
        action_idx = randint(5)
        action: Action = Action.INTERACT
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
        elif self.controller.can_interact(self.hitbox, id(self)):
            # TODO - implement interaction
            pass
