"""Module containing all entities implementations."""
from typing import Tuple
from numpy.random import uniform
from pygame import Rect
from utils import LIVING_WIDTH
from utils import LIVING_HEIGHT

class Entity:
    """Base class for entities."""
    def __init__(self, hitbox: Rect, walkable: bool, interactive: bool) -> None:
        """Instantiates a generic entity.
        
        Arguments:  
        `hitbox`: the entity's hitbox.  
        `walkable`: whether living beings can walk on this entity.  
        `interactive`: whether living beings can interact with this entity."""
        self.hitbox: Rect = hitbox
        self.walkable: bool = walkable
        self.interactive: bool = interactive

    def get_pos(self) -> Tuple[float, float]:
        """Returns a `Tuple` representing the current entity position."""
        return (self.hitbox.x, self.hitbox.y)

    def is_colliding(self, hitbox: Rect) -> bool:
        """Checks if the entity is colliding with the given hitbox.
        
        Arguments:  
        `hitbox`: the hitbox to be checked for collision."""
        return self.hitbox.colliderect(hitbox)


class Playground(Entity):
    """Playground implementation."""
    def __init__(self, hitbox:Rect) -> None:
        """Instantiates a playground.
        
        Arguments:  
        `hitbox`: the desired playground hitbox."""
        super().__init__(
            hitbox=hitbox,
            walkable=True,
            interactive=False
        )

    def get_random_inner_spot(self) -> Tuple[float, float]:
        """Returns a random coordinate inside the playground."""
        return (
            uniform(self.hitbox.x, self.hitbox.x + self.hitbox.width - LIVING_WIDTH),
            uniform(self.hitbox.y, self.hitbox.y + self.hitbox.height - LIVING_HEIGHT)
        )


class InteractiveSpot(Entity):
    """Interactive spot implementation."""
    def __init__(self, hitbox: Rect):
        """Instantiates an interactive spot.
        
        Arguments:  
        `hitbox`: the interactive spot's hitbox."""
        super().__init__(
            hitbox=hitbox,
            walkable=True,
            interactive=True
        )


class LivingBeing(Entity):
    """Living being implementation, for characters."""
    def __init__(self, hitbox: Rect) -> None:
        """Instantiates a living being.
        
        Arguments:  
        `hitbox`: the initial hitbox for the living being."""
        super().__init__(
            hitbox=hitbox,
            walkable=False,
            interactive=True
        )
        self.speed: float = 1.0
        #self.genome = genome
        #self.speed = genome.speed
        #self.brain = Brain(genome, world)
