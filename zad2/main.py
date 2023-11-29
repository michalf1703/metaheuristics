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
            individuals = algorytm_genetyczny(ruletka=False, liczba_iteracji=i + 2)
            sums.append(oblicz_srednie_przystosowanie_populacji(individuals))
            sums_2.append(oblicz_maksymalne_przystosowanie_populacji(individuals))
            sums_3.append(oblicz_minimalne_przystosowanie_populacji(individuals))
        averages.append(sum(sums) / len(sums))
        maximums.append(max(sums_2))
        minimums.append(min(sums_3))
        print(i)

    for i in range(NUMBERS):
        sums = []
        sums_2 = []
        sums_3 = []
        for j in range(50):
            individuals = algorytm_genetyczny(ruletka=True, liczba_iteracji=i + 2)
            sums.append(oblicz_srednie_przystosowanie_populacji(individuals))
            sums_2.append(oblicz_maksymalne_przystosowanie_populacji(individuals))
            sums_3.append(oblicz_minimalne_przystosowanie_populacji(individuals))
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
    plt.legend(["selekcja elitarna, minimum",
                "selekcja elitarna, średnia",
                "selekcja elitarna, maksimum",
                "koło ruletki, minimum",
                "koło ruletki, średnia",
                "koło ruletki, maksimum",
                "maksymalna warotść adaptacji"
                ])
    plt.xlabel("liczba iteracji")
    plt.ylabel("adaptacja indywidualna w populacji końcowej")
    plt.show()