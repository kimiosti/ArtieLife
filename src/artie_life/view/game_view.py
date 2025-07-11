"""Module containing the main game view implementation"""
from typing import TYPE_CHECKING
from pygame.rect import Rect
from pygame.display import set_mode, flip
from view.resources import ResourceLoader
from utils import MAP_WIDTH, MAP_HEIGHT, BACKGROUND_COLOR, BUTTON_TEXT_COLOR, \
        BG_TO_SCREEN_HEIGHT_RATIO, MAP_WTH_RATIO, TOP_BLANK_TO_SCREEN_RATIO, \
        BOTTOM_TEXT_COLOR

if TYPE_CHECKING:
    from typing import List, Tuple, Dict
    from pygame.surface import Surface
    from utils import EntityType

class GameView:
    """Implementation of the main Game View class"""
    def __init__(self) -> "None":
        """Instantiates the game view."""
        self.screen: "Surface"
        self.map: "Rect" = Rect(0, 0, 0, 0)
        self.spawn_button: "Rect"
        self.resource_loader: "ResourceLoader" = ResourceLoader()

    def show_screen(self) -> "None":
        """Makes the screen visible."""
        self.screen = set_mode()

    def game_to_view_coordinates(self, rect: "Rect") -> "Rect":
        """Converts a set of game coordinates into a set of graphic coordinates.
        
        Arguments:  
        `rect`: the rectangle representing the game coordinates.
        
        Returns:  
        a `Rect` instance representing the new set of coordinates and dimensions."""
        new_x = self.map.left + (rect.left / MAP_WIDTH * self.map.width)
        new_y = self.map.top + (rect.top / MAP_HEIGHT * self.map.height)
        new_width = rect.width / MAP_WIDTH * self.map.width
        new_height = rect.height / MAP_HEIGHT * self.map.height
        return Rect(new_x, new_y, new_width, new_height)

    def render(self, sprites: "List[Tuple[EntityType, Rect]]") -> "None":
        """Renders a game scene.
        
        Arguments:  
        `sprites`: a `List` of `Tuple` objects associating to each sprite type
        its position in game coordinates."""
        self.screen.fill(BACKGROUND_COLOR)
        screen_height: "int" = self.screen.get_height()
        screen_width: "int" = self.screen.get_width()

        bg_height = screen_height * BG_TO_SCREEN_HEIGHT_RATIO
        bg_width = bg_height * MAP_WTH_RATIO
        bg_y = screen_height * TOP_BLANK_TO_SCREEN_RATIO
        bg_x = (screen_width - bg_width) / 2
        self.map = Rect(bg_x, bg_y, bg_width, bg_height)

        button_surf = self.resource_loader.load_text_surface(BUTTON_TEXT_COLOR, "SPAWN NEW CREATURE")
        self.spawn_button = self.screen.blit(
            button_surf,
            (screen_width / 2 - button_surf.get_width() / 2, self.map.top / 2)
        )

        bg: "Surface" = self.resource_loader.load_background(self.map.width, self.map.height)
        self.screen.blit(bg, self.game_to_view_coordinates(Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)))

        for sprite_type, sprite in sprites:
            sprite_rect = self.game_to_view_coordinates(sprite)
            self.screen.blit(
                self.resource_loader.load_sprite(
                    sprite_type,
                    sprite_rect.width,
                    sprite_rect.height
                ),
                (sprite_rect.left, sprite_rect.top)
            )

    def render_bottom_bar(self, params: "Dict[str, float]") -> "None":
        """Renders the bottom part of the screen, to show a living being's
        vital parameters when selected.
        
        Arguments:  
        `params`: a dictionary of all the living being's vital parameters, with their name"""
        param_height: int = (self.screen.get_height() - self.map.bottom) // 10
        for param_name, param in params.items():
            param_name_surf = self.resource_loader.load_text_surface(
                BOTTOM_TEXT_COLOR,
                param_name.replace("_", " ").upper()
            )
            self.screen.blit(
                param_name_surf,
                (self.map.left, self.map.bottom + param_height)
            )
            surf_height = param_name_surf.get_height()
            param_val_surf = self.resource_loader.get_level_bar(
                param_name,
                param,
                self.map.width * 0.25,
                surf_height * 0.7
            )
            self.screen.blit(
                param_val_surf,
                (
                    self.map.left + self.map.width * 0.25,
                    self.map.bottom + param_height + surf_height * 0.15)
            )
            param_height += surf_height

    def show_frame(self) -> "None":
        """Displays the next frame, already rendered."""
        flip()
