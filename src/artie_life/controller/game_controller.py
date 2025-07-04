"""Module containing the main game controller implementation."""
from typing import List
from typing import Tuple
from pygame.rect import Rect
from model.world import World
from utils import EntityType

class GameController:
    """Implementation of the game controller."""
    def __init__(self) -> None:
        """Instantiates a game controller."""
        self.world: World

    def create_world(self) -> None:
        """Creates a new game world."""
        self.world = World()

    def get_map_elems(self) -> List[Tuple[EntityType, Rect]]:
        """Returns all map elements by type.
        
        Returns:  
        A `List` of `Tuples` containing the `EntityType` and the `Rect` representing  
        each entity's hitbox."""
        elems: List[Tuple[EntityType, Rect]] = []
        elems.append((EntityType.PLAYGROUND, self.world.playground.hitbox))

        for ent_type, ents in self.world.interactive_spots.items():
            for entity in ents:
                elems.append((ent_type, entity.hitbox))

        for living in self.world.living:
            elems.append((EntityType.LIVING, living.hitbox))

        return elems
