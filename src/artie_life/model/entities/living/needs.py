"""Module containing the needs tracker's implementation."""
from typing import TYPE_CHECKING
from controller.genetics import compute_fitness
from utils.living.needs import Need
from utils.living.actions import EntityType

if TYPE_CHECKING:
    from typing import Dict, Tuple
    from pygame.rect import Rect
    from controller.world.world_controllers import DistanceController
    from utils.living.genome import Gene

class NeedsTracker:
    """Implementation for the needs tracker of each living being."""
    def __init__(self, genome: "Dict[Gene, float]") -> "None":
        """Instantiates a needs tracker.
        
        Arguments:  
        `genome`: the living being's genome."""
        self.needs: "Dict[Need, float]" = { }
        self.needs_avg: "Dict[Need, float]" = { }
        for need in Need:
            if need != Need.NONE:
                self.needs[need] = need.get_base_value()
                self.needs_avg[need] = 0
        self.observations: "int" = 0
        self.lifetime: "float" = 0
        self.fitness: "float" = 0
        self.genome = genome

    def decay(self, elapsed_time: "float") -> "bool":
        """Actuates a single decay step in all needs.
        
        Positional arguments:  
         - `elapsed_time`: the amount of time elapsed since last step, in seconds.
        
        Return:  
        `True` if the living being is still alive after the decay step, `False` otherwise."""
        for need, value in self.needs.items():
            if (
                need != Need.LIFE
                or self.needs[Need.HUNGER] >= Need.HUNGER.get_threshold()
                or self.needs[Need.TIREDNESS] >= Need.TIREDNESS.get_threshold()
            ):
                new_value = value + (self.genome[need.get_corresponding_gene()] * elapsed_time)
                self.needs[need] = \
                    new_value \
                    if new_value <= need.get_threshold() \
                    else need.get_threshold()
            self.needs_avg[need] = (self.needs_avg[need] * self.observations + value) \
                                   / (self.observations + 1)
        self.observations += 1
        self.lifetime += elapsed_time
        self.fitness = compute_fitness(self.needs_avg)
        return self.needs[Need.LIFE] < Need.LIFE.get_threshold()

    def actuate(self, need: "Need") -> "None":
        """Actuates a given action on the living being's needs.
        
        Arguments:  
         - `need`: the `Need` fulfilled by the desired action."""
        if need != Need.NONE:
            self.needs[need] = need.get_base_value()

    def get_needs(self) -> "Dict[str, float]":
        """Returns the needs' current values in a representable way.
        
        Return:  
        A `Dict` associating to each `Need` name (as a `str`) its current
        value as a `float`."""
        return {
            need.name.lower(): value for need, value in self.needs.items()
        }


class PerceptionTracker:
    """Implementation for the living being's perception tracker."""
    def __init__(self, controller: "DistanceController") -> "None":
        """Instantiates a perception tracker.
        
        Arguments:  
         - `controller`: the distance controller, responsible of calculating the \
        living being's perceived values."""
        self.perception: "Dict[EntityType, Tuple[float, float]]"
        self.perception_avg: "Dict[EntityType, Tuple[float, float]]" = { }
        for entity_type in EntityType:
            if entity_type != EntityType.PLAYGROUND:
                self.perception_avg[entity_type] = (0, 0)
        self.observations: "int" = 0
        self.controller: "DistanceController" = controller

    def record(self, hitbox: "Rect") -> "None":
        """Records an observation of the environment.
        
        Positional arguments:  
         - `hitbox`: the living being's current hitbox."""
        self.perception = self.controller.get_distance_by_type(hitbox)
        for entity_type, values in self.perception.items():
            self.perception_avg[entity_type] = (
                (self.perception_avg[entity_type][0] * self.observations + values[0])
                    / (self.observations + 1),
                (self.perception_avg[entity_type][1] * self.observations + values[1])
                    / (self.observations + 1)
            )
        self.observations += 1
