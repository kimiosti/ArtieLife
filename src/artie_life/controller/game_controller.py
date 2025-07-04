"""Module containing the main game controller implementation."""
from typing import TYPE_CHECKING
from model.world import World
from controller.world.world_controllers import ActionsController
from utils import EntityType

if TYPE_CHECKING:
    from typing import List
    from typing import Tuple
    from pygame.rect import Rect
    from model.entities.non_living import Entity

class GameController:
    """Implementation of the game controller."""
    def __init__(self) -> "None":
        """Instantiates a game controller."""
        self.world: "World"

    def create_world(self) -> "None":
        """Creates a new game world."""
        self.world = World()

    def spawn_living(self) -> "None":
        """Spawns a new living being in the current game world."""
        self.world.spawn_living(ActionsController(self))

    def get_all_entities(self) -> "List[Tuple[EntityType, Entity]]":
        """Returns all map entities by type.
        
        Returns:  
        A `List` of `Tuples` containing the `EntityType` and the `Entity` object  
        representing each entity."""
        elems: "List[Tuple[EntityType, Entity]]" = []
        elems.append((EntityType.PLAYGROUND, self.world.playground))
        for ent_type, ents in self.world.interactive_spots.items():
            for entity in ents:
                elems.append((ent_type, entity))
        for living in self.world.living:
            elems.append((EntityType.LIVING, living))
        return elems

    def get_map_elems(self) -> "List[Tuple[EntityType, Rect]]":
        """Returns all map entities' hitboxes by type.
        
        Returns:  
        A `List` of `Tuples` containing the `EntityType` and the `Rect` representing  
        each entity's hitbox."""
        return [(entity_type, entity.hitbox) for entity_type, entity in self.get_all_entities()]

    def update_world(self, elapsed_time: "int") -> "None":
        """Updates the current game world.
        
        Arguments:  
        `elapsed_time`: the amount of time elapsed since the last model update."""
        self.world.update(elapsed_time)
