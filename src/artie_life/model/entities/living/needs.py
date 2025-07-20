"""Module containing the needs tracker's implementation."""
from typing import TYPE_CHECKING
from numpy import sqrt
from controller.log import LivingLogger
from utils.living.needs import Need
from utils.living.actions import EntityType

if TYPE_CHECKING:
    from typing import Dict, Tuple
    from pygame.rect import Rect
    from controller.world.world_controllers import DistanceController
    from utils.living.genome import Gene

class NeedsTracker:
    """Implementation for the needs tracker of each living being."""
    def __init__(self, living_id: "int", genome: "Dict[Gene, float]") -> "None":
        """Instantiates a needs tracker.
        
        Arguments:  
        `living_id`: the living being's in-game ID.
        `genome`: the living being's genome."""
        self.needs: "Dict[Need, float]" = { }
        self.needs_avg: "Dict[Need, float]" = { }
        for need in Need:
            if need != Need.NONE:
                self.needs[need] = need.get_base_value()
                self.needs_avg[need] = 0
        self.observations: "int" = 0
        self.logger: "LivingLogger" = LivingLogger(living_id)
        self.genome = genome

    def decay(self, elapsed_time: "float") -> "bool":
        """Actuates a single decay step in all needs.
        
        Arguments:  
        `elapsed_time`: the amount of time elapsed since last step, in seconds.
        
        Returns:  
        A `bool` representing if the living being is still alive."""
        for need, value in self.needs.items():
            if (
                need != Need.LIFE
                or (
                    self.needs[Need.HUNGER] >= Need.HUNGER.get_threshold()
                    and self.needs[Need.TIREDNESS] >= Need.TIREDNESS.get_threshold()
                )
            ):
                new_value = value + (self.genome[need.get_corresponding_gene()] * elapsed_time)
                self.needs[need] = \
                    new_value \
                    if new_value <= need.get_threshold() \
                    else need.get_threshold()
        return self.needs[Need.LIFE] <= Need.LIFE.get_threshold()

    def actuate(self, need: "Need") -> "None":
        """Actuates a given action on the living being's needs.
        
        Arguments:  
        `need`: the need fulfilled by the action to actuate."""
        if need != Need.NONE:
            self.needs[need] = need.get_base_value()

    def record(self) -> "None":
        """Updates the record of the average needs value."""
        for need, value in self.needs.items():
            self.needs_avg[need] = (self.needs_avg[need] * self.observations + value) \
                                   / (self.observations + 1)
        self.observations += 1
        self.logger.dump_observation({
            need.name.lower(): avg for need, avg in self.needs_avg.items()
        })

    def get_needs(self) -> "Dict[str, float]":
        """Getter for the current needs measure.
        
        Returns:  
        A `Dict` containing `float` values for each need, described by a `str` label."""
        return {
            need.name.lower(): value for need, value in self.needs.items()
        }


class PerceptionTracker:
    """Implementation for the living being's perception tracker."""
    def __init__(self, controller: "DistanceController", living_id: "int") -> "None":
        """Instantiates a perception tracker.
        
        Arguments:  
        `controller`: the distance controller, responsible of calculating the
        perceived values.  
        `living_id`: the living being's in-game ID."""
        self.perception: "Dict[EntityType, Tuple[float, float]]"
        self.perception_avg: "Dict[EntityType, Tuple[float, float]]" = { }
        for entity_type in EntityType:
            self.perception_avg[entity_type] = (0, 0)
        self.observations: "int" = 0
        self.controller: "DistanceController" = controller
        self.logger: "LivingLogger" = LivingLogger(living_id)

    def record(self, hitbox: "Rect") -> "None":
        """Records an observation of the environment.
        
        Arguments:  
        `hitbox`: the living being's hitbox."""
        self.perception = self.controller.get_distance_by_type(hitbox)
        for entity_type, values in self.perception.items():
            self.perception_avg[entity_type] = (
                (self.perception_avg[entity_type][0] * self.observations + values[0])
                    / (self.observations + 1),
                (self.perception_avg[entity_type][1] * self.observations + values[1])
                    / (self.observations + 1)
            )
        self.observations += 1
        self.logger.dump_observation({
            entity_type.name.lower():
            sqrt(dists[0]**2 + dists[1]**2)
            for entity_type, dists in self.perception.items()
        })
