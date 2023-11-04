import random
import math

# Parametry początkowe
T = 5
alpha = 0.997 * T
k = 0.1
M = 6200

def f(x):
    return x * math.sin(10 * math.pi * x) + 1

def simulated_annealing(T, alpha, k, M):
    current_solution = random.uniform(-1, 2)  # Rozwiązanie początkowe w przedziale [-1, 2]
    current_cost = f(current_solution)
    best_solution = current_solution
    best_cost = current_cost

    sB = best_solution

    for i in range(M):
        new_solution = current_solution + random.uniform(-0.1, 0.1)  # Rozszerzenie obszaru sąsiedztwa
        new_solution = max(-1, min(new_solution, 2))

        new_cost = f(new_solution)
        delta = new_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / (k * T)):
            current_solution = new_solution
            current_cost = new_cost

        if new_cost > best_cost:
            best_solution = new_solution
            best_cost = new_cost

        # Aktualizacja najlepszego rozwiązania od początku
        if new_cost < f(sB):
            sB = new_solution

        T = alpha * T

    return best_solution, best_cost

best_solution, best_cost = simulated_annealing(T, alpha, k, M)

print(f"Maksimum globalne funkcji: x = {best_solution}, f(x) = {best_cost}")
