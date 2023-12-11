import random
from numpy.random import choice


def selekcja_ruletkowa(miejsca, wagi):
    return choice(miejsca, None, True, wagi)


def losowa_selekcja(miejsca):
    return miejsca[random.randint(0, len(miejsca) - 1)]


def oblicz_wage(feromony, odleglosc, alfa, beta):
    return (feromony ** alfa) * ((1 / odleglosc) ** beta)


class Mrowka:
    def __init__(self, punkt_startowy):
        self.odwiedzone_miejsca = [punkt_startowy]

    def odleglosc_przebyta(self, plansza):
        suma_odleglosci = 0
        for i in range(len(self.odwiedzone_miejsca) - 1):
            suma_odleglosci += plansza.odleglosci[self.odwiedzone_miejsca[i]][self.odwiedzone_miejsca[i + 1]]
        return suma_odleglosci

    def nastepny_krok(self, plansza, alfa, beta, czynnik_losowy):
        nieodwiedzone_miejsca = [a for a in plansza.miejsca if a not in self.odwiedzone_miejsca]
        obecne_miejsce = self.odwiedzone_miejsca[-1]

        if random.random() <= czynnik_losowy:
            self.odwiedzone_miejsca.append(losowa_selekcja(nieodwiedzone_miejsca))
        else:
            wagi = [oblicz_wage(plansza.feromony[obecne_miejsce][nastepne_miejsce],
                               plansza.odleglosci[obecne_miejsce][nastepne_miejsce], alfa, beta)
                    for nastepne_miejsce in nieodwiedzone_miejsca]
            prawdopodobienstwa = [waga / sum(wagi) for waga in wagi]
            self.odwiedzone_miejsca.append(selekcja_ruletkowa(nieodwiedzone_miejsca, prawdopodobienstwa))
