"""Module containing the game world's implementation."""
from typing import TYPE_CHECKING
from pygame.rect import Rect
from model.entities.non_living import Playground, InteractiveSpot
from model.entities.living.living import LivingBeing
from utils.living.actions import EntityType
from utils.map.generation import init_playground, init_interactive_spots
from utils.map.constants import LIVING_WIDTH, LIVING_HEIGHT
from utils.living.genome import Gene
from utils.logs import start_world_log, log_living_being_stats, \
    start_performance_log, log_frame_performance

if TYPE_CHECKING:
    from typing import Dict, List
    from controller.game_controller import GameController

class World:
    """Implementation for the game world."""
    def __init__(self, controller: "GameController", world_id: "int") -> "None":
        """Instantiates the game world.
        
        Positional arguments:  
         - `controller`: the world's controller.  
         - `world_id`: the world's in-game ID."""
        self.controller: "GameController" = controller
        self.playground: "Playground" = init_playground()
        self.interactive_spots: "Dict[EntityType, List[InteractiveSpot]]" = \
                init_interactive_spots()
        self.living: "List[LivingBeing]" = []
        self.population_size: "int" = 0
        self.world_id = world_id
        self.next_id: "int" = 0
        start_world_log(self.world_id)
        start_performance_log(self.world_id)

    def spawn_living(self, controller: "GameController",
                     genome: "Dict[Gene, float]", learning_enable: "bool") -> "None":
        """Spawns a living being inside the playground.
        
        Positional arguments:  
         - `controller`: the game's world controller.
         - `genome`: the living being's desired genome.
         - `learning_enable`: a `bool` representing if the living being should learn or \
        act randomly."""
        colliding: "bool" = True
        rect: "Rect"
        while colliding:
            colliding = False
            pos = self.playground.get_random_inner_spot()
            rect = Rect(pos[0], pos[1], LIVING_WIDTH, LIVING_HEIGHT)
            for living in self.living:
                if living.is_colliding(rect):
                    colliding = True
        self.next_id += 1
        self.living.append(
            LivingBeing(
                rect,
                genome,
                controller,
                self.next_id,
                learning_enable
            )
        )
        if len(self.living) > self.population_size:
            self.population_size += 1

    def update(self, elapsed_time: "float") -> "None":
        """Updates the game world.
        
        Positional arguments:  
         - `elapsed_time`: the amount of time elapsed since the last model update, in seconds."""
        log_frame_performance(self.world_id, elapsed_time)
        for living_being in self.living:
            alive = living_being.update(elapsed_time)
            if not alive:
                self.living.remove(living_being)
                log_living_being_stats(self.world_id, living_being)
                if len(self.living) < self.population_size:
                    self.controller.spawn_living()

    def deselect(self) -> "None":
        """Deselects the selected creature."""
        for living_being in self.living:
            living_being.selected = False

    def select(self, living_being: "LivingBeing") -> "None":
        """Selects a certain living being to inspect its state and to provide it with  
        input.
        
        Positional arguments:  
         - `living_being`: the living being to be selected."""
        living_being.selected = True

    def send_input(self, text: "str") -> "None":
        """Sends user input to the selected living being.
        
        Positional arguments:  
         - `text`: the user input text."""
        for living_being in self.living:
            if living_being.selected:
                living_being.brain.record_input(text)

    def apply_user_reward(self, reward: "float") -> "None":
        """Applies the user-defined reward to the selected living being.
        
        Positional arguments:  
         - `reward`: the reward to be applied to the living being."""
        for living_being in self.living:
            if living_being.selected:
                living_being.brain.apply_user_reward(reward)

    def dump_current_state(self) -> "None":
        """Dumps the current state of the world."""
        for living_being in self.living:
            log_living_being_stats(self.world_id, living_being)
