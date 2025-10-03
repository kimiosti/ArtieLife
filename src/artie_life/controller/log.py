"""Module for log handlers implementation."""
from typing import TYPE_CHECKING
from shutil import rmtree
from pathlib import Path
from utils.logs import GENOME_LOG, LOGS_FOLDER, WORLD_LOG, ATTENTION_LOG, REASON_LOG

if TYPE_CHECKING:
    from typing import Dict, Tuple
    from utils.living.actions import Action, EntityType
    from utils.living.needs import Need
    from utils.living.genome import Gene

def log_genome(living_id: "int", genome: "Dict[Gene, float]") -> "None":
    """Logs a living being's genome.
    
    Positional arguments:  
     - `living_id`: the living being's in-game ID.
     - `genome`: the living being's genome."""
    log = Path(GENOME_LOG(living_id))
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w", encoding="utf-8") as f:
        f.writelines([
            gene.name.lower()
            + ": "
            + str(value)
            + "\n"
            for gene, value in genome.items()
        ])

class AttentionLogger:
    """Implementation for the Attention lobe's activity logger."""
    def __init__(self, living_id: "int") -> "None":
        """Instantiates the attention lobe logger for the desired living being.
        
        Positional arguments:  
         - `living_id`: the living being's in-game ID."""
        self.log: "Path" = Path(ATTENTION_LOG(living_id))
        self.log.parent.mkdir(parents=True, exist_ok=True)
        with self.log.open("w", encoding="utf-8") as f:
            f.write("Starting Attention log of living being " + str(living_id)+ "\n\n")

    def log_step(self, user_reward: "float", needs_reward: "float",
                 positional_reward: "float", perception: "Dict[EntityType, Tuple[float, float]]",
                 user_input: "str", next_focus: "EntityType") -> "None":
        """Logs a single Attention lobe decision step.
        
        Positional arguments:  
         - `user_reward`: the user-defined reward value.
         - `needs_reward`: the self-obtained needs reward value.
         - `positional_reward`: the self-obtained positional reward value.
         - `perception`: the current living being's perception.
         - `user_input`: the current value of user input.
         - `next_focus`: the next computed focus of the living being."""
        with self.log.open("a", encoding="utf-8") as f:
            f.write("user reward: " + str(user_reward) + "\n")
            f.write("needs reward: " + str(needs_reward) + "\n")
            f.write("positional reward: " + str(positional_reward) + "\n\n")
            f.writelines([
                entity_type.name.lower() + ": "
                + str(value[0]) + ", " + str(value[1]) + "\n"
                for entity_type, value in perception.items()
            ])
            f.write("user input: " + user_input + "\n")
            f.write("attention: " + next_focus.name.lower() + "\n")

class ReasonLogger:
    """Implementation for the Reason lobe's activity logger."""
    def __init__(self, living_id: "int") -> "None":
        """Instantiates the reason logger for the desired living being.
        
        Positional arguments:  
         - `living_id`: the living being's in-game ID."""
        self.log: "Path" = Path(REASON_LOG(living_id))
        self.log.parent.mkdir(parents=True, exist_ok=True)
        with self.log.open("w", encoding="utf-8") as f:
            f.write("Starting Reason log for living being " + str(living_id) + "\n\n")

    def log_step(self, user_reward: "float", delta_fitness: "float",
                 delta_distance: "float", focus: "EntityType",
                 needs: "Dict[Need, float]", next_action: "Action") -> "None":
        """Logs a single Reason lobe decision step.
        
        Positional arguments:  
         - `user_reward`: the user-defined reward.
         - `delta_fitness`: the fitness gain since last decision.
         - `delta_distance`: the distance gain relative to the focus object since last decision.
         - `focus`: the actual object of the living being's focus.
         - `needs`: the current vital parameters of the living being.
         - `next_action`: the next action chosen by the lobe."""
        with self.log.open("a", encoding="utf-8") as f:
            f.write("user reward: " + str(user_reward) + "\n")
            f.write("fitness gain: " + str(delta_fitness) + "\n")
            f.write("distance gain: " + str(delta_distance) + "\n\n")
            f.write("attention: " + focus.name.lower() + "\n")
            f.writelines([
                need.name.lower().replace("_", " ") + ": "
                + str(value) + "\n" for need, value in needs.items()
            ])
            f.write("action: " + next_action.name.lower() + "\n")


class WorldLogger:
    """Implementation for the world logger, responsible of tracking living being spawn, death and
    population size."""
    def __init__(self) -> "None":
        """Instantiates a world logger."""
        rmtree(Path(LOGS_FOLDER), ignore_errors=True)
        self.log: "Path" = Path(WORLD_LOG)
        self.log.parent.mkdir(parents=True, exist_ok=True)
        with self.log.open("w", encoding="utf-8") as f:
            f.write("Starting game World log \n\n")

    def record_spawn(self, living_id: "int", population_size: "int") -> "None":
        """Logs the spawn of a livin being.
        
        Positional arguments:  
         - `living_id`: the ID of the spawned living being.  
         - `population_size`: the current population size."""
        with self.log.open("a", encoding="utf-8") as f:
            f.write("Spawning living being " + str(living_id) + "\n")
            f.write("Current population size: " + str(population_size) + "\n\n")

    def record_death(self, living_id: "int", lifetime: "float") -> "None":
        """Logs the death of a living being.
        
        Positional arguments:  
         - `living_id`: the ID of the dead living being.
         - `lifetime`: the living being's lifetime."""
        with self.log.open("a", encoding="utf-8") as f:
            f.write("Living being " + str(living_id) + " died \n")
            f.write("Lifetime: " + str(lifetime) + "\n\n")

    def dump_lifetime(self, living_id: "int", lifetime: "float") -> "None":
        """Dumps a living being's lifetime.
        
        Positional arguments:  
         - `living_id`: the living being's in-game ID.
         - `lifetime`: the living being's lifetime."""
        with self.log.open("a", encoding="utf-8") as f:
            f.write("Living being " + str(living_id) + " still alive \n")
            f.write("Lifetime: " + str(lifetime) + "\n\n")
