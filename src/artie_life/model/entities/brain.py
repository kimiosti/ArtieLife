"""Module containing the brain implementation."""
from utils import InteractionType, BASE_HUNGER_DECAY, BASE_LIFE_DECAY, BASE_TIREDNESS_DECAY, \
        BASE_MATING_DRIVE_DECAY, BASE_HUNGER, BASE_LIFE, BASE_TIREDNESS, BASE_MATING_DRIVE, \
        MAX_HUNGER, MAX_TIREDNESS, MIN_LIFE

class Brain:
    """Generic implementation for the living beings' brain."""
    def __init__(self) -> "None":
        """Instantiates the living being's brain."""
        self.hunger: "float" = BASE_HUNGER
        self.life: "float" = BASE_LIFE
        self.tiredness: "float" = BASE_TIREDNESS
        self.mating_drive: "float" = BASE_MATING_DRIVE

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

        if self.life <= MIN_LIFE:
            return False
        return True

    def actuate(self, interaction: "InteractionType") -> "None":
        """Actuates a given interaction on the living being.
        
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
