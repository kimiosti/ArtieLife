"""Module containing the single world's execution engine."""
from multiprocessing import Process
from pygame import init
from pygame.time import Clock

class WorldEngine(Process):
    """Class representing the single world's execution engine."""

    def __init__(self, world_id: "int", gui_enable: "str", learning_enable: "str",
                 genetic_algorithm: "str") -> "None":
        """Constructor for the world's execution engine.
        
        Positional arguments:  
        `world_id`: the in-game world's ID.  
        `gui_enable`: true/false flag representing if the world should be visually 
        shown to the user for interaction.  
        `learning_enable`: true/false flag representing if the agents should be  
        learning or acting randomly.  
        `genetic_algorithm`: the kind of genetic algorithm applied to the  
        population, or none if all genomes should be randomly generated."""
        self.world_id = world_id
        self.gui_enable = gui_enable
        self.learning_enable = learning_enable
        self.genetic_algorithm = genetic_algorithm
        init()
        self.running = True
        super().__init__()

    def run(self) -> "None":
        """Main method of the world engine."""
        # TODO - implement world engine behavior
        clock = Clock()
        while self.running:
            print(self.world_id)
            clock.tick(1)

