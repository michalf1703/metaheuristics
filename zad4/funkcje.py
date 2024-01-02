from numpy import pi, e, sin, exp, sqrt, cos


def ackley_function(x, y):
    return -(-20.0 * exp(-0.2 * sqrt(0.5 * (pow(x, 2) + pow(y, 2)))) - exp(0.5 * (cos(2 * pi * x) + cos(
        2 * pi * y))) + e + 20)


def mccormic_function(x, y):
    return sin(x + y) + pow(x - y, 2) - 1.5 * x + 2.5 * y + 1