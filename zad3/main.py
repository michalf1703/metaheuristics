from random import randint

from tqdm import tqdm

import multiprocessing as mp
import matplotlib.pyplot as plt

from Ant import Ant
from Board import Board

POPULATION_SIZE = 10  # [10, 30, 50]
RANDOM_FACTOR = 0.3  # [0.01, 0.3]
ALFA = 1  # [1, 2]
BETA = 1  # [1, 3]
ITERATION_NUMBER = 150
PHEROMONES_EVAPORATION_FACTOR = 0.5  # [0.1, 0.5]


def ant_algorithm(file_path, color, position, results):
    board = Board(file_path)
    best_ants = []

    for _ in tqdm(range(ITERATION_NUMBER), colour=color, position=position, leave=False):
        last_place = len(board.places) - 1
        ants = [Ant(randint(0, last_place)) for _ in range(POPULATION_SIZE)]
        for _ in range(last_place):
            for ant in ants:
                ant.next_step(board, ALFA, BETA, RANDOM_FACTOR)

        board.update_pheromones(PHEROMONES_EVAPORATION_FACTOR, ants)
        best_ants.append(min(ants, key=lambda x: x.distance_traveled(board)))
    results[position] = [board, best_ants]


def plot_iterations(results):
    fig = plt.figure()
    fig.set_figheight(20)
    fig.set_figwidth(20)
    for i in range(len(results)):
        plot = fig.add_subplot(4, 2, i + 1, title=results[i][0].title)
        plot.plot(range(1, ITERATION_NUMBER + 1), [ant.distance_traveled(results[i][0]) for ant in (results[i][1])])
        plt.xlabel("number_of_iterations")
        plt.ylabel("shortest distance in ant population")

    plt.tight_layout()
    plt.show()


def plot_paths(results):
    fig = plt.figure()
    fig.set_figheight(20)
    fig.set_figwidth(20)

    for i in range(len(results)):
        board = results[i][0]
        best_ants = results[i][1]
        best_ant = min(best_ants, key=lambda x: x.distance_traveled(board))
        x_values = [board.positions[place][0] for place in best_ant.visited_places]
        y_values = [board.positions[place][1] for place in best_ant.visited_places]

        plot = fig.add_subplot(4, 2, i + 1, title=results[i][0].title)
        plot.plot(x_values, y_values, 'ro-')

        plt.annotate('START', board.positions[best_ant.visited_places[0]],
                     textcoords="offset points", xytext=(5, -5))
        plt.annotate('END', board.positions[best_ant.visited_places[-1]],
                     textcoords="offset points", xytext=(5, -5))
        for place in best_ant.visited_places:
            plt.annotate(place + 1, board.positions[place], textcoords="offset points", xytext=(0, 7), ha='center')
        plt.xlabel("Najlepsza znaleziona trasa: " + str(best_ant.distance_traveled(board)))

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    results = mp.Manager().dict()
    processes = [mp.Process(target=ant_algorithm, args=("data/A-n32-k5.txt", "black", 0, results)),
                 mp.Process(target=ant_algorithm, args=("data/A-n80-k10.txt", "blue", 1, results)),
                 mp.Process(target=ant_algorithm, args=("data/B-n31-k5.txt", "green", 2, results)),
                 mp.Process(target=ant_algorithm, args=("data/B-n78-k10.txt", "yellow", 3, results)),
                 mp.Process(target=ant_algorithm, args=("data/P-n16-k8.txt", "white", 4, results)),
                 mp.Process(target=ant_algorithm, args=("data/P-n76-k5.txt", "red", 5, results))]

    for process in processes:
        process.start()
    for process in processes:
        process.join()

    plot_iterations([results[key] for key in sorted(results)])
    plot_paths(results.values())
