"""Module containing all necessary functions for the genetic algorithm."""
from typing import TYPE_CHECKING
from numpy.random import uniform, randint, normal
from utils.living.needs import Need
from utils.living.genome import Gene, MUTATION_RATE

if TYPE_CHECKING:
    from typing import Dict, List, Tuple
    from model.entities.living.living import LivingBeing
    from model.entities.living.brain.central import Brain

def create_random_genome() -> "Dict[Gene, float]":
    """Creates a random genome, generating each gene's
    value with a uniform distribution within its acceptable range.
    
    Return:  
    a genome in the form of a `Dict` associating to each `Gene` its `float` value."""
    genome: "Dict[Gene, float]" = { }
    for gene in Gene:
        genome[gene] = uniform(gene.min(), gene.max())
    return genome

def compute_fitness(needs_avg: "Dict[Need, float]") -> "float":
    """Computes the fitness function of a given living being.

    Positional arguments:  
     - `needs_avg`: a `Dict` associating to each `Need` its average value during the
    living being's lifetime.
    
    Return:  
    The fitness value of the living being, as a `float`."""
    needs_avg_sum: "float" = 0
    for need in Need:
        if need not in [Need.LIFE, Need.NONE]:
            needs_avg_sum += (100 - needs_avg[need])
    no_life_avg: "float" = needs_avg_sum / (len(Need) - 2)
    return (no_life_avg + 100 - needs_avg[Need.LIFE]) / 2

def compute_whole_fitness(brain: "Brain") -> "float":
    """Computes the whole fitness of a living being, wheighted by its lifetime.
    
    Positional arguments:  
     - `brain`: the brain of the living being whose fitness is being computed.
    
    Return:  
    The fitness value of the living being weighted by its lifetime."""
    return brain.needs_tracker.lifetime * compute_fitness(brain.needs_tracker.needs_avg)

def select_parents(population: "List[LivingBeing]") -> "Tuple[LivingBeing, LivingBeing]":
    """Picks two parents from a given population, according to their fitness value.
    
    Positional arguments:  
     - `population`: all living beings currently alive.
    
    Return:  
    a `Tuple` containing the two parents."""
    fitnesses = [compute_whole_fitness(living.brain) for living in population]
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
    """Computes the mutation to be applied to a gene, knowing the range of
    its admissible values.
    
    Positional arguments:  
     - `range`: the width of the range of admissible values.
    
    Return:  
    The magnitude of the gene mutation."""
    return normal(loc=0.0, scale=range) if uniform() <= MUTATION_RATE else 0.0

def compute_evolutionary_genome(population: "List[LivingBeing]") -> "Dict[Gene, float]":
    """Computes the new offspring genome, applying the genetic algorithm to the desired
    parent population.
    
    Positional arguments:  
     - `population`: the parent population.
    
    Return:  
    A `Dict` associating to each `Gene` its value."""
    parents = select_parents(population)
    genome: "Dict[Gene, float]" = { }
    for gene in Gene:
        gene_val = parents[randint(2)].genome[gene] \
            + mutation(gene.max() - gene.min())
        genome[gene] = gene.min() if gene_val < gene.min() else \
            gene.max() if gene_val > gene.max() else gene_val
    return genome
