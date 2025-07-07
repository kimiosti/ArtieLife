"""Module containing the game world's implementation."""
from typing import TYPE_CHECKING
from pygame.rect import Rect
from model.entities.non_living import Playground, InteractiveSpot
from model.entities.living import LivingBeing
from utils import EntityType, MAP_WIDTH, MAP_HEIGHT, PLAYGROUND_WIDTH, PLAYGROUND_HEIGHT, \
        SPOT_TO_SIDE_OFFSET, SPOT_WIDTH, SPOT_HEIGHT, LIVING_WIDTH, LIVING_HEIGHT

if TYPE_CHECKING:
    from typing import Tuple, Dict, List
    from controller.game_controller import GameController
    from controller.world.world_controllers import ActionsController

class World:
    """Implementation for the game world."""
    def __init__(self, controller: "GameController") -> "None":
        """Instantiates the game world."""
        self.controller: "GameController" = controller
        self.dimension: "Tuple[float, float]" = (MAP_WIDTH, MAP_HEIGHT)
        self.playground: "Playground" = Playground(Rect(
            (MAP_WIDTH - PLAYGROUND_WIDTH) / 2,
            (MAP_HEIGHT - PLAYGROUND_HEIGHT) / 2,
            PLAYGROUND_WIDTH,
            PLAYGROUND_HEIGHT
        ))
        self.interactive_spots: "Dict[EntityType, List[InteractiveSpot]]" = {
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
        self.living: "List[LivingBeing]" = []
        self.population_size: "int" = 0
        self.next_id: "int" = 0

    def spawn_living(self, controller: "ActionsController") -> "None":
        """Spawns a living being inside the playground.
        
        Arguments:  
        `controller`: the `ActionsController` monitoring the living being's actions."""
        colliding: "bool" = True
        rect: "Rect"
        while colliding:
            colliding = False
            pos = self.playground.get_random_inner_spot()
            rect = Rect(pos[0], pos[1], LIVING_WIDTH, LIVING_HEIGHT)
            for living in self.living:
                if living.is_colliding(rect):
                    colliding = True
        self.living.append(LivingBeing(rect, controller, self.next_id))
        self.next_id += 1
        if len(self.living) > self.population_size:
            self.population_size += 1

    def update(self, elapsed_time: "int") -> "None":
        """Updates the game world.
        
        Arguments:  
        `elapsed_time`: the amount of time elapsed since the last model update."""
        for living_being in self.living:
            alive = living_being.update(elapsed_time)
            if not alive:
                self.living.remove(living_being)
                self.controller.spawn_living()

    def deselect(self) -> "None":
        """Deselects the selected creature."""
        for living_being in self.living:
            living_being.selected = False

    def select(self, living_being: "LivingBeing") -> "None":
        """Selects a certain living being to inspect its state and to provide it with  
        input.
        
        Arguments:  
        `living_being`: the living being to be selected."""
        living_being.selected = True
