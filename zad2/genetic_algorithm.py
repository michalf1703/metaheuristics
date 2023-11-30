import random
from bitarray.util import urandom
from data import DATA, BAG_MAX_WEIGHT

#unrandom -> ciag losowych bitow o dl 26 (tyle jest przedmiotow)
def losowy_osobnik():
    return urandom(26)

# Funkcja zwracająca sumę przystosowania całej populacji
def oblicz_sume_przystosowania_populacji(populacja):
    suma = 0
    for osobnik in populacja:
        suma += oblicz_przystosowanie(osobnik)
    return suma

# Funkcja zwracająca średnie przystosowanie osobnika z populacji
def oblicz_srednie_przystosowanie_populacji(populacja):
    return oblicz_sume_przystosowania_populacji(populacja) / len(populacja)

def oblicz_maksymalne_przystosowanie_populacji(populacja):
    maksimum = 0
    for osobnik in populacja:
        if maksimum < oblicz_przystosowanie(osobnik):
            maksimum = oblicz_przystosowanie(osobnik)
    return maksimum

def oblicz_minimalne_przystosowanie_populacji(populacja):
    if not populacja:
        return None
    return min(oblicz_przystosowanie(osobnik) for osobnik in populacja)


# Funkcja zwracająca wartość przystosowania jednego osobnika
def oblicz_przystosowanie(osobnik):
    suma_wagi = 0
    suma_wartosci = 0
    for i in range(len(osobnik)):
        #sprawdzamy czy w danym miejscu ustawione jest 1
        if osobnik[i]:
            suma_wagi += DATA[i][1]
            suma_wartosci += DATA[i][2]
    if suma_wagi > BAG_MAX_WEIGHT:
        return 0
    else:
        return suma_wartosci

def selekcja_ruletkowa(populacja):
    suma_przystosowania = oblicz_sume_przystosowania_populacji(populacja)
    if suma_przystosowania == 0: #nie mozna przeprowadzic ruletki jak 0
        return populacja
    tabela_prawdopodobienstw = {}
    for i in range(len(populacja)):
        tabela_prawdopodobienstw[i] = oblicz_przystosowanie(populacja[i]) / suma_przystosowania
    #wybor losowych indeksow z uwzglednieniem prawdopodobienstw
    indeksy = random.choices(list(tabela_prawdopodobienstw.keys()),
                             weights=list(tabela_prawdopodobienstw.values()),
                             k=len(populacja))
    return [populacja[indeks] for indeks in indeksy]


# Funkcja zwracająca rodziców wybranych do krzyżowania
def selekcja_elitarna(populacja):
    tabela_rankingowa = {}
    for i in range(len(populacja)):
        tabela_rankingowa[i] = oblicz_przystosowanie(populacja[i])
    #posortowanie według malejącego przystosowania
    indeks = sorted(tabela_rankingowa.items(), key=lambda item: -item[1])
    lepsza_polowa = [populacja[indeks[i][0]] for i in range(int(len(populacja) / 2))]
    return lepsza_polowa + lepsza_polowa

# Funkcja zwracająca ocalałych i rodziców wybranych do krzyżowania
def wybierz_rodzicow(populacja, prawdopodobienstwo_krzyzowania, czy_ruletka):
    #tasujemy funkcje, zeby kolejnosc byla losowa
    random.shuffle(populacja)
    #liczba osobonikow do krzyzowania
    liczba_do_wyboru = int(prawdopodobienstwo_krzyzowania * len(populacja))
    wybrani_osobnicy = populacja[:liczba_do_wyboru]
    pozostali_osobnicy = populacja[liczba_do_wyboru:]
    if czy_ruletka:
        return pozostali_osobnicy, selekcja_ruletkowa(wybrani_osobnicy)
    else:
        return pozostali_osobnicy, selekcja_elitarna(wybrani_osobnicy)

# Funkcja zwracająca dwójkę dzieci z krzyżowaniem genów na podstawie dwóch rodziców
def krzyzowanie_genow(rodzice, czy_jednopunktowe):
    punkt_krzyzowania = random.randint(1, 24)
    punkt_krzyzowania_2 = random.randint(1, 24)
    if punkt_krzyzowania > punkt_krzyzowania_2:
        punkt_krzyzowania, punkt_krzyzowania_2 = punkt_krzyzowania_2, punkt_krzyzowania
    if czy_jednopunktowe:
        return [rodzice[0][:punkt_krzyzowania] + rodzice[1][punkt_krzyzowania:],
                rodzice[1][:punkt_krzyzowania] + rodzice[0][punkt_krzyzowania:]]
    else:
        return [rodzice[0][:punkt_krzyzowania] + rodzice[1][punkt_krzyzowania:punkt_krzyzowania_2] + rodzice[0][punkt_krzyzowania_2:],
                rodzice[1][:punkt_krzyzowania] + rodzice[0][punkt_krzyzowania:punkt_krzyzowania_2] + rodzice[1][punkt_krzyzowania_2:]]


# Funkcja zwracająca losowe pary z populacji
def wybierz_pary(populacja):
    pary = []
    #tasowanie populacji
    random.shuffle(populacja)
    i = 0
    #tworzymy kolejne pary
    while i < len(populacja) - 1:
        pary.append([populacja[i], populacja[i + 1]])
        i += 2
    #jeśli nieparzysta populacja to ostatni łączy się z pierwszym - dodatkowa para
    if len(populacja) % 2 == 1:
        pary.append([populacja[len(populacja) - 1], populacja[0]])
    return pary

# Funkcja zwracająca nową populację na podstawie par rodziców
def nowa_generacja(pary, czy_jednopunktowe):
    dzieci = []
    for para in pary:
        dzieci += krzyzowanie_genow(para, czy_jednopunktowe)
    return dzieci

# Funkcja zwracająca populację z losowo zmienionymi genami
def mutuj_populacje(populacja, prawdopodobienstwo):
    random.shuffle(populacja)
    for i in range(int(prawdopodobienstwo * len(populacja))):
        #losowemu osobnikowi zmienia losowy bit na przeciwny
        populacja[i].invert(random.randint(0, 25))
    return populacja

# Funkcja zwracająca finalną populację wygenerowaną przez algorytm genetyczny
def algorytm_genetyczny(rozmiar_populacji=20,
                        liczba_iteracji=30,
                        prawdopodobienstwo_krzyzowania=0.9,
                        prawdopodobienstwo_mutacji=0.01,
                        ruletka=True,
                        jednopunktowe=False):
    populacja = []
    for i in range(rozmiar_populacji):
        populacja.append(losowy_osobnik())
    for i in range(liczba_iteracji):
        #ocalali - osobniki niebrani, rodzice - osobnicy brani do krzyzowania
        ocalali, rodzice = wybierz_rodzicow(populacja, prawdopodobienstwo_krzyzowania, ruletka)
        pary = wybierz_pary(rodzice)
        dzieci = mutuj_populacje(nowa_generacja(pary, jednopunktowe), prawdopodobienstwo_mutacji)
        populacja = ocalali + dzieci
    return populacja

