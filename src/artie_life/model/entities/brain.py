"""Module containing the brain implementation."""
from typing import TYPE_CHECKING
from numpy.random import randint
from utils import Action, InteractionType, BASE_HUNGER_DECAY, BASE_LIFE_DECAY, \
        BASE_TIREDNESS_DECAY, BASE_MATING_DRIVE_DECAY, BASE_HUNGER, BASE_LIFE, \
        BASE_TIREDNESS, BASE_MATING_DRIVE, MAX_HUNGER, MAX_TIREDNESS, MIN_LIFE, \
        BASE_DECISION_RATE

if TYPE_CHECKING:
    from typing import Dict
    from controller.world.world_controllers import DistanceController

class Brain:
    """Generic implementation for the living beings' brain."""
    def __init__(self, distance_controller: "DistanceController", living_id: "int") -> "None":
        """Instantiates the living being's brain.
        
        Arguments:  
        `distance_controller`: the `DistanceController` tracking the living being's
        perception of the world's space."""
        self.needs: "Dict[str, float]" = {
            "life": BASE_LIFE,
            "hunger": BASE_HUNGER,
            "tiredness": BASE_TIREDNESS,
            "mating drive": BASE_MATING_DRIVE
        }
        self.time_since_last_decision: "int" = 0
        self.action: "Action" = Action.INTERACT
        self.controller: "DistanceController" = distance_controller

    def compute_new_action(self) -> "None":
        """Computes the next action to be performed."""
        action_idx = randint(5)
        for action in Action:
            if action.value == action_idx:
                self.action = action
        self.time_since_last_decision = 0

    def update(self, elapsed_time: "int") -> "bool":
        """Updates the brain, decaying vital parameters.

        Arguments:  
        `elapsed_time`: the amount of time since last brain update.

        Returns:  
        A `bool` representing whether the living being is still alive."""
        self.needs["hunger"] += elapsed_time * BASE_HUNGER_DECAY
        self.needs["tiredness"] += elapsed_time * BASE_TIREDNESS_DECAY
        self.needs["mating drive"] += elapsed_time * BASE_MATING_DRIVE_DECAY
        if self.needs["hunger"] >= MAX_HUNGER and self.needs["tiredness"] >= MAX_TIREDNESS:
            self.needs["life"] += BASE_LIFE_DECAY

        self.time_since_last_decision += elapsed_time
        if self.time_since_last_decision >= BASE_DECISION_RATE:
            self.compute_new_action()

        if self.needs["life"] <= MIN_LIFE:
            return False
        return True

    def get_action(self) -> "Action":
        """Gets the next action to be performed by the living being.
        
        Returns:  
        An `Action` value representing the desired action."""
        return self.action

    def actuate(self, interaction: "InteractionType") -> "None":
        """Actuates a given interaction on the living being's vital parameters.
        
        Arguments:  
        `interaction`: the type of the interaction to be made effective."""
        match interaction:
            case InteractionType.HEAL:
                self.needs["life"] = BASE_LIFE
            case InteractionType.FEED:
                self.needs["hunger"] = BASE_HUNGER
            case InteractionType.REST:
                self.needs["tiredness"] = BASE_TIREDNESS
            case InteractionType.MATE:
                self.needs["mating drive"] = BASE_MATING_DRIVE
