"""Module containing the main game controller implementation."""
from typing import TYPE_CHECKING
from model.world import World
from controller.world.world_controllers import ActionsController, DistanceController
from utils.living.actions import EntityType

if TYPE_CHECKING:
    from typing import List, Tuple, Dict
    from pygame.rect import Rect
    from model.entities.non_living import Entity
    from model.entities.living.living import LivingBeing

class GameController:
    """Implementation of the game controller."""
    def __init__(self) -> "None":
        """Instantiates a game controller."""
        self.world: "World"

    def create_world(self) -> "None":
        """Creates a new game world."""
        self.world = World(self)

    def spawn_living(self) -> "None":
        """Spawns a new living being in the current game world."""
        self.world.spawn_living(ActionsController(self), DistanceController(self))

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

    def is_living_selected(self) -> "bool":
        """Checks if a living being is seleceted.
        
        Returns:  
        A `bool` representing if a living being was selected."""
        for living in self.world.living:
            if living.selected:
                return True
        return False

    def get_selected_info(self) -> "Dict[str, float]":
        """Returns the selected living being's vital parameters.
        
        Returns:  
        A `Dict` containing a `float` value associated to each vital parameter description  
        as a `str`."""
        selected: "LivingBeing"
        for living in self.world.living:
            if living.selected:
                selected = living
        return selected.brain.needs_tracker.get_needs()


    def update_world(self, elapsed_time: "float") -> "None":
        """Updates the current game world.
        
        Arguments:  
        `elapsed_time`: the amount of time elapsed since the last model update, in seconds."""
        self.world.update(elapsed_time)
