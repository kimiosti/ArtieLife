"""Module containing map generation utilities."""
from typing import TYPE_CHECKING
from pygame.rect import Rect
from model.entities.non_living import Playground, InteractiveSpot
from utils.living.actions import EntityType
from utils.map.constants import MAP_WIDTH, MAP_HEIGHT, PLAYGROUND_WIDTH, PLAYGROUND_HEIGHT, \
        SPOT_TO_SIDE_OFFSET, SPOT_WIDTH, SPOT_HEIGHT

if TYPE_CHECKING:
    from typing import Dict, List

def init_playground() -> "Playground":
    """Initializes the map's playground."""
    return Playground(Rect(
        (MAP_WIDTH - PLAYGROUND_WIDTH) / 2,
        (MAP_HEIGHT - PLAYGROUND_HEIGHT) / 2,
        PLAYGROUND_WIDTH,
        PLAYGROUND_HEIGHT
    ))

def init_interactive_spots() -> "Dict[EntityType, List[InteractiveSpot]]":
    """Initializes the map's interactive spots."""
    return {
        EntityType.FEEDING: [
            InteractiveSpot(Rect(
                SPOT_TO_SIDE_OFFSET,
                SPOT_TO_SIDE_OFFSET,
                SPOT_WIDTH,
                SPOT_HEIGHT
            )),
            InteractiveSpot(Rect(
                MAP_WIDTH - SPOT_TO_SIDE_OFFSET - SPOT_WIDTH,
                MAP_HEIGHT - SPOT_TO_SIDE_OFFSET - SPOT_HEIGHT,
                SPOT_WIDTH,
                SPOT_HEIGHT
            ))
        ],
        EntityType.HEALING: [
            InteractiveSpot(Rect(
                SPOT_TO_SIDE_OFFSET,
                (MAP_HEIGHT / 2) - (SPOT_HEIGHT / 2),
                SPOT_WIDTH,
                SPOT_HEIGHT
            )),
            InteractiveSpot(Rect(
                MAP_WIDTH - SPOT_TO_SIDE_OFFSET - SPOT_WIDTH,
                (MAP_HEIGHT / 2) - (SPOT_HEIGHT / 2),
                SPOT_WIDTH,
                SPOT_HEIGHT
            ))
        ],
        EntityType.RESTING: [
            InteractiveSpot(Rect(
                SPOT_TO_SIDE_OFFSET,
                MAP_HEIGHT - SPOT_TO_SIDE_OFFSET - SPOT_HEIGHT,
                SPOT_WIDTH,
                SPOT_HEIGHT
            )),
            InteractiveSpot(Rect(
                MAP_WIDTH - SPOT_TO_SIDE_OFFSET - SPOT_WIDTH,
                SPOT_TO_SIDE_OFFSET,
                SPOT_WIDTH,
                SPOT_HEIGHT
            ))
        ]
    }
