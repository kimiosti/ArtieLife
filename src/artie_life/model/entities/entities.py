"""Module containing all entities implementations."""
from enum import Enum
from typing import Tuple
from numpy.random import uniform
from artie_life.model.entities.collisions import Hitbox
from artie_life.model.world import World

class EntityType(Enum):
    """Enumerative class listing all entity types."""
    LIVING = 0
    HEALING = 1
    FEEDING = 2
    RESTING = 3
    PLAYGROUND = 4

class Entity:
    """Base class for entities."""
    def __init__(self, hitbox: Hitbox, entity_type: EntityType,
                 walkable: bool, interactive: bool) -> None:
        """Instantiates a generic entity.
        
        Arguments:  
        `hitbox`: the entity's hitbox.  
        `entity_type`: the desired entity type.  
        `walkable`: whether living beings can walk on this entity.  
        `interactive`: whether living beings can interact with this entity."""
        self.hitbox: Hitbox = hitbox
        self.entity_type: EntityType = entity_type
        self.walkable: bool = walkable
        self.interactive: bool = interactive

    def get_pos(self) -> Tuple[float, float]:
        """Returns a `Tuple` representing the current entity position."""
        return (self.hitbox.x, self.hitbox.y)

    def is_colliding(self, hitbox: Hitbox) -> bool:
        """Checks if the entity is colliding with the given hitbox.
        
        Arguments:  
        `hitbox`: the hitbox to be checked for collision."""
        return self.hitbox.is_colliding(hitbox)


class Playground(Entity):
    """Playground implementation."""
    def __init__(self, hitbox:Hitbox) -> None:
        """Instantiates a playground.
        
        Arguments:  
        `hitbox`: the desired playground hitbox."""
        super().__init__(
            hitbox=hitbox,
            entity_type=EntityType.PLAYGROUND,
            walkable=True,
            interactive=False
        )

    def get_random_inner_spot(self) -> Tuple[float, float]:
        """Returns a random coordinate inside the playground."""
        return (
            uniform(self.hitbox.x, self.hitbox.x + self.hitbox.width),
            uniform(self.hitbox.y, self.hitbox.y + self.hitbox.height)
        )


class InteractiveSpot(Entity):
    """Interactive spot implementation."""
    def __init__(self, hitbox: Hitbox, entity_type: EntityType):
        """Instantiates an interactive spot.
        
        Arguments:  
        `hitbox`: the interactive spot's hitbox.  
        `entity_type`: the type of the interactive spot. Must be one between `EntityType.FEEDING`,
        `EntityType.HEALING` or `EntityType.RESTING`, otherwise a `TypeError` is raised."""
        if entity_type in [EntityType.LIVING, EntityType.PLAYGROUND]:
            raise TypeError(
                "Entity type cannot be LIVING nor PLAYGROUND."
                + "Consider using the corresponding classes instead."
            )
        super().__init__(
            hitbox=hitbox,
            entity_type=entity_type,
            walkable=True,
            interactive=True
        )


class LivingBeing(Entity):
    """Living being implementation, for characters."""
    def __init__(self, hitbox: Hitbox, world: World) -> None:
        """Instantiates a living being.
        
        Arguments:  
        `hitbox`: the initial hitbox for the living being."""
        super().__init__(
            hitbox=hitbox,
            entity_type=EntityType.LIVING,
            walkable=False,
            interactive=True
        )
        self.speed: float = 1.0
        #self.genome = genome
        #self.speed = genome.speed
        #self.brain = Brain(genome, world)

    def update(self, elapsed_time: int) -> bool:
        """Performs the living being's action, as decided by the brain, actuating the effect based
        on how much time has elapsed.
        
        Arguments:  
        `elapsed_time`: the elapsed time since last update
        
        Returns:  
        a `bool` value representing whether the creature is still alive."""
        #action = self.brain.get_action()
        #perform action using elapsed time if necessary
        #return self.brain.is_alive()
        return True
