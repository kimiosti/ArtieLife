"""Module containing resource loading helpers."""
from typing import TYPE_CHECKING
from os.path import join as join_path
from pygame.image import load as load_image
from pygame.transform import smoothscale
from pygame.surface import Surface
from pygame.font import Font
from utils.view import FONT_PATH, BAR_COLORS, SPRITES_PATH, SPRITES_EXTENSION, \
        BACKGROUND_SPRITE_NAME

if TYPE_CHECKING:
    from pygame.color import Color
    from utils.living.actions import EntityType

class ResourceLoader:
    """Implementation for the game's resource loader."""
    def load_font(self, font_size: "int" = 24) -> "Font":
        """Loads the game's font
        
        Arguments:  
        `font_size`: the desired font size."""
        return Font(FONT_PATH, font_size)

    def load_text_surface(self, color: "Color", text: "str",
                          font_size: "int" = 24) -> "Surface":
        """Loads a surface showing the desired text in the game color.
        
        Argumetns:  
        `color`: the desired text color.  
        `text`: the text to be rendered.
        `size`: the desired font size."""
        font: "Font" = self.load_font(font_size)
        return font.render(text, False, color)

    def get_level_bar(self, label: "str", percentage: "float",
                      width: "float", height: "float") -> "Surface":
        """Loads the asset corresponding to the requested level bar.
        
        Arguments:  
        `label`: the `str` representing the level bar type.  
        `percentage`: the current level of the bar.  
        `width`: the desired maximum width of the bar on screen.  
        `height`: the desired height of the bar on screen.
        
        Returns:  
        A `Surface` representing the desired asset."""
        bar_width: "float" = width * (100 - percentage) / 100 \
                if label == "life" else width * percentage / 100
        surf: "Surface" = Surface((bar_width, height))
        surf.fill(BAR_COLORS[label])
        return surf

    def load_sprite(self, entity_type: "EntityType", width: "float",
                    height: "float") -> "Surface":
        """Loads the sprite corresponding to a given entity type.
        
        Arguments:  
        `entity_type`: the type of the entity to be loaded.  
        `width:  the desired resulting width.  
        `height`: the desired resulting height."""
        path = join_path(
            SPRITES_PATH,
            entity_type.name.lower() + SPRITES_EXTENSION
        )
        surf: "Surface" = load_image(path).convert_alpha()
        return smoothscale(surf, (width, height))

    def load_background(self, width: "float", height: "float") -> "Surface":
        """Loads the background's asset.
        
        Arguments:  
        `width`: the desired resulting width.  
        `height`: the desired resulting height."""
        path = join_path(
            SPRITES_PATH,
            BACKGROUND_SPRITE_NAME + SPRITES_EXTENSION
        )
        surf: "Surface" = load_image(path).convert()
        return smoothscale(surf, (width, height))
