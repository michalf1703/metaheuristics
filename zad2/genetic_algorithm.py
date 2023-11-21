import random
from bitarray.util import urandom
from data import DATA, BAG_MAX_WEIGHT, BAG_MAX_VALUE


# return individual with random genes
def random_individual():
    return urandom(26)


# return sum of adaptation from all population
def calculate_population_adaptation_sum(population):
    sum = 0
    for individual in population:
        sum += calculate_adaptation(individual)
    return sum


# return average adaptation of individual from population
def calculate_population_adaptation_avg(population):
    return calculate_population_adaptation_sum(population) / len(population)


def calculate_population_adaptation_max(population):
    max = 0
    for individual in population:
        if max < calculate_adaptation(individual):
            max = calculate_adaptation(individual)
    return max


def calculate_population_adaptation_min(population):
    min = BAG_MAX_VALUE
    for individual in population:
        if min > calculate_adaptation(individual):
            min = calculate_adaptation(individual)
    return min

# return adaptation value of one individual
def calculate_adaptation(individual):
    weight_sum = 0
    value_sum = 0
    for i in range(len(individual)):
        if individual[i]:
            weight_sum += DATA[i][1]
            value_sum += DATA[i][2]
    if weight_sum > BAG_MAX_WEIGHT:
        return 0
    else:
        return value_sum


# return parents selected for crossing
def roulette_selection(population):
    adaptation_sum = calculate_population_adaptation_sum(population)
    if adaptation_sum == 0:
        return population
    probability_table = {}
    for i in range(len(population)):
        probability_table[i] = calculate_adaptation(population[i]) / adaptation_sum
    indexes = random.choices(list(probability_table.keys()),
                             weights=list(probability_table.values()),
                             k=len(population))
    return [population[index] for index in indexes]


# return parents selected for crossing
def elite_selection(population):
    ranking_table = {}
    for i in range(len(population)):
        ranking_table[i] = calculate_adaptation(population[i])
    indexes = sorted(ranking_table.items(), key=lambda item: -item[1])
    better_half = [population[indexes[i][0]] for i in range(int(len(population) / 2))]
    return better_half + better_half


# return survivors and parents chosen for crossing
def select_parents(population, crossing_probability, is_roulette):
    random.shuffle(population)
    number_to_selection = int(crossing_probability * len(population))
    individuals_to_selection = population[:number_to_selection]
    other_individuals = population[number_to_selection:]
    if is_roulette:
        return other_individuals, roulette_selection(individuals_to_selection)
    else:
        return other_individuals, elite_selection(individuals_to_selection)


# return two children with crossed genes based on two parents
def cross_genes(pair, is_single_pivot):
    pivot = random.randint(1, 24)
    pivot_2 = random.randint(1, 24)
    if pivot > pivot_2:
        pivot, pivot_2 = pivot_2, pivot
    if is_single_pivot:
        return [pair[0][:pivot] + pair[1][pivot:],
                pair[1][:pivot] + pair[0][pivot:]]
    else:
        return [pair[0][:pivot] + pair[1][pivot:pivot_2] + pair[0][pivot_2:],
                pair[1][:pivot] + pair[0][pivot:pivot_2] + pair[1][pivot_2:]]


# return random pairs from population
def select_pairs(population):
    pairs = []
    random.shuffle(population)

    i = 0
    while i < len(population) - 1:
        pairs.append([population[i], population[i + 1]])
        i += 2

    if len(population) % 2 == 1:
        pairs.append([population[len(population) - 1], population[0]])
    return pairs


# return new population based on pairs of parents
def new_generation(pairs, is_single_pivot):
    children = []
    for pair in pairs:
        children += cross_genes(pair, is_single_pivot)
    return children


# return population with random genes changed
def mutate_population(population, probability):
    random.shuffle(population)
    for i in range(int(probability * len(population))):
        population[i].invert(random.randint(0, 25))
    return population


# return final population generated by genetic algorithm
def genetic_algorithm(population_size=30,
                      number_of_iterations=30,
                      crossing_probability=1,
                      mutating_probability=0,
                      is_roulette=True,
                      wanted_adaptation=BAG_MAX_VALUE,
                      is_single_pivot=True):
    population = []
    for i in range(population_size):
        population.append(random_individual())

    for i in range(number_of_iterations):
        survivors, parents = select_parents(population, crossing_probability, is_roulette)
        pairs = select_pairs(parents)
        children = mutate_population(new_generation(pairs, is_single_pivot), mutating_probability)
        population = survivors + children
        if calculate_population_adaptation_avg(population) >= wanted_adaptation:
            return population
    return population