"""Module containing the bottom part of the view."""
from typing import TYPE_CHECKING
from pygame.surface import Surface
from pygame.rect import Rect
from view.resources import ResourceLoader
from utils.view import BOTTOM_TEXT_COLOR, REWARD_BUTTON_COLOR, PUNISH_BUTTON_COLOR, \
        INPUT_TEXT_BACKGROUND_COLOR, INPUT_TEXT_COLOR, INPUT_TEXT_SIZE, ATTENTION_LABEL

if TYPE_CHECKING:
    from typing import Dict

class BottomBar:
    """Implementation for the bottom part of the view."""
    def __init__(self) -> "None":
        """Instantiates a bottom bar view element."""
        self.resource_loader = ResourceLoader()
        self.text: "str"
        self.pos_reward: "Rect"
        self.neg_reward: "Rect"

    def render(self, area: "Rect", params: "Dict[str, float]", attention: "str") -> "Surface":
        """Renders a single frame for the bottom bar.

        Positional arguments:  
         - `area`: the area containing the bottom bar on screen.
         - `params`: the living being's vital parameters.
         - `attention`: a string representing the living being's object of attention.

        Return:  
        The `Surface` representing the bottom bar to be rendered on screen.
        """
        surf = Surface((area.width, area.height))
        top_padding = area.height // 10
        side_padding = area.width // 20
        inner_surf = Surface((area.width - (side_padding * 2), area.height - top_padding))

        width = inner_surf.get_width()
        acc_height = 0
        for param_name, param in params.items():
            text_surf = self.resource_loader.load_text_surface(
                BOTTOM_TEXT_COLOR,
                param_name.replace("_", " ").upper()
            )
            inner_surf.blit(text_surf, (0, acc_height))
            bar_surf = self.resource_loader.get_level_bar(
                param_name,
                param,
                width * 0.25,
                text_surf.get_height() * 0.7
            )
            inner_surf.blit(
                bar_surf,
                (width * 0.25, acc_height + text_surf.get_height() * 0.15)
            )
            acc_height += text_surf.get_height()
        inner_surf.blit(
            self.resource_loader.load_text_surface(
                BOTTOM_TEXT_COLOR,
                ATTENTION_LABEL
            ),
            (0, acc_height)
        )
        inner_surf.blit(
            self.resource_loader.load_text_surface(
                BOTTOM_TEXT_COLOR,
                attention
            ),
            (width * 0.25, acc_height)
        )

        self.pos_reward = Rect(
            area.left + side_padding + width * 0.6,
            area.top + top_padding,
            width * 0.15,
            acc_height / len(params)
        )
        pos_surf = Surface((self.pos_reward.width, self.pos_reward.height))
        pos_surf.fill(REWARD_BUTTON_COLOR)
        pos_text = self.resource_loader.load_text_surface(
            BOTTOM_TEXT_COLOR,
            "REWARD",
            INPUT_TEXT_SIZE
        )
        pos_surf.blit(
            pos_text,
            (
                (self.pos_reward.width - pos_text.get_width()) / 2,
                (self.pos_reward.height - pos_text.get_height()) / 2
            )
        )
        inner_surf.blit(pos_surf, (width * 0.6, 0))

        self.neg_reward = Rect(
            area.left + side_padding + width * 0.8,
            area.top + top_padding,
            self.pos_reward.width,
            self.pos_reward.height
        )
        neg_surf = Surface((self.neg_reward.width, self.neg_reward.height))
        neg_surf.fill(PUNISH_BUTTON_COLOR)
        neg_text = self.resource_loader.load_text_surface(
            BOTTOM_TEXT_COLOR,
            "PUNISH",
            INPUT_TEXT_SIZE
        )
        neg_surf.blit(
            neg_text,
            (
                (self.neg_reward.width - neg_text.get_width()) / 2,
                (self.neg_reward.height - neg_text.get_height()) / 2
            )
        )
        inner_surf.blit(neg_surf, (width * 0.8, 0))

        input_bg_surf = Surface((width * 0.25, acc_height / len(params)))
        input_bg_surf.fill(INPUT_TEXT_BACKGROUND_COLOR)
        input_surf = self.resource_loader.load_text_surface(
            INPUT_TEXT_COLOR,
            self.text,
            INPUT_TEXT_SIZE
        )
        input_bg_surf.blit(
            input_surf,
            (
                (input_bg_surf.get_width() - input_surf.get_width()) / 2,
                (input_bg_surf.get_height() - input_surf.get_height()) / 2
            )
        )
        inner_surf.blit(input_bg_surf, (width * 0.65, acc_height / len(params) + top_padding))

        surf.blit(inner_surf,(side_padding, top_padding))
        return surf
