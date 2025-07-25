"""Module for input controllers implementation."""
from typing import TYPE_CHECKING
from pygame import MOUSEBUTTONDOWN, KEYDOWN, K_RETURN, K_BACKSPACE
from pygame.mouse import get_pos as get_mouse_pos
from utils.living.learning.attention import MAX_INPUT_LENGTH, POSITIVE_REWARD, \
        NEGATIVE_REWARD

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
                    self.world.deselect()
                    for living_being in self.world.living:
                        if self.view.game_to_view_coordinates(living_being.hitbox). \
                                collidepoint(get_mouse_pos()):
                            self.world.select(living_being)

    def handle_user_reward(self, events: "List[Event]") -> "None":
        """
        Checks and handles user-driven rewards.
        
        Arguments:  
        `events`: the list of events recorded since last frame."""
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                if self.view.bottom_bar.pos_reward.collidepoint(get_mouse_pos()):
                    self.world.apply_user_reward(POSITIVE_REWARD)
                elif self.view.bottom_bar.neg_reward.collidepoint(get_mouse_pos()):
                    self.world.apply_user_reward(NEGATIVE_REWARD)

class TextController:
    """Implementation for the text input controller."""
    def __init__(self, world: "World", view: "GameView"):
        """Instantiates a text controller.
        
        Arguments:  
        `world`: the game world.  
        `view`: the game's view."""
        self.world = world
        self.view = view

    def clear(self) -> "None":
        """Clears the text input buffer."""
        self.view.bottom_bar.text = ""

    def update(self, events: "List[Event]") -> "None":
        """Checks for user keyboard input and updates the recorded text.
        
        Arguments:  
        `events`: the list of all events since last update."""
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.view.bottom_bar.text = self.view.bottom_bar.text[:-1]
                elif event.key == K_RETURN:
                    self.world.send_input(self.view.bottom_bar.text)
                    self.clear()
                elif len(self.view.bottom_bar.text) < MAX_INPUT_LENGTH:
                    self.view.bottom_bar.text += event.unicode.upper()
