from random import randint
from tqdm import tqdm
import multiprocessing as mp
import matplotlib.pyplot as plt
from Mrowka import Mrowka
from Plansza import Plansza

ROZMIAR_POPULACJI = 10  # [10, 30, 50]
CZYNNIK_LOSOWY = 0.3  # [0.3]
ALFA = 1  # [1, 2]
BETA = 1  # [1, 3]
LICZBA_ITERACJI = 1000
CZYNNIK_PAROWANIA_FEROMONOW = 0.1  # [0.1, 0.5]


def algorytm_mrowkowy(sciezka_pliku, kolor, pozycja, wyniki):
    plansza = Plansza(sciezka_pliku)
    najlepsze_mrowki = []

    for _ in tqdm(range(LICZBA_ITERACJI), colour=kolor, position=pozycja, leave=False):
        ostatnie_miejsce = len(plansza.miejsca) - 1
        mrowki = [Mrowka(randint(0, ostatnie_miejsce)) for _ in range(ROZMIAR_POPULACJI)]
        for _ in range(ostatnie_miejsce):
            for mrowka in mrowki:
                mrowka.nastepny_krok(plansza, ALFA, BETA, CZYNNIK_LOSOWY)

        plansza.aktualizuj_feromony(CZYNNIK_PAROWANIA_FEROMONOW, mrowki)
        najlepsze_mrowki.append(min(mrowki, key=lambda x: x.odleglosc_przebyta(plansza)))
    wyniki[pozycja] = [plansza, najlepsze_mrowki]


def rysuj_iteracje(wyniki):
    fig = plt.figure()
    fig.set_figheight(20)
    fig.set_figwidth(20)
    for i in range(len(wyniki)):
        wykres = fig.add_subplot(4, 2, i + 1, title=wyniki[i][0].tytul)
        wykres.plot(range(1, LICZBA_ITERACJI + 1), [mrowka.odleglosc_przebyta(wyniki[i][0]) for mrowka in wyniki[i][1]])
        plt.xlabel("numer_iteracji")
        plt.ylabel("najkrótsza odległość w populacji mrówek")

    plt.tight_layout()
    plt.show()


def rysuj_trasy(wyniki):
    fig = plt.figure()
    fig.set_figheight(20)
    fig.set_figwidth(20)

    for i in range(len(wyniki)):
        plansza = wyniki[i][0]
        najlepsze_mrowki = wyniki[i][1]
        najlepsza_mrowka = min(najlepsze_mrowki, key=lambda x: x.odleglosc_przebyta(plansza))
        x_wartosci = [plansza.pozycje[miejsce][0] for miejsce in najlepsza_mrowka.odwiedzone_miejsca]
        y_wartosci = [plansza.pozycje[miejsce][1] for miejsce in najlepsza_mrowka.odwiedzone_miejsca]

        wykres = fig.add_subplot(4, 2, i + 1, title=wyniki[i][0].tytul)
        wykres.plot(x_wartosci, y_wartosci, 'ro-')

        plt.annotate('START', plansza.pozycje[najlepsza_mrowka.odwiedzone_miejsca[0]],
                     textcoords="offset points", xytext=(5, -5))
        plt.annotate('END', plansza.pozycje[najlepsza_mrowka.odwiedzone_miejsca[-1]],
                     textcoords="offset points", xytext=(5, -5))
        for miejsce in najlepsza_mrowka.odwiedzone_miejsca:
            plt.annotate(miejsce + 1, plansza.pozycje[miejsce], textcoords="offset points", xytext=(0, 7), ha='center')
        plt.xlabel("Najlepsza znaleziona trasa: " + str(najlepsza_mrowka.odleglosc_przebyta(plansza)))

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    wyniki = mp.Manager().dict()
    procesy = [mp.Process(target=algorytm_mrowkowy, args=("data/A-n32-k5.txt", "black", 0, wyniki)),
               mp.Process(target=algorytm_mrowkowy, args=("data/A-n80-k10.txt", "blue", 1, wyniki)),
               mp.Process(target=algorytm_mrowkowy, args=("data/B-n31-k5.txt", "green", 2, wyniki)),
               mp.Process(target=algorytm_mrowkowy, args=("data/B-n78-k10.txt", "yellow", 3, wyniki)),
               mp.Process(target=algorytm_mrowkowy, args=("data/P-n16-k8.txt", "white", 4, wyniki)),
               mp.Process(target=algorytm_mrowkowy, args=("data/P-n76-k5.txt", "red", 5, wyniki))]

    for proces in procesy:
        proces.start()
    for proces in procesy:
        proces.join()

    rysuj_iteracje([wyniki[klucz] for klucz in sorted(wyniki)])
    rysuj_trasy(wyniki.values())
