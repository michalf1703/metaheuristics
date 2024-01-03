from numpy import linspace, meshgrid
from tqdm import tqdm
from random import uniform
from Czastka import Czastka
import matplotlib.pyplot as plt

from funkcje import mccormic_function, ackley_function


def rysuj_wykres(dziedzina, czastki, funkcja_adaptacji):
    X, Y = meshgrid(linspace(dziedzina[0], dziedzina[1], num=100), linspace(dziedzina[0], dziedzina[1], num=100))
    Z = funkcja_adaptacji(X, Y)

    ax = plt.axes(projection='3d')
    ax.scatter3D([c.x for c in czastki],
                 [c.y for c in czastki],
                 [c.aktualna_adaptacja for c in czastki],
                 edgecolor='red',
                 alpha=1,
                 color='red')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, edgecolor="none", alpha=0.4)
    plt.show()


if __name__ == '__main__':
    LICZBA_ITERACJI = 30
    ROZMIAR_POPULACJI = 50
    BEZWLADNOSC = 0.4
    STALA_POZNAWCZA = 0.3
    STALA_SPOLECZNA = 0.9
    DZIEDZINA = [-5, 5]
    FUNKCJA_ADAPTACJI = ackley_function

    czastki = [Czastka(uniform(DZIEDZINA[0], DZIEDZINA[1]),
                       uniform(DZIEDZINA[0], DZIEDZINA[1]),
                       BEZWLADNOSC,
                       STALA_POZNAWCZA,
                       STALA_SPOLECZNA,
                       FUNKCJA_ADAPTACJI, DZIEDZINA)
               for _ in range(ROZMIAR_POPULACJI)]

    for _ in tqdm(range(LICZBA_ITERACJI), ncols=200):
        najlepsza_aktualna_adaptacja = czastki[0].aktualna_adaptacja
        najlepszy_x = czastki[0].x
        najlepszy_y = czastki[0].y

        for czastka in czastki:
            if czastka.aktualna_adaptacja > najlepsza_aktualna_adaptacja:
                najlepsza_aktualna_adaptacja = czastka.aktualna_adaptacja
                najlepszy_x = czastka.x
                najlepszy_y = czastka.y

        for czastka in czastki:
            czastka.aktualizuj_predkosc(najlepszy_x, najlepszy_y)
            czastka.aktualizuj_pozycje()
            czastka.aktualizuj_adaptacje()
        rysuj_wykres(DZIEDZINA, czastki, FUNKCJA_ADAPTACJI)

    print(max([c.najlepsza_adaptacja for c in czastki]))
    for czastka in czastki:
        print("---------------------------")
        print(czastka.najlepsza_adaptacja)
        print(czastka.najlepszy_x)
        print(czastka.najlepszy_y)
        print(ackley_function(najlepszy_x,najlepszy_y))
        print("---------------------------")
    najlepsza_czastka = max(czastki, key=lambda c: c.najlepsza_adaptacja)
    print("Najlepsza adaptacja:", najlepsza_czastka.najlepsza_adaptacja)
