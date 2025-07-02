"""Module containing the game world's implementation."""
from typing import Tuple, Dict, List
from pygame import Rect
from model.entities.entities import Playground, InteractiveSpot, LivingBeing
from utils import EntityType
from utils import MAP_WIDTH
from utils import MAP_HEIGHT
from utils import PLAYGROUND_WIDTH
from utils import PLAYGROUND_HEIGHT
from utils import SPOT_WIDTH
from utils import SPOT_HEIGHT
from utils import SPOT_TO_SIDE_OFFSET
from utils import LIVING_WIDTH
from utils import LIVING_HEIGHT

class World:
    """Implementation for the game world."""
    def __init__(self) -> None:
        """Instantiates the game world."""
        self.dimension: Tuple[float, float] = (MAP_WIDTH, MAP_HEIGHT)
        self.playground: Playground = Playground(Rect(
            (MAP_WIDTH - PLAYGROUND_WIDTH) / 2,
            (MAP_HEIGHT - PLAYGROUND_HEIGHT) / 2,
            PLAYGROUND_WIDTH,
            PLAYGROUND_HEIGHT
        ))
        self.interactive_spots: Dict[EntityType, List[InteractiveSpot]] = {
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
        self.living: List[LivingBeing] = []

    def spawn_living(self) -> None:
        """Spawns a living being inside the playground."""
        colliding: bool = True
        rect: Rect
        while colliding:
            colliding = False
            pos = self.playground.get_random_inner_spot()
            rect = Rect(pos[0], pos[1], LIVING_WIDTH, LIVING_HEIGHT)
            for living in self.living:
                if living.is_colliding(rect):
                    colliding = True
        self.living.append(LivingBeing(rect))
