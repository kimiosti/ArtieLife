"""Module containing the main game view implementation"""
from typing import TYPE_CHECKING
from pygame.rect import Rect
from pygame.display import set_mode, flip
from pygame.surface import Surface
from pygame.color import Color
from pygame.font import Font
from utils import EntityType, MAP_WIDTH, MAP_HEIGHT, BG_TO_SCREEN_HEIGHT_RATIO, \
        MAP_WTH_RATIO, TOP_BLANK_TO_SCREEN_RATIO

if TYPE_CHECKING:
    from typing import List, Tuple

class GameView:
    """Implementation of the main Game View class"""
    def __init__(self) -> "None":
        """Instantiates the game view."""
        self.screen: "Surface"
        self.map: "Rect" = Rect(0, 0, 0, 0)
        self.spawn_button: "Rect"
        self.font: "Font" = Font("resources/font/game_font.ttf", 24)

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

    def render_sprite(self, rect: "Rect", color: "Color") -> "None":
        """Renders a single sprite, starting from its game coorinates.
        
        Arguments:  
        `rect`: the game coordinates of the sprite to be rendered.
        `color`: the color used to fill the sprite rectangle. TEMPORARY"""
        graphic_rect: "Rect" = self.game_to_view_coordinates(rect)
        surf: "Surface" = Surface(size=(graphic_rect.width, graphic_rect.height))
        surf.fill(color)
        self.screen.blit(surf, graphic_rect)

    def render(self, sprites: "List[Tuple[EntityType, Rect]]") -> "None":
        """Renders a game scene.
        
        Arguments:  
        `world`: instance of the game world. TEMPORARY"""
        screen_height: "int" = self.screen.get_height()
        screen_width: "int" = self.screen.get_width()

        bg_height = screen_height * BG_TO_SCREEN_HEIGHT_RATIO
        bg_width = bg_height * MAP_WTH_RATIO
        bg_y = screen_height * TOP_BLANK_TO_SCREEN_RATIO
        bg_x = (screen_width - bg_width) / 2
        self.map = Rect(bg_x, bg_y, bg_width, bg_height)

        button_surf = self.font.render("SPAWN NEW CREATURE", True, Color(255, 0, 0))
        self.spawn_button = self.screen.blit(
            button_surf,
            (screen_width / 2 - button_surf.get_width() / 2, self.map.top / 2)
        )

        bg: "Surface" = Surface(size=(self.map.width, self.map.height))
        bg.fill(Color(255,255,255))
        self.screen.blit(bg, self.game_to_view_coordinates(Rect(0, 0, MAP_WIDTH, MAP_HEIGHT)))

        for sprite_type, sprite in sprites:
            self.render_sprite(
                sprite,
                Color(0, 0, 0) if sprite_type == EntityType.PLAYGROUND else (
                    Color(255, 0, 0) if sprite_type == EntityType.FEEDING else (
                        Color(0, 255, 0) if sprite_type == EntityType.HEALING else (
                            Color(0, 0, 255) if sprite_type == EntityType.RESTING else \
                            Color(255, 255, 0)
                        )
                    )
                )
            )

        flip()
