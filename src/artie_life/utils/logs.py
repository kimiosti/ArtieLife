from typing import TYPE_CHECKING
from pathlib import Path
from shutil import rmtree
from os.path import join as join_path
from utils.living.genome import Gene
from utils.living.needs import Need, compute_expected_lifetime
from controller.genetics import compute_fitness, compute_whole_fitness

if TYPE_CHECKING:
    from model.entities.living.living import LivingBeing

LOGS_FOLDER: "Path" = Path("logs")
GAME_SETTINGS_LOG: "Path" = Path(join_path(LOGS_FOLDER, "game.csv"))
def WORLD_LOG(world_id: "int") -> "Path":
    """Returns the desired single-world log path, given an in-game world ID.
    
    Positional arguments:  
     - `world_id`: the world's in-game ID.
    
    Return:  
    A `Path` object pointing to the desired file."""
    return Path(join_path(LOGS_FOLDER, str(world_id), "world.csv"))

def reset_logs_folder() -> "None":
    """Cleans up previous logs. Necessary at startup to avoid conflicts."""
    rmtree(LOGS_FOLDER, ignore_errors=True)
    LOGS_FOLDER.mkdir(parents=True, exist_ok=True)


def log_game_settings(learning: "str", genetics: "str") -> "None":
    """Logs the current game's settings. To be invoked just once, at the system
    startup.
    
    Positional arguments:  
     - `learning`: the value of the command line option related to learning \
    enabling.
     - `genetics`: the kind of genetic algorithm requested via the command line option."""
    with open(GAME_SETTINGS_LOG, "a") as file:
        file.write("learning_enable, genetic_algorithm\n")
        file.write(learning + ", " + genetics + "\n")

def start_world_log(world_id: "int") -> "None":
    """Starts a world's log, recording the log's header.
    
    Positional arguments:  
     - `world_id`: the in-game world ID."""
    log = WORLD_LOG(world_id)
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "w") as file:
        file.write("id, ")
        for gene in Gene:
            file.write(gene.name.lower() + ", ")
        file.write("fitness, whole_fitness, ")
        file.write("expected_lifetime, lifetime, alive\n")

def log_living_being_stats(world_id: "int", living_being: "LivingBeing") -> "None":
    """Logs all relevant data about a given living being.
    
    Positional arguments:  
     - `world_id`: the world's in-game ID.  
     - `living_being`: the living being whose information has to be logged."""
    log = WORLD_LOG(world_id)
    with open(log, "a") as file:
        file.write(str(living_being.game_id) + ", ")
        for gene in Gene:
            file.write(str(living_being.genome[gene]) + ", ")
        file.write(str(compute_fitness(living_being.brain.needs_tracker.needs_avg)) + ", ")
        file.write(str(compute_whole_fitness(living_being.brain)) + ", ")
        file.write(str(compute_expected_lifetime(living_being.genome)) + ", ")
        file.write(str(living_being.brain.needs_tracker.lifetime) + ", ")
        file.write(str(
            living_being.brain.needs_tracker.needs[Need.LIFE] < Need.LIFE.get_threshold()
        ))
        file.write("\n")
