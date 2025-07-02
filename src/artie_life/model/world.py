"""Module containing the game world's implementation."""
from typing import Tuple, Dict, List
from pygame import Rect
from model.entities.entities import Playground, InteractiveSpot, LivingBeing
from utils import EntityType

class World:
    """Implementation for the game world."""
    def __init__(self) -> None:
        """Instantiates the game world."""
        interactive_spot_width: float = 30.0
        interactive_spot_height: float = 30.0
        self.dimension: Tuple[float, float] = (320.0, 200.0)
        self.playground: Playground = Playground(Rect(110.0, 68.75, 100.0, 62.5))
        self.interactive_spots: Dict[EntityType, List[InteractiveSpot]] = {
            EntityType.FEEDING: [
                InteractiveSpot(Rect(30.0, 30.0, interactive_spot_width, interactive_spot_height)),
                InteractiveSpot(Rect(260.0, 140.0, interactive_spot_width, interactive_spot_height))
            ],
            EntityType.HEALING: [
                InteractiveSpot(Rect(30.0, 85.0, interactive_spot_width, interactive_spot_height)),
                InteractiveSpot(Rect(260.0, 85.0, interactive_spot_width, interactive_spot_height))
            ],
            EntityType.RESTING: [
                InteractiveSpot(Rect(30.0, 140.0, interactive_spot_width, interactive_spot_height)),
                InteractiveSpot(Rect(260.0, 30.0, interactive_spot_width, interactive_spot_height))
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
