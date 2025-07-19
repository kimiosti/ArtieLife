"""Module containing all non-living entities implementations."""
from typing import TYPE_CHECKING
from numpy.random import uniform
from utils.map import LIVING_WIDTH, LIVING_HEIGHT

if TYPE_CHECKING:
    from typing import Tuple
    from pygame.rect import Rect

class Entity:
    """Base class for entities."""
    def __init__(self, hitbox: "Rect") -> "None":
        """Instantiates a generic entity.
        
        Arguments:  
        `hitbox`: the entity's hitbox.  
        `walkable`: whether living beings can walk on this entity.  
        `interactive`: whether living beings can interact with this entity."""
        self.hitbox: "Rect" = hitbox

    def is_colliding(self, hitbox: "Rect") -> "bool":
        """Checks if the entity is colliding with the given hitbox.
        
        Arguments:  
        `hitbox`: the hitbox to be checked for collision."""
        return self.hitbox.colliderect(hitbox)


class Playground(Entity):
    """Playground implementation."""

    def get_random_inner_spot(self) -> "Tuple[float, float]":
        """Returns a random coordinate inside the playground."""
        return (
            uniform(self.hitbox.x, self.hitbox.x + self.hitbox.width - LIVING_WIDTH),
            uniform(self.hitbox.y, self.hitbox.y + self.hitbox.height - LIVING_HEIGHT)
        )


class InteractiveSpot(Entity):
    """Interactive spot implementation."""
