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
        
        Arguments:  
        `controller`: the `GameController` handling the world."""
        self.controller: "GameController" = controller
        self.map: "Rect" = Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)

    def can_move(self, hitbox: "Rect", entity_id: "int") -> "bool":
        """Checks if a given living being can move.
        
        Arguments:  
        `hitbox`: the new position of the living being, to be checked for obstruction.  
        `entity_id`: the moving living being's object ID, to avoid self-checking."""
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
        
        Arguments:  
        `hitbox`: the hitbox of the living being requesting the interaction.  
        `entity_id`: the living being's object ID, to avoid self-checking."""
        for entity_type, entity in self.controller.get_all_entities():
            if id(entity) != entity_id \
                    and entity.is_colliding(hitbox):
                return entity_type.get_interaction()
        return InteractionType.NONE


class DistanceController:
    """Implementation for the distance controller."""
    def __init__(self, controller: "GameController") -> "None":
        """Instantiates a distance controller."""
        self.controller = controller

    def get_distance_by_type(self, hitbox: "Rect") -> "Dict[EntityType, Tuple[float, float]]":
        """Computes the distance of a given hitbox to the closest instance of
        each type of entity on map.
        
        Arguments:  
        `hitbox`: the hitbox used to compute the distances.
        
        Returns:  
        A `Dict` containing `float` values described by `str` as identifiers."""
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
