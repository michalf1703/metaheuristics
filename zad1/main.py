import random
import math

def f(x):
    if -105 < x < -95:
        return -2 * abs(x + 100) + 10
    elif 95 < x < 105:
        return -2.2 * abs(x - 100) + 11
    else:
        return 0

def simulated_annealing(T, alpha, k, M):
    current_solution = random.uniform(-150, 150)  # Rozwiązanie początkowe w przedziale <-150, 150>
    current_cost = f(current_solution)
    best_solution = current_solution
    best_cost = current_cost

    for i in range(M):
        new_solution = current_solution + random.uniform(-5, 5)  # Generowanie sąsiedniego rozwiązania
        new_solution = max(-150, min(new_solution, 150))  # Ograniczenie rozwiązania do przedziału <-150, 150>
        new_cost = f(new_solution)

        delta = new_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / (k * T)):
            current_solution = new_solution
            current_cost = new_cost

        if current_cost > best_cost:
            best_solution = current_solution
            best_cost = current_cost

        T = alpha * T

    return best_solution, best_cost

# Parametry początkowe
T = 500
alpha = 0.999 * T
k = 0.1
M = 3000

best_solution, best_cost = simulated_annealing(T, alpha, k, M)

print(f"Najlepsze rozwiązanie: x = {best_solution}, f(x) = {best_cost}")
