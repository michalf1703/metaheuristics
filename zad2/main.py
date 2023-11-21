import data
from genetic_algorithm import *
import matplotlib.pyplot as plt

if __name__ == '__main__':

    NUMBERS = 50
    x_values = [x+2 for x in range(NUMBERS)]
    averages = []
    averages_2 = []
    maximums = []
    maximums_2 = []
    minimums = []
    minimums_2 = []

    for i in range(NUMBERS):
        sums = []
        sums_2 = []
        sums_3 = []
        for j in range(50):
            individuals = genetic_algorithm(is_roulette=False, number_of_iterations=i+2)
            sums.append(calculate_population_adaptation_avg(individuals))
            sums_2.append(calculate_population_adaptation_max(individuals))
            sums_3.append(calculate_population_adaptation_min(individuals))
        averages.append(sum(sums) / len(sums))
        maximums.append(max(sums_2))
        minimums.append(min(sums_3))
        print(i)

    for i in range(NUMBERS):
        sums = []
        sums_2 = []
        sums_3 = []
        for j in range(50):
            individuals = genetic_algorithm(is_roulette=True, number_of_iterations=i+2)
            sums.append(calculate_population_adaptation_avg(individuals))
            sums_2.append(calculate_population_adaptation_max(individuals))
            sums_3.append(calculate_population_adaptation_min(individuals))
        averages_2.append(sum(sums) / len(sums))
        maximums_2.append(max(sums_2))
        minimums_2.append(min(sums_3))
        print(i)

    plt.plot(x_values, minimums, "#99b8ff")
    plt.plot(x_values, averages, "#6996ff")
    plt.plot(x_values, maximums, "#0a54ff")
    plt.plot(x_values, minimums_2, "#ffa6a6")
    plt.plot(x_values, averages_2, "#ff6969")
    plt.plot(x_values, maximums_2, "#ff0505")
    plt.plot(x_values, [BAG_MAX_VALUE for x in range(NUMBERS)])
    plt.legend(["elite selection, minimum",
                "elite selection, average",
                "elite selection, maximum",
                "roulette selection, minimum",
                "roulette selection, average",
                "roulette selection, maximum",
                "max adaptation value"
                ])
    plt.xlabel("number_of_iterations")
    plt.ylabel("individual adaptation in final population")
    plt.show()