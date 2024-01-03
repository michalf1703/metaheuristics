from random import random


class Czastka:
    def __init__(self, x, y, bezwladnosc, stala_poznawcza, stala_spoleczna, funkcja_adaptacji, dziedzina):
        self.bezwladnosc = bezwladnosc
        self.stala_poznawcza = stala_poznawcza
        self.stala_spoleczna = stala_spoleczna
        self.funkcja_adaptacji = funkcja_adaptacji
        self.dziedzina = dziedzina
        self.predkosc_x = 0
        self.predkosc_y = 0
        self.x = x
        self.y = y
        self.aktualna_adaptacja = self.oblicz_adaptacje()
        self.najlepszy_x = x
        self.najlepszy_y = y
        self.najlepsza_adaptacja = self.aktualna_adaptacja

    def oblicz_adaptacje(self):
        return self.funkcja_adaptacji(self.x, self.y)

    def aktualizuj_adaptacje(self):
        self.aktualna_adaptacja = self.oblicz_adaptacje()
        if self.aktualna_adaptacja > self.najlepsza_adaptacja:
            self.najlepsza_adaptacja = self.aktualna_adaptacja
            self.najlepszy_x = self.x
            self.najlepszy_y = self.y

    def aktualizuj_predkosc(self, najlepszy_x_w_populacji, najlepszy_y_w_populacji):
        self.predkosc_x = self.bezwladnosc * self.predkosc_x + \
                           (self.stala_spoleczna * random()) * (najlepszy_x_w_populacji - self.x) + \
                           (self.stala_poznawcza * random()) * (self.najlepszy_x - self.x)

        self.predkosc_y = self.bezwladnosc * self.predkosc_y + \
                           (self.stala_poznawcza * random()) * (self.najlepszy_y - self.y) + \
                           (self.stala_spoleczna * random()) * (najlepszy_y_w_populacji - self.y)

    def aktualizuj_pozycje(self):
        if self.x + self.predkosc_x < self.dziedzina[0]:
            self.x = self.dziedzina[0]
        elif self.x + self.predkosc_x > self.dziedzina[1]:
            self.x = self.dziedzina[1]
        else:
            self.x += self.predkosc_x

        if self.y + self.predkosc_y < self.dziedzina[0]:
            self.y = self.dziedzina[0]
        elif self.y + self.predkosc_y > self.dziedzina[1]:
            self.y = self.dziedzina[1]
        else:
            self.y += self.predkosc_y