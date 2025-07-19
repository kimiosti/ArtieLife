"""Module containing utility constants for the game view."""
from typing import TYPE_CHECKING
from os.path import join as join_path
from pygame.color import Color

if TYPE_CHECKING:
    from typing import Dict

BG_TO_SCREEN_HEIGHT_RATIO: "float" = 5 / 8
TOP_BLANK_TO_SCREEN_RATIO: "float" = 1 / 9
FONT_PATH: "str" = "resources/font/jupiteroid.ttf"
RESOURCES_FOLDER: "str" = "resources"
FONT_PATH: "str" = join_path(RESOURCES_FOLDER, "font", "jupiteroid.ttf")
BAR_COLORS: "Dict[str, Color]" = {
    "mating_drive": Color("firebrick2"),
    "tiredness": Color(37, 24, 157),
    "life": Color("green3"),
    "hunger": Color(230, 210, 34)
}
BACKGROUND_COLOR = Color("black")
BUTTON_TEXT_COLOR = Color("firebrick2")
BOTTOM_TEXT_COLOR = Color("white")
SPRITES_PATH: "str" = join_path(RESOURCES_FOLDER, "sprites")
BACKGROUND_SPRITE_NAME: "str" = "background"
SPRITES_EXTENSION: "str" = ".png"
