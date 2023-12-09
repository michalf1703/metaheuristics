from math import sqrt


def calculate_distance(p1, p2):
    return sqrt((p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


class Board:
    def __init__(self, file_path):
        file = open(file_path, "r")

        points = [[int(i) for i in line.split(" ")] for line in file]
        file.close()
        self.title = file_path
        self.places = [point[0] - 1 for point in points]
        self.positions = [(point[1], point[2]) for point in points]
        self.pheromones = [[1 for _ in points] for _ in points]
        self.distances = [[calculate_distance(i, j) for j in points] for i in points]

    def update_pheromones(self, factor, ants):
        self._evaporate_pheromones(factor)
        for ant in ants:
            self._intensify_pheromones(ant)

    def _evaporate_pheromones(self, factor):
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[0])):
                self.pheromones[i][j] -= self.pheromones[i][j] * factor

    def _intensify_pheromones(self, ant):
        for i in range(len(ant.visited_places) - 1):
            self.pheromones[ant.visited_places[i]][ant.visited_places[i + 1]] += (1 / ant.distance_traveled(self))
