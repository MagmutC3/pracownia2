"""Klasa, w ktorej mozna zrealizowac rozwiazanie Zadania 1"""

from numpy.lib.function_base import copy
import uklad, wykresy
import iteracjaprosta, iteracjaseidela
import numpy as np

class Zadanie1:

    # powinienem byl podac wartosci jako argumenty __init__ i guess
    def __init__(self):
        """Konstruktor"""
        self.k = 5                   # liczba iteracji
        self.n = 3 # self.zakresN[0] = self.n # rozmiar macierzy o n elementow w wierszu/kolumnie
        self.alfa = 0.01             # parametr metody losującej układ
        self.pomiary = 40            # ilosc pomiarow wykonanych na jednym rozmiarze
        self.zakresN = [3,63]        # zakres wartosci n do zbadania
        self.norma = 1
        self.N = 15

    def testy(self):
        """Testy wstepne"""
        # miejsce na rozwiazanie pierwszej czesci zadania 1

        # wykonaj kilka wstępnych eksperymentów, by określić zakres parametru, 
        # którego wpływ badasz, możesz w tym celu wykorzystać metodę testy()  
        # w pliku zadanie1.py, opisz przebieg testów w raporcie (1 punkt)
        # iter Seidela, iteruj, parametr n, norma 1

        niedokladnosci = []
        for i in range(37):

            ukladA = uklad.Uklad(wymiar = self.n)
            sredniaNiedokladnosc = 0
            for i in range(self.pomiary):
                ukladA.losuj_uklad_symetryczny_dodatnio_okreslony(self.alfa)
                iterSeidelaA = iteracjaseidela.IteracjaSeidela(ukladA)
                iterSeidelaA.przygotuj()
                iterSeidelaA.iteruj(self.k, norma = ukladA.norma_wektora(typ = 1), wyswietlaj = 0)
                sredniaNiedokladnosc += iterSeidelaA.sprawdz_rozwiazanie(2)
            print(f'Rozmiar: {self.n}x{self.n}, alfa = {self.alfa}, k = {self.k}')
            # print(f'Niedokładność: {iterSeidelaA.sprawdz_rozwiazanie(2)}')
            print(f'Średnia niedokładność z {self.pomiary} pomiarów: {sredniaNiedokladnosc/self.pomiary}')

            self.n += 1
            niedokladnosci.append(sredniaNiedokladnosc)
        wykresik = wykresy.Wykresy()
        wykresik.badaj_zbieznosc(
            tytul="Zbieznosc met Seidela dla roznych n",
            opis_OY = "Niedokladnosc rozwiazania",
            dane1 = niedokladnosci.copy(),
            opis1 = "Średnia dokładność rozwiązania",
            dane2 = None,
            opis2 = None,
            dane3 = None,
            opis3 = None)

        return 0
        
    def badaj_zbieznosc(self):
        """Badam zbieznosc metody iteracyjnej"""
        # miejsce na realizacje eksperymentu - drugiej czesci zadania 1

        # zapisz  wybrane  charakterystyki  (normę  macierzy,  liczbę 
        # iteracji  oraz  niedokładność rozwiązania) i dla każdej z nich wyznacz jej 
        # średnią wartość

        # miejsce na listy zmiennych ktore sie roznia miedzy wynikami iteracji
        # dla macierzy o roznych rozmiarach
        srednieNormy = []
        iloscPowtorzenPomiaru = self.pomiary
        srednieNiedokladnosci = []

        # wybrane N rozmiarow macierzy z przedzialu zakresN[0] do [1]
        listaRozmiarow = []
        dlugosc = self.zakresN[1]-self.zakresN[0]
        print(f'min n = {self.zakresN[0]}, max n = {self.zakresN[1]}')
        print(f'dlugosc = {dlugosc}')
        listaRozmiarow.append(self.zakresN[0])
        for i in range(self.N - 1):
            # overengineered, nie zawiera szczytowej wartosci z zakresu
            listaRozmiarow.append(int( dlugosc / self.N * (i+1) ) + self.zakresN[0])
        print(listaRozmiarow)

        for aktualnyRozmiar in listaRozmiarow:
            # miejsce dla srednich wartosci z 40 pomiarow
            lacznaNorma = 0.0
            lacznaNiedokladnosc = 0.0
            # tworzymy uklad o rozmiarze n
            macierzA = uklad.Uklad(wymiar = aktualnyRozmiar)

            i = 0
            while i < iloscPowtorzenPomiaru:
                # miejsce dla wartosci z pojedynczego pomiaru
                norma = 0.0
                niedokladnosc = 0.0
                # losujemy zmienne i rozwiazujemy uklad
                macierzA.losuj_uklad_symetryczny_dodatnio_okreslony(self.alfa)
                macierzASeidela = iteracjaseidela.IteracjaSeidela(macierzA)
                if macierzASeidela.przygotuj() == 1:
                    macierzASeidela.iteruj(
                        iteracje = self.k,
                        norma = self.norma,
                        wyswietlaj = 0,
                        X0 = None
                        )
                    # dopisujemy do listy srednich dla danego n
                    lacznaNorma += macierzA.norma_macierzy(
                        typ = self.norma,
                        macierz = macierzASeidela.D
                        )
                    lacznaNiedokladnosc += macierzASeidela.sprawdz_rozwiazanie(
                        norma = self.norma
                        )
                    # iterujemy petle
                    i += 1

            # dzielimy skumulowany wynik pomiarow przez ich ilosc
            # i dopisujemy do listy zmiennych
            srednieNormy.append(lacznaNorma / iloscPowtorzenPomiaru)
            srednieNiedokladnosci.append(lacznaNiedokladnosc / iloscPowtorzenPomiaru)
        print(f'srednieNormy: {srednieNormy}')
        print(f'srednieNiedokladnosci: {srednieNiedokladnosci}')

        # wykres ilustruje uzyskane srednie
        wykres1 = wykresy.Wykresy()
        wykres1.badaj_zbieznosc(
            tytul="Zbieżność iteracji dla coraz większych macierzy",
            opis_OY = "Średnia niedokładność rozwiązania",
            dane1 = srednieNiedokladnosci.copy(),
            opis1 = "Niedokładność iteracji Seidela"
        )
        wykres2 = wykresy.Wykresy()
        wykres2.badaj_zbieznosc(
            tytul="Średnie wartości norm dla coraz większych macierzy",
            opis_OY = "Średnia norma",
            dane1 = srednieNormy.copy(),
            opis1 = "Norma ||D||1 iteracji Seidela"
        )

        return 0

if __name__ == '__main__':
    test1 = Zadanie1()
    test1.badaj_zbieznosc()



"""

        parametr = self.parametry[0]
        srednieNiedokladnosci = []
        srednieNormy = []
        while parametr < self.parametry[1]:
            sredniaNiedokladnosc = 0
            sredniaNorma = []

            # losuje uklad
            macierzA = uklad.Uklad(wymiar = parametr)
            macierzA.losuj_uklad_symetryczny_dodatnio_okreslony()

            # zamieniam w iter seidela
            macierzASeidela = iteracjaseidela.IteracjaSeidela(ukl = macierzA)
            macierzASeidela.przygotuj()
            normaD = macierzA.norma_macierzy(typ = self.norma)


            parametr += 1

"""