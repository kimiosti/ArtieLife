"""Module for log handlers implementation."""
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from typing import Dict
    from utils import Action

class LivingLogger:
    """Implementation of a living being's logger."""
    def __init__(self, living_id: "int") -> "None":
        """Instantiates a living being's logger.
        
        Arguments:  
        `living_id`: the living being's ID."""
        self.id: "int" = living_id
        self.log: "Path" = Path("logs/" + str(self.id) + "/log")
        self.log.parent.mkdir(mode=666, parents=True, exist_ok=True)
        with self.log.open("w", encoding="utf-8") as f:
            f.write("Starting log of living being " + str(living_id) + "\n")

    def dump(self, needs: "Dict[str, float]", dists: "Dict[str, float]",
             action: "Action") -> "None":
        """Writes a single log unit.
        
        Arguments:  
        `needs`: the needs of the living being, as perceived by the brain.  
        `dists`: the distances from the closest entities by type, as perceived by the brain.  
        `action`: the action chosen by the brain to be performed next."""
        with self.log.open("a", encoding="utf-8") as f:
            f.writelines([
                need_name + ": " + str(need_val) + "\n" for need_name, need_val in needs.items()
            ])
            f.writelines([
                dist_name + ": " + str(dist_val) + "\n" for dist_name, dist_val in dists.items()
            ])
            f.write("action: " + action.name.lower() + "\n\n\n")

    def record_death(self) -> "None":
        """Logs a living being's death."""
        with self.log.open("w", encoding="utf-8") as f:
            f.write("Living being " + str(self.id) + " died \nClosing log.\n")


class WorldLogger:
    """Implementation for the wolrd logger, responsible of tracking living being spawn, death and
    population size."""
    def __init__(self) -> "None":
        """Instantiates a world logger."""
        self.log: "Path" = Path("logs/world/log")
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
