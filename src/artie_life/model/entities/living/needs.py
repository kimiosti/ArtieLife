"""Module containing the needs tracker's implementation."""
from typing import TYPE_CHECKING
from controller.log import LivingLogger
from utils import Need

if TYPE_CHECKING:
    from typing import Dict

class NeedsTracker:
    """Implementation for the needs tracker of each living being."""
    def __init__(self) -> "None":
        """Instantiates a needs tracker."""
        self.needs: "Dict[Need, float]" = { }
        self.needs_avg: "Dict[Need, float]" = { }
        for need in Need:
            if need != Need.NONE:
                self.needs[need] = need.get_base_value()
                self.needs_avg[need] = 0
        self.observations: "int" = 0

    def decay(self, elapsed_time: "int") -> "bool":
        """Actuates a single decay step in all needs.
        
        Arguments:  
        `elapsed_time`: the amount of time elapsed since last step.
        
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
                new_value = value + (need.get_base_decay() * elapsed_time)
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

    def get_avgs(self) -> "Dict[str, float]":
        """Getter for the average needs values.
        
        Returns:  
        A `Dict` containing all averages as `float` described by a label as `str`."""
        return {
            need.name.lower().replace("_", " "): value for need, value in self.needs_avg.items()
        }

    def get_needs(self) -> "Dict[str, float]":
        """Getter for the last measured needs values.
        
        Returns:  
        A `Dict` containing all the last measured values as `float`
        described by a label as a `str`."""
        return {
            need.name.lower().replace("_", " "): value for need, value in self.needs.items()
        }
