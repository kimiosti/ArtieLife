"""Module containing all world controllers implementation."""
from typing import TYPE_CHECKING
from pygame.rect import Rect
from utils import MAP_WIDTH
from utils import MAP_HEIGHT

if TYPE_CHECKING:
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

    def can_interact(self, hitbox: "Rect", entity_id: "int") -> "bool":
        """Checks if a given living being can interact.
        
        Arguments:  
        `hitbox`: the hitbox of the living being requesting the interaction.  
        `entity_id`: the living being's object ID, to avoid self-checking."""
        for entity_type, entity in self.controller.get_all_entities():
            if id(entity) != entity_id \
                    and entity_type.interactive() \
                    and entity.is_colliding(hitbox):
                return True
        return False
