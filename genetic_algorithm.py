import copy
import random
import numpy as np

from typing import List, Tuple, Optional, Union
from individual import Individual
from neural_network import *


# GA selection , selects snake with percentage based on snake fitness // chance for snake to be selected is directly proportional with snake fitness
def roulette_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    selected = []
    # sum of fitness of all snakes in a population, used to select snakes
    sum_pop_fitness = sum(individual.fitness for individual in population)

    # for number of individuals to select : choose a random fitness between 0:pop_fit_sum and initialize current_fitness with 0
    # loop over all snakes in population and sum their fitness with current fitness, if
    for i in range(individuals_to_select):
        random_fitness = random.uniform(0, sum_pop_fitness)
        current_fitness = 0
        for individual in population:
            current_fitness += individual.fitness
            if current_fitness >= random_fitness:
                selected.append(individual)
                break

    return selected


def tournament_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    pass


def two_point_roulette_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    pass


def elitist_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    selected = sorted(population, key=lambda individual: individual.fitness, reverse=True)
    return selected[:individuals_to_select]


# numpy matrix has shape (row_count, col_count)
# swaps weights from a parent to a child from a random row until the end
def one_point_crossover(parent1: NeuralNetwork, parent2: NeuralNetwork) -> Tuple[NeuralNetwork, NeuralNetwork]:
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    architecture = parent1.neural_net_architecture

    for layer in architecture:
        matrix_rows, matrix_cols = parent1.weights[layer].shape
        rand_row = random.randint(0, matrix_rows)

        # all columns , rows from 0 to rand_row
        child1.weights[layer][:rand_row, :] = parent2.weights[layer][:rand_row, :]
        child2.weights[layer][:rand_row, :] = parent1.weights[layer][:rand_row, :]

        matrix_rows, matrix_cols = parent1.biases[layer].shape
        rand_row = random.randint(0, matrix_rows)

        child1.biases[layer][:rand_row, :] = parent2.biases[layer][:rand_row, :]
        child2.biases[layer][:rand_row, :] = parent1.biases[layer][:rand_row, :]

    return child1, child2


# only swaps weights and biases between 2 random rows from the parent
def two_point_crossover(parent1: NeuralNetwork, parent2: NeuralNetwork) -> Tuple[NeuralNetwork, NeuralNetwork]:
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    architecture = parent1.neural_net_architecture

    for layer in architecture:
        matrix_rows, matrix_cols = parent1.weights[layer].shape
        rand_row1 = random.randint(0, matrix_rows)
        rand_row2 = random.randint(rand_row1, matrix_rows)

        # all columns , rows from 0 to rand_row
        child1.weights[layer][rand_row1:rand_row2, :] = parent2.weights[layer][rand_row1:rand_row2, :]
        child2.weights[layer][rand_row1:rand_row2, :] = parent1.weights[layer][rand_row1:rand_row2, :]

        matrix_rows, matrix_cols = parent1.biases[layer].shape
        rand_row1 = random.randint(0, matrix_rows)
        rand_row2 = random.randint(rand_row1, matrix_rows)

        child1.biases[layer][rand_row1:rand_row2, :] = parent2.biases[layer][rand_row1:rand_row2, :]
        child2.biases[layer][rand_row1:rand_row2, :] = parent1.biases[layer][rand_row1:rand_row2, :]

    return child1, child2


def uniform_crossover(parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    pass


def arithmetic_crossover(parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    pass


def whole_mutation(child: NeuralNetwork, mutation_rate: float) -> NeuralNetwork:
    # mutation_array = np.random.random(child.weights["L1"].shape) < mutation_rate
    # uniform_mutation = np.random.uniform(size=child.weights["L1"].shape)
    # child.weights["L1"][mutation_array] = uniform_mutation[mutation_array]

    child_copy = copy.deepcopy(child)

    for layer in child_copy.neural_net_architecture:

        for weight in child_copy.weights[layer]:
            for i in range(len(weight)):
                choice = random.uniform(0, 1)
                if choice < mutation_rate:
                    weight[i] = random.uniform(-1, 1)

        for bias in child_copy.biases[layer]:
            for i in range(len(bias)):
                choice = random.uniform(0, 1)
                if choice < mutation_rate:
                    bias[i] = random.uniform(-1, 1)

    return child_copy


def gaussian_mutation(chromosome: np.ndarray, prob_mutation: float,
                      mu: List[float] = None, sigma: List[float] = None,
                      scale: Optional[float] = None) -> None:
    """
    Perform a gaussian mutation for each gene in an individual with probability, prob_mutation.

    If mu and sigma are defined then the gaussian distribution will be drawn from that,
    otherwise it will be drawn from N(0, 1) for the shape of the individual.
    """
    # Determine which genes will be mutated
    mutation_array = np.random.random(chromosome.shape) < prob_mutation
    # If mu and sigma are defined, create gaussian distribution around each one
    if mu and sigma:
        gaussian_mutation = np.random.normal(mu, sigma)
    # Otherwise center around N(0,1)
    else:
        gaussian_mutation = np.random.normal(size=chromosome.shape)

    if scale:
        gaussian_mutation[mutation_array] *= scale

    # Update
    chromosome[mutation_array] += gaussian_mutation[mutation_array]


def random_uniform_mutation(chromosome: np.ndarray, prob_mutation: float,
                            low: Union[List[float], float],
                            high: Union[List[float], float]
                            ) -> None:
    """
    Randomly mutate each gene in an individual with probability, prob_mutation.
    If a gene is selected for mutation it will be assigned a value with uniform probability
    between [low, high).

    @Note [low, high) is defined for each gene to help get the full range of possible values
    @TODO: Eq 11.4
    """
    assert type(low) == type(high), 'low and high must have the same type'
    mutation_array = np.random.random(chromosome.shape) < prob_mutation
    if isinstance(low, list):
        uniform_mutation = np.random.uniform(low, high)
    else:
        uniform_mutation = np.random.uniform(low, high, size=chromosome.shape)
    chromosome[mutation_array] = uniform_mutation[mutation_array]


def simulated_binary_crossover(parent1: np.ndarray, parent2: np.ndarray, eta: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    This crossover is specific to floating-point representation.
    Simulate behavior of one-point crossover for binary representations.

    For large values of eta there is a higher probability that offspring will be created near the parents.
    For small values of eta, offspring will be more distant from parents

    Equation 9.9, 9.10, 9.11
    @TODO: Link equations
    """
    # Calculate Gamma (Eq. 9.11)
    rand = np.random.random(parent1.shape)
    gamma = np.empty(parent1.shape)
    gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (eta + 1))  # First case of equation 9.11
    gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (eta + 1))  # Second case

    # Calculate Child 1 chromosome (Eq. 9.9)
    chromosome1 = 0.5 * ((1 + gamma) * parent1 + (1 - gamma) * parent2)
    # Calculate Child 2 chromosome (Eq. 9.10)
    chromosome2 = 0.5 * ((1 - gamma) * parent1 + (1 + gamma) * parent2)

    return chromosome1, chromosome2


def single_point_binary_crossover(parent1: np.ndarray, parent2: np.ndarray, major='r') -> Tuple[np.ndarray, np.ndarray]:
    offspring1 = parent1.copy()
    offspring2 = parent2.copy()

    rows, cols = parent2.shape
    row = np.random.randint(0, rows)
    col = np.random.randint(0, cols)

    if major.lower() == 'r':
        offspring1[:row, :] = parent2[:row, :]
        offspring2[:row, :] = parent1[:row, :]

        offspring1[row, :col + 1] = parent2[row, :col + 1]
        offspring2[row, :col + 1] = parent1[row, :col + 1]
    elif major.lower() == 'c':
        offspring1[:, :col] = parent2[:, :col]
        offspring2[:, :col] = parent1[:, :col]

        offspring1[:row + 1, col] = parent2[:row + 1, col]
        offspring2[:row + 1, col] = parent1[:row + 1, col]

    return offspring1, offspring2
