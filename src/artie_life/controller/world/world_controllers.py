"""Module containing all world controllers implementation."""
from typing import TYPE_CHECKING
from numpy import sqrt
from pygame import Vector2
from pygame.rect import Rect
from utils.map.constants import MAP_WIDTH, MAP_HEIGHT
from utils.living.actions import EntityType, InteractionType

if TYPE_CHECKING:
    from typing import Dict, Tuple
    from controller.game_controller import GameController

class ActionsController:
    """Implementation for the game's movement controller."""
    def __init__(self, controller: "GameController") -> "None":
        """Instantiates a movement controller.
        
        Positional arguments:  
         - `controller`: the `GameController` handling the world."""
        self.controller: "GameController" = controller
        self.map: "Rect" = Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)

    def can_move(self, hitbox: "Rect", entity_id: "int") -> "bool":
        """Checks if a given living being can move.
        
        Positional arguments:  
         - `hitbox`: the new position of the living being, to be checked for obstruction.  
         - `entity_id`: the moving living being's object ID, to avoid self-checking.
        
        Return:  
        `True` if the indicated hitbox's position is valid, `False` otherwise."""
        if self.map.contains(hitbox):
            for entity_type, entity in self.controller.get_all_entities():
                if id(entity) != entity_id \
                        and not entity_type.walkable() \
                        and entity.is_colliding(hitbox):
                    return False
            return True
        return False

    def interact(self, hitbox: "Rect", entity_id: "int") -> "InteractionType":
        """Checks if a given living being can interact.
        
        Positional arguments:  
         - `hitbox`: the hitbox of the living being requesting the interaction.
         - `entity_id`: the living being's object ID, to avoid self-checking.
        
        Return:  
        If the living being can interact, the corresponding `InteractionType`.  
        Otherwise, `InteractionType.NONE` is returned."""
        for entity_type, entity in self.controller.get_all_entities():
            if id(entity) != entity_id \
                    and entity.is_colliding(hitbox):
                return entity_type.get_interaction()
        return InteractionType.NONE


class DistanceController:
    """Implementation for the distance controller."""
    def __init__(self, controller: "GameController") -> "None":
        """Instantiates a distance controller.
        
        Positional arguments:  
         - `controller`: the current game world's controller."""
        self.controller = controller

    def get_distance_by_type(self, hitbox: "Rect") -> "Dict[EntityType, Tuple[float, float]]":
        """Computes the distance of a given hitbox from the closest instances of all
        game entity types, grouping the result by type.
        
        Arguments:  
        `hitbox`: the living being's current hitbox.
        
        Returns:  
        Given a living being's hitbox, it computes the distance to the closest instance
        of each `EntityType`. Those distances are then expressed as `Tuple` indicating
        the two dimensions' distance."""
        distances: "Dict[EntityType, Tuple[float, float]]" = { }
        for cur_entity_type in EntityType:
            if cur_entity_type != EntityType.PLAYGROUND:
                min_dist = sqrt(MAP_WIDTH**2 + MAP_HEIGHT**2)
                min_x: "float" = MAP_WIDTH
                min_y: "float" = MAP_HEIGHT
                for entity_type, entity in self.controller.get_all_entities():
                    if entity_type == cur_entity_type and entity.hitbox is not hitbox:
                        if entity.hitbox.colliderect(hitbox):
                            min_x = 0
                            min_y = 0
                            min_dist = 0
                        else:
                            dist = Vector2(entity.hitbox.center).distance_to(hitbox.center)
                            if dist < min_dist:
                                min_x = entity.hitbox.centerx - hitbox.centerx
                                min_y = entity.hitbox.centery - hitbox.centery
                                min_dist = dist
                distances[cur_entity_type] = (min_x, min_y)
        return distances
