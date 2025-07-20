"""Module containing all necessary functions for the genetic algorithm."""
from typing import TYPE_CHECKING
from numpy.random import uniform, randint, normal
from utils.living.needs import Need
from utils.living.genome import Gene, MUTATION_RATE

if TYPE_CHECKING:
    from typing import Dict, List, Tuple
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

def select_parents(population: "List[LivingBeing]") -> "Tuple[LivingBeing, LivingBeing]":
    """Selects two parents from a given population, applying the genetic algorithm.
    
    Arguments:  
    `population`: the population from which the two parents are selected.
    
    Returns:  
    a tuple of two `LivingBeing` instances, the two parents."""
    fitnesses = [compute_fitness(living) for living in population]
    max_fitness = max(fitnesses)
    selected_indices: "List[int]" = []
    selected: "int" = 0
    while selected < 2:
        index = randint(len(population))
        if index not in selected_indices \
                 and uniform(high=1) <= fitnesses[index] / max_fitness:
            selected_indices.append(index)
            selected += 1
    return (
        population[selected_indices[0]],
        population[selected_indices[1]]
    )

def mutation(range: "float") -> "float":
    """Computes the mutation to be applied to a gene, knowing the width of the range of
    its admissible values.
    
    Arguments:  
    `range`: the width of the range of admissible values."""
    return normal(loc=0.0, scale=range) if uniform(0, 1) <= MUTATION_RATE else 0.0

def compute_evolutionary_genome(population: "List[LivingBeing]") -> "Dict[Gene, float]":
    """Computes the resulting genome from a population.
    
    Arguments:  
    `population`: the parent population.
    
    Returns:  
    a resulting genome, obtained via recomposition and mutations."""
    parents = select_parents(population)
    genome: "Dict[Gene, float]" = { }
    for gene in Gene:
        genome[gene] = parents[randint(2)].genome[gene] \
            + mutation(gene.max() - gene.min())
    return genome
