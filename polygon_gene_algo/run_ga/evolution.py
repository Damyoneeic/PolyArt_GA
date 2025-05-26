from copy import deepcopy
from typing import List, Tuple

import cv2
import numpy as np

# Define a type alias for clarity
Individual = Tuple[np.ndarray, float]


# Calculate the mean squared error between target and generated images
def calc_fitness(goal_img: np.ndarray, img: np.ndarray) -> float:
    assert goal_img.shape == img.shape, "Images must have the same dimensions."
    error = goal_img.astype(float) - img.astype(float)
    return float(np.mean(error**2))


# Convert gene into an image by drawing circles onto the canvas
def gene2image(gene: np.ndarray, canvas: np.ndarray, radius: int) -> np.ndarray:
    height, width, channels = canvas.shape
    segment_size = 2 + channels
    fragments = np.split(gene, list(range(segment_size, len(gene), segment_size)))
    output = canvas.copy()
    for fragment in fragments:
        y_norm, x_norm, b_norm, g_norm, r_norm = fragment
        y, x = int(y_norm * height), int(x_norm * width)
        b, g, r = int(b_norm * 255), int(g_norm * 255), int(r_norm * 255)
        temp = deepcopy(output)
        # Draw a filled circle at the given position
        cv2.circle(temp, (x, y), radius, (b, g, r), thickness=-1)
        # Blend it with the existing canvas
        output = cv2.addWeighted(output, 0.5, temp, 0.5, 0)
    return output


# Apply random mutation to a gene based on mutation_rate
def mutate(gene: np.ndarray, mutation_rate: float) -> np.ndarray:
    if np.random.rand() < mutation_rate:
        idx = np.random.randint(len(gene))
        gene[idx] = np.random.rand()
    return gene


# Select one individual from population using roulette wheel selection
def roulette_selection(population: List[Individual]) -> Individual:
    fitness_vals = [ind[1] for ind in population]
    inv = [1.0 / f if f > 0 else 0.0 for f in fitness_vals]
    total = sum(inv)
    probs = [v / total for v in inv]
    idx = np.random.choice(len(population), p=probs)
    return population[idx]


# Perform one-point crossover between two parent genes
def crossover(
    parent1: np.ndarray, parent2: np.ndarray, cross_rate: float
) -> Tuple[np.ndarray, np.ndarray]:
    child1, child2 = deepcopy(parent1), deepcopy(parent2)
    if np.random.rand() < cross_rate:
        cp = np.random.randint(1, len(parent1))
        child1[:cp], child2[:cp] = parent2[:cp].copy(), parent1[:cp].copy()
    return child1, child2


# Select the top fraction of individuals as elites
def select_elites(
    population: List[Individual], elite_fraction: float = 0.2
) -> List[Individual]:
    k = max(1, int(len(population) * elite_fraction))
    sorted_pop = sorted(population, key=lambda ind: ind[1])
    return sorted_pop[:k]


# Generate the next generation of population
def next_generation(
    population: List[Individual],
    num_pop: int,
    mutation_rate: float,
    cross_rate: float,
    goal_img: np.ndarray,
    canvas: np.ndarray,
    radius: int,
) -> List[Individual]:
    # Calculate fitness for each individual
    for i, (gene, _) in enumerate(population):
        fitness = calc_fitness(goal_img, gene2image(gene, canvas, radius))
        population[i] = (gene, fitness)

    # Carry over elites directly
    new_population: List[Individual] = select_elites(population)

    # Fill the rest of the population
    while len(new_population) < num_pop:
        p1 = roulette_selection(population)
        p2 = roulette_selection(population)

        c1_gene, c2_gene = crossover(p1[0], p2[0], cross_rate)
        c1_gene = mutate(c1_gene, mutation_rate)
        c2_gene = mutate(c2_gene, mutation_rate)

        c1_fit = calc_fitness(goal_img, gene2image(c1_gene, canvas, radius))
        new_population.append((c1_gene, c1_fit))

        if len(new_population) < num_pop:
            c2_fit = calc_fitness(goal_img, gene2image(c2_gene, canvas, radius))
            new_population.append((c2_gene, c2_fit))

    return new_population
