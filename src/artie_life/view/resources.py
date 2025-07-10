"""Module containing resource loading helpers."""
from pygame.surface import Surface
from pygame.font import Font
from utils import FONT_PATH, BAR_COLORS

class ResourceLoader:
    """Implementation for the game's resource loader."""
    def get_game_font(self, size: "int" = 24) -> "Font":
        """Loads the game's font.
        
        Argumetns:  
        `size`: the desired font size."""
        return Font(FONT_PATH, size)

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
