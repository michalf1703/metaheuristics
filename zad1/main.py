import random
import math
import matplotlib.pyplot as plt


def plot_solution_changes(f, s1, s2, step, solution_changes, best_solution):
    x = [i * step for i in range(int(s1 / step), int(s2 / step))]
    y = [f(i) for i in x]

    x_values = [change[0] for change in solution_changes]
    y_values = [change[1] for change in solution_changes]

    plt.plot(x, y, label=f"Funkcja {f.__name__}")
    plt.scatter(x_values, y_values, color='red', label="Zmiany best_solution")

    # Dodaj zaznaczenie punktu best_solution
    plt.scatter(best_solution[0], best_solution[1], color='green', label="best_solution", marker='x', s=100)

    plt.xlabel('Wartość x')
    plt.ylabel('Wartość funkcji')
    plt.legend()
    plt.show()


def f1(x):
    return x * math.sin(10 * math.pi * x) + 1


def f2(x):
    if -105 < x < -95:
        return -2 * abs(x + 100) + 10
    elif 95 < x < 105:
        return -2.2 * abs(x - 100) + 11
    else:
        return 0


def simulated_annealing(T, alpha, k, M, f, s1, s2, r1, r2):
    current_solution = random.uniform(s1, s2)
    current_cost = f(current_solution)
    best_solution = current_solution
    best_cost = current_cost
    correction = 0
    solution_changes = []  # Przechowuje zmiany best_solution

    for i in range(M):
        new_solution = current_solution + random.uniform(r1, r2)
        new_solution = max(s1, min(new_solution, s2))

        new_cost = f(new_solution)
        delta = new_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / (k * T)):
            current_solution = new_solution
            current_cost = new_cost

        if new_cost > best_cost:
            best_solution = new_solution
            best_cost = new_cost
            correction += 1
            solution_changes.append((best_solution, best_cost))

        T = alpha * T

    return best_solution, best_cost, correction, solution_changes


def menu():
    while True:
        print("__________________________________________________________________________________________")
        print("Wybierz funkcję do optymalizacji:")
        print("1. f(x) = x * sin(10πx) + 1 , dla przedziału [-1,2]")
        print("2. f(x) = -2 * |x + 100) + 10 dla x należącego do (-105, -95)")
        print("   f(x) = -2.2 * |x - 100| + 11 dla x należącego do (95, 105)")
        print("   f(x) = 0 dla reszty x z przedziału [-150,150]")
        print("Inna komenda - zakończenie pracy programu")
        choice = input("Podaj numer funkcji (1 lub 2): ")

        if choice == "1":
            T = 5
            alpha = 0.997 * T
            k = 0.1
            M = 1200
            f = f1
            s1 = -1
            s2 = 2
            r1 = -0.1
            r2 = 0.1
            result = simulated_annealing(T, alpha, k, M, f, s1, s2, r1, r2)
        elif choice == "2":
            T = 500
            alpha = 0.999 * T
            k = 0.1
            M = 3000
            f = f2
            s1 = -150
            s2 = 150
            r1 = -15
            r2 = 15
            result = simulated_annealing(T, alpha, k, M, f, s1, s2, r1, r2)
        else:
            print("Zakończenie pracy programu.")
            break

        best_solution, best_cost, correction, solution_changes = result
        print(
            f"Maksimum globalne funkcji {f.__name__}: x = {best_solution}, f(x) = {best_cost}, liczba korekcji = {correction}")
        # Stwórz wykres funkcji
        plot_solution_changes(f, s1, s2, 0.01, solution_changes, (best_solution, best_cost))


menu()
