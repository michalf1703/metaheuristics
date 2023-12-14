import numpy as np


def oblicz_odleglosc(p1, p2):
    return np.linalg.norm(np.array(p2) - np.array(p1))


class Plansza:
    def __init__(self, sciezka_pliku):
        plik = open(sciezka_pliku, "r")
        punkty = [[int(i) for i in linia.split(" ")] for linia in plik]
        plik.close()
        self.tytul = sciezka_pliku
        self.miejsca = [punkt[0] - 1 for punkt in punkty]
        self.pozycje = [(punkt[1], punkt[2]) for punkt in punkty]
        self.feromony = [[1 for _ in punkty] for _ in punkty]
        self.odleglosci = [[oblicz_odleglosc(i, j) for j in punkty] for i in punkty]

    def aktualizuj_feromony(self, czynnik, mrowki):
        self._paruj_feromony(czynnik)
        for mrowka in mrowki:
            self._intensyfikuj_feromony(mrowka)

#iteracja przez wszystkie feromony i pomniejszanie ich o czynnik
    def _paruj_feromony(self, czynnik):
        for i in range(len(self.feromony)):
            for j in range(len(self.feromony[0])):
                self.feromony[i][j] -= self.feromony[i][j] * czynnik

#iteracja przez odwiedzone miejsca - im krotsza trasa im wiecej feromonow
    def _intensyfikuj_feromony(self, mrowka):
        for i in range(len(mrowka.odwiedzone_miejsca) - 1):
            self.feromony[mrowka.odwiedzone_miejsca[i]][mrowka.odwiedzone_miejsca[i + 1]] += (1 / mrowka.odleglosc_przebyta(self))
