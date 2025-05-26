from collections import deque
from typing import Dict

import cv2
import numpy as np

from . import evolution


def run_ga(goal_img: np.ndarray, parameters: Dict) -> tuple[np.ndarray, list]:
    fitness_list = []
    h, w, channel = goal_img.shape
    r = int(max(w, h) / 2)
    radius_const = r

    threshold = parameters["threshold"]
    polygon_per_cycle = parameters["polygon_per_cycle"]
    num_pop = parameters["num_pop"]
    num_gen = parameters["num_gen"]
    mutation_rate = parameters["mutation_rate"]
    cross_rate = parameters["cross_rate"]
    num_step = parameters["num_step"]
    dir_name = parameters["name"]

    canvus = np.full((h, w, 3), 128, dtype=np.uint8)

    # make a radius_list, there are more elements when the radius is small
    radius_deque: deque = deque()
    i = 1
    while r >= 0:
        if not (r < radius_const / 8):
            radius_deque.append(r)
            r = int(radius_const - i * radius_const / num_step)
            i += 1
        else:
            for _ in range(4):
                radius_deque.append(r)
                i += 1
            r -= 1
    cycle = 0
    cur_elite = 0
    while radius_deque:
        radius = radius_deque.popleft()
        print(f"~~~~~starting cycle {cycle}~~~~~~")
        print("radius for this cycle:", radius)

        # initialize population
        population = []
        for _ in range(num_pop):
            individual_gene = np.random.rand((2 + channel) * polygon_per_cycle)
            initial_fitness = evolution.calc_fitness(
                goal_img, evolution.gene2image(individual_gene, canvus, radius)
            )
            population.append(
                [individual_gene, initial_fitness]
            )  # fitnessは初期値10**9

        # iterate generation
        for i in range(num_gen):
            population = evolution.next_generation(
                population, num_pop, mutation_rate, cross_rate, goal_img, canvus, radius
            )

            best_fit_individual = min(population, key=lambda x: x[1])
            if best_fit_individual[1] < threshold:
                print(
                    f"generation {i}: best fitness**2 of the generation is {best_fit_individual[1]} and below threshold"
                )
                break
            elif i == num_gen - 1:
                print(
                    f"cycle {cycle}, generation {i}: best fitness**2 of the generation is {best_fit_individual[1]}"
                )
            elif i % 500 == 0:
                print(
                    f"cycle {cycle}, generation {i}: best fitness**2 of the generation is {best_fit_individual[1]}"
                )
        print("\n" * 2)

        prev_elite = cur_elite
        cur_elite = best_fit_individual[1]
        # if the radius is a good one, do it again
        if prev_elite - cur_elite > polygon_per_cycle * 100 / np.sqrt(h * w):
            radius_deque.appendleft(radius)
            print("added current radius, deque right now", list(radius_deque)[:3])

        if cycle == 0 or prev_elite >= cur_elite:
            # the final canvus with the genes outputted
            canvus = evolution.gene2image(best_fit_individual[0], canvus, radius)
            cv2.imwrite(f"./output/{dir_name}/cycle{cycle}.jpg", canvus)
            fitness_list.append([best_fit_individual[1], cycle, radius])
        elif cycle > 0 and prev_elite < cur_elite:
            cur_elite = prev_elite
            print(f"not improved, cycle{cycle} is therefore skipped")
        cycle += 1
    return canvus, fitness_list


# def print_population(population: np.ndarray) -> None:
#     i = 0
#     population = sorted(population, key=lambda x: x[1])
#     for individual in population:
#         print(f"-----number {i}-----", individual[1])
#         print(individual[0])
#         i += 1
#     print("------printed poplutaion------")
#     print("")
#     print("")
#     print("")
