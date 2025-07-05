"""Module containing the brain implementation."""
from numpy.random import randint
from utils import Action, InteractionType, BASE_HUNGER_DECAY, BASE_LIFE_DECAY, \
        BASE_TIREDNESS_DECAY, BASE_MATING_DRIVE_DECAY, BASE_HUNGER, BASE_LIFE, \
        BASE_TIREDNESS, BASE_MATING_DRIVE, MAX_HUNGER, MAX_TIREDNESS, MIN_LIFE, \
        BASE_DECISION_RATE

class Brain:
    """Generic implementation for the living beings' brain."""
    def __init__(self) -> "None":
        """Instantiates the living being's brain."""
        self.hunger: "float" = BASE_HUNGER
        self.life: "float" = BASE_LIFE
        self.tiredness: "float" = BASE_TIREDNESS
        self.mating_drive: "float" = BASE_MATING_DRIVE
        self.time_since_last_decision: "int" = 0
        self.action: "Action" = Action.INTERACT

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
        self.hunger += elapsed_time * BASE_HUNGER_DECAY
        self.tiredness += elapsed_time * BASE_TIREDNESS_DECAY
        self.mating_drive += elapsed_time * BASE_MATING_DRIVE_DECAY
        if self.hunger >= MAX_HUNGER and self.tiredness >= MAX_TIREDNESS:
            self.life += BASE_LIFE_DECAY

        self.time_since_last_decision += elapsed_time
        if self.time_since_last_decision >= BASE_DECISION_RATE:
            self.compute_new_action()

        if self.life <= MIN_LIFE:
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
                self.life = BASE_LIFE
            case InteractionType.FEED:
                self.hunger = BASE_HUNGER
            case InteractionType.REST:
                self.tiredness = BASE_TIREDNESS
            case InteractionType.MATE:
                self.mating_drive = BASE_MATING_DRIVE
