"""Module for input controllers implementation."""
from typing import TYPE_CHECKING
from pygame import MOUSEBUTTONDOWN
from pygame.mouse import get_pos as get_mouse_pos

if TYPE_CHECKING:
    from typing import List
    from pygame.event import Event
    from model.world import World
    from view.game_view import GameView

class ClickController:
    """Implementation for the mouse click input controller."""
    def __init__(self, world: "World", view: "GameView") -> "None":
        """Instantiates a click controller."""
        self.world: "World" = world
        self.view: "GameView" = view

    def is_spawn_requested(self, events: "List[Event]") -> "bool":
        """Checks if the user requested a new living being spawn.

        Arguments:  
        `events`: the `List` of `Event` objects recorded since last frame.
        
        Returns:  
        A `bool` representing if the user has requested the spawn action."""
        for event in events:
            if event.type == MOUSEBUTTONDOWN \
                    and self.view.spawn_button.collidepoint(get_mouse_pos()):
                return True
        return False

    def handle_living_selection(self, events: "List[Event]") -> "None":
        """Checks and handles the living being selection process.
        
        Arguments:  
        `events`: the `List` of `Event` objects recorded since last frame."""
        if self.view.map.collidepoint(get_mouse_pos()):
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    for living_being in self.world.living:
                        if self.view.game_to_view_coordinates(living_being.hitbox). \
                                collidepoint(get_mouse_pos()):
                            self.world.select(living_being)
                            return
                    self.world.deselect()
