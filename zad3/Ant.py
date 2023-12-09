import random
from numpy.random import choice


def roulette_selection(places, weights):
    return choice(places, None, True, weights)


def random_selection(places):
    return places[random.randint(0, len(places) - 1)]


def calculate_weight(pheromone, distance, alfa, beta):
    return (pheromone ** alfa) * ((1 / distance) ** beta)


class Ant:
    def __init__(self, starting_point):
        self.visited_places = [starting_point]

    def distance_traveled(self, board):
        distance_sum = 0
        for i in range(len(self.visited_places) - 1):
            distance_sum += board.distances[self.visited_places[i]][self.visited_places[i + 1]]
        return distance_sum

    def next_step(self, board, alfa, beta, random_factor):
        not_visited_places = [a for a in board.places if a not in self.visited_places]
        current_place = self.visited_places[-1]

        if random.random() <= random_factor:
            self.visited_places.append(random_selection(not_visited_places))
        else:
            weights = [calculate_weight(board.pheromones[current_place][next_place],
                                        board.distances[current_place][next_place], alfa, beta)
                       for next_place in not_visited_places]
            probabilities = [weight / sum(weights) for weight in weights]
            self.visited_places.append(roulette_selection(not_visited_places, probabilities))
