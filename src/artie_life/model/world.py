"""Module containing the game world's implementation."""
from typing import Tuple, Dict, List
from pygame import Rect
from model.entities.entities import Playground, InteractiveSpot, LivingBeing
from utils import EntityType

class World:
    """Implementation for the game world."""
    def __init__(self) -> None:
        """Instantiates the game world."""
        INTERACTIVE_SPOT_WIDTH: float = 30.0
        INTERACTIVE_SPOT_HEIGHT: float = 30.0
        self.dimension: Tuple[float, float] = (320.0, 200.0)
        self.playground: Playground = Playground(Rect(110.0, 68.75, 100.0, 62.5))
        self.interactive_spots: Dict[EntityType, List[InteractiveSpot]] = {
            EntityType.FEEDING: [
                InteractiveSpot(Rect(30.0, 30.0, INTERACTIVE_SPOT_WIDTH, INTERACTIVE_SPOT_HEIGHT)),
                InteractiveSpot(Rect(260.0, 140.0, INTERACTIVE_SPOT_WIDTH, INTERACTIVE_SPOT_HEIGHT))
            ],
            EntityType.HEALING: [
                InteractiveSpot(Rect(30.0, 85.0, INTERACTIVE_SPOT_WIDTH, INTERACTIVE_SPOT_HEIGHT)),
                InteractiveSpot(Rect(260.0, 85.0, INTERACTIVE_SPOT_WIDTH, INTERACTIVE_SPOT_HEIGHT))
            ],
            EntityType.RESTING: [
                InteractiveSpot(Rect(30.0, 140.0, INTERACTIVE_SPOT_WIDTH, INTERACTIVE_SPOT_HEIGHT)),
                InteractiveSpot(Rect(260.0, 30.0, INTERACTIVE_SPOT_WIDTH, INTERACTIVE_SPOT_HEIGHT))
            ]
        }
        self.living: List[LivingBeing] = []

    def spawn_living(self) -> None:
        """Spawns a living being inside the playground."""
        pos = self.playground.get_random_inner_spot()
        living_being: LivingBeing = LivingBeing(
            Rect(pos[0], pos[1], 10.0, 20.0)
        )
        self.living.append(living_being)
