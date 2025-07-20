"""Module containing all necessary functions for the genetic algorithm."""
from typing import TYPE_CHECKING
from numpy.random import uniform
from utils.living.needs import Need
from utils.living.genome import Gene

if TYPE_CHECKING:
    from typing import Dict
    from model.entities.living.living import LivingBeing

def create_random_genome() -> "Dict[Gene, float]":
    """Creates a random genome, pulling from each gene's possbile
    values with a uniform distribution.
    
    Returns:  
    a genome in the form of a dictionary associating to each `Gene` its value."""
    genome: "Dict[Gene, float]" = { }
    for gene in Gene:
        genome[gene] = uniform(gene.min(), gene.max())
    return genome

def compute_fitness(living: "LivingBeing") -> "float":
    """Computes the fitness function of a given living being.
    
    Returns:  
    the fitness value of the living being, as a `float`."""
    needs_avg_sum: "float" = 0
    for need in Need:
        if need not in [Need.LIFE, Need.NONE]:
            needs_avg_sum += (100 - living.brain.needs_tracker.needs_avg[need])
    needs_avg: "float" = needs_avg_sum / (len(Need) - 2)
    return living.lifetime * (needs_avg + 100 - living.brain.needs_tracker.needs_avg[Need.LIFE]) / 2
