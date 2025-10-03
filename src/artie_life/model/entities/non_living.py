"""Module containing all non-living entities implementations."""
from typing import TYPE_CHECKING
from numpy.random import uniform
from utils.map.constants import LIVING_WIDTH, LIVING_HEIGHT

if TYPE_CHECKING:
    from typing import Tuple
    from pygame.rect import Rect

class Entity:
    """Base class for entities."""
    def __init__(self, hitbox: "Rect") -> "None":
        """Instantiates a generic entity.
        
        Positional arguments:  
         - `hitbox`: the entity's hitbox."""
        self.hitbox: "Rect" = hitbox

    def is_colliding(self, hitbox: "Rect") -> "bool":
        """Checks if the entity is colliding with the given hitbox.
        
        Positional arguments:  
         - `hitbox`: the hitbox to be checked for collision.
        
        Return:  
        `True` if the two hitboxes collide, `False` otherwise."""
        return self.hitbox.colliderect(hitbox)


class Playground(Entity):
    """Implementation of the playground."""

    def get_random_inner_spot(self) -> "Tuple[float, float]":
        """Computes a random spot inside the playground area.
        
        Return:  
        A `Tuple` of `float` representing the two coordinates in the game world space."""
        return (
            uniform(self.hitbox.x, self.hitbox.x + self.hitbox.width - LIVING_WIDTH),
            uniform(self.hitbox.y, self.hitbox.y + self.hitbox.height - LIVING_HEIGHT)
        )


class InteractiveSpot(Entity):
    """Interactive spot implementation."""
