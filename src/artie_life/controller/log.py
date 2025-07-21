"""Module for log handlers implementation."""
from typing import TYPE_CHECKING
from shutil import rmtree
from pathlib import Path
from utils.logs import LIVING_LOG, GENOME_LOG, LOGS_FOLDER, WORLD_LOG

if TYPE_CHECKING:
    from typing import Dict
    from utils.living.actions import Action
    from utils.living.genome import Gene

class LivingLogger:
    """Implementation of a living being's logger."""
    def __init__(self, living_id: "int") -> "None":
        """Instantiates a living being's logger.
        
        Arguments:  
        `living_id`: the living being's ID."""
        self.living_id: "int" = living_id
        self.genome_log: "Path" = Path(GENOME_LOG(living_id))
        self.log: "Path" = Path(LIVING_LOG(living_id))
        self.log.parent.mkdir(mode=666, parents=True, exist_ok=True)

    def record_spawn(self, genome: "Dict[Gene, float]") -> "None":
        """Logs the living being's spawn."""
        with self.genome_log.open("w", encoding="utf-8") as f:
            f.writelines([
                gene.name.lower()
                + ": "
                + str(value)
                + "\n"
                for gene, value in genome.items()
            ])
        with self.log.open("w", encoding="utf-8") as f:
            f.write("Starting log of living being " + str(self.living_id) + "\n")

    def dump_observation(self, observation: "Dict[str, float]") -> "None":
        """Logs a single living being observation.
        
        Arguments:  
        `observation`: a `Dict` containing all observed `float` values with their `str` label."""
        with self.log.open("a", encoding="utf-8") as f:
            f.writelines([
                need_name
                + ": "
                + str(need_val)
                + "\n"
                for need_name, need_val in observation.items()
            ])

    def dump_action(self, action: "Action") -> "None":
        """Logs a single living being action.
        
        Arguments:  
        `action`: the action to be logged."""
        with self.log.open("a", encoding="utf-8") as f:
            f.write("Action: " + action.name.lower() + "\n\n")

    def record_death(self) -> "None":
        """Logs a living being's death."""
        with self.log.open("w", encoding="utf-8") as f:
            f.write("Living being " + str(self.living_id) + " died \nClosing log.\n")


class WorldLogger:
    """Implementation for the wolrd logger, responsible of tracking living being spawn, death and
    population size."""
    def __init__(self) -> "None":
        """Instantiates a world logger."""
        rmtree(Path(LOGS_FOLDER))
        self.log: "Path" = Path(WORLD_LOG)
        self.log.parent.mkdir(parents=True, exist_ok=True)
        with self.log.open("w", encoding="utf-8") as f:
            f.write("Starting game World log \n")

    def record_spawn(self, living_id: "int", population_size: "int") -> "None":
        """Logs the spawning of a livin being.
        
        Arguments:  
        `living_id`: the ID of the spawned living being.  
        `population_size`: the current population size."""
        with self.log.open("a", encoding="utf-8") as f:
            f.write("Spawning living being " + str(living_id) + "\n")
            f.write("Current population size: " + str(population_size) + "\n\n")

    def record_death(self, living_id: "int") -> "None":
        """Logs the death of a living being.
        
        Arguments:  
        `living_id`: the ID of the dead living being."""
        with self.log.open("a", encoding="utf-8") as f:
            f.write("Living being " + str(living_id) + " died \n\n")
