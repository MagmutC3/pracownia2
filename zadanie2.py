"""Klasa, w ktorej mozna zrealizowac rozwiazanie Zadania 2"""

import uklad, wykresy
import iteracjaprosta, iteracjaseidela, pagerank, potegowa
import numpy as np

class Zadanie2:
    # iteracja Seidela, met. potęgowa, iteruj_roznica, parametr eps, norma 0

    # nalezy porownacc efektywnosc uzyskiwania rankingu stron
    # dwoma wymienionymi metodami

    def __init__(self):
        """Konstruktor"""
        self.norma = 0
        self.n = 150
        self.N = 15
        self.epsilony = []
        for i in range(self.N):
            self.epsilony.append(1 * (10 ** (-i/3-1)))
        print(f'parametry eps = {self.epsilony}')
        self.k = 20 # liczba pomiarow dla jednej wartosci parametru
        
    def testy(self):
        """Testy wstepne"""
        # miejsce na rozwiazanie pierwszej czesci zadania 2

        # wykonaj kilka wstępnych eksperymentów, by określić zakres parametru,
        # którego wpływ badasz, możesz w tym celu wykorzystać metodę testy()
        # pliku zadanie2.py, opisz przebieg testów w raporcie
        
        seria1 = []
        seria2 = []

        for i in range(self.N):
            seria1Total = 0
            for j in range(self.k):
                macierzA = pagerank.PageRank(nn=self.n)
                macierzA.losuj(gamma=0.1)
                macierzAPotegowa = potegowa.Potegowa(ukl=macierzA.u)
                macierzAPotegowa.iteruj_roznica(
                    eps=self.epsilony[i], 
                    wyswietlaj=0, 
                    y0=None)
                seria1Total += macierzAPotegowa.sprawdz_rozwiazanie(norma=self.norma)
            seria1.append(seria1Total / self.k)

            g = 0
            seria2Total = 0
            while g < self.k:
                macierzA = pagerank.PageRank(nn=self.n)
                macierzA.losuj(gamma=0.1)
                if macierzA.przygotuj_do_iteracji() == 0:
                    continue
                macierzASeidela = iteracjaseidela.IteracjaSeidela(ukl=macierzA.v)
                if macierzASeidela.przygotuj() == 0:
                    continue
                macierzASeidela.iteruj_roznica(
                    eps=self.epsilony[i], 
                    norma=self.norma, 
                    wyswietlaj=0, 
                    X0=None)
                g += 1
                seria2Total += macierzASeidela.sprawdz_rozwiazanie(norma=self.norma)
            seria2.append(seria2Total / self.k)
               
        wykres = wykresy.Wykresy()
        wykres.badaj_zbieznosc_zadanie_2(
            epsList = self.epsilony,
            tytul = "Porównanie efektywności dwóch metod w wyznaczaniu rankingu stron",
            opis_OY = "Niedokladnosc rozwiazania",
            dane1 = seria1,
            opis1 = "metoda potęgowa",
            dane2 = seria2,
            opis2 = "metoda iteracji Seidela"
        )

        return 0
        
    def badaj_zbieznosc(self):
        """Badam zbieznosc metody iteracyjnej"""
        # miejsce na realizacje eksperymentu - drugiej czesci zadania 2

        # uzupełnij ciało metyody badaj_zbieznosc() pligu zadanie2.py i opisz
        # jej działanie w raporcie, a następnie dla każdej z N wartości parametru
        # wykonaj co najmniej trzy eksperymenty, zapisz wybrane charakterystyki
        # (liczbę iteracji, średnią liczbę linków na stronie, niedokładność
        # rozwiązania) i dla każdej z nich wyznacz jej średnią wartość

        # srednie niedokladnosci potegowa
        seria1 = []
        # srednie niedokladnosci seidel
        seria2 = []

        srednieIteracjePotegowa = []
        srednieIteracjeSeidela = []

        srednieIlosciLinkowPot = []
        srednieIlosciLinkowSei = []

        for i in range(self.N):

            laczneIteracjePotegowa = 0.0
            laczneIlosciLinkowPot = 0.0
            seria1Total = 0
            for j in range(self.k):
                macierzA = pagerank.PageRank(nn=self.n)
                macierzA.losuj(gamma=0.1)
                macierzAPotegowa = potegowa.Potegowa(ukl=macierzA.u)
                laczneIteracjePotegowa += macierzAPotegowa.iteruj_roznica(
                    eps=self.epsilony[i], 
                    wyswietlaj=0, 
                    y0=None)
                laczneIlosciLinkowPot += macierzA.srednia_liczba_linkow()
                seria1Total += macierzAPotegowa.sprawdz_rozwiazanie(norma=self.norma)
            seria1.append(seria1Total / self.k)
            srednieIteracjePotegowa.append(laczneIteracjePotegowa)
            srednieIlosciLinkowPot.append(laczneIlosciLinkowPot)

            g = 0
            laczneIteracjeSeidela = 0.0
            laczneIlosciLinkowSei = 0.0
            seria2Total = 0
            while g < self.k:
                macierzA = pagerank.PageRank(nn=self.n)
                macierzA.losuj(gamma=0.1)
                if macierzA.przygotuj_do_iteracji() == 0:
                    continue
                macierzASeidela = iteracjaseidela.IteracjaSeidela(ukl=macierzA.v)
                if macierzASeidela.przygotuj() == 0:
                    continue
                laczneIteracjeSeidela += macierzASeidela.iteruj_roznica(
                    eps=self.epsilony[i], 
                    norma=self.norma, 
                    wyswietlaj=0, 
                    X0=None)
                g += 1
                laczneIlosciLinkowSei += macierzA.srednia_liczba_linkow()
                seria2Total += macierzASeidela.sprawdz_rozwiazanie(norma=self.norma)
            seria2.append(seria2Total / self.k)
            srednieIteracjeSeidela.append(laczneIteracjeSeidela)
            srednieIlosciLinkowSei.append(laczneIlosciLinkowSei)

        print()
        print("Metoda potęgowa:")
        print(f'seria1: {seria1}')
        print(f'srednieIteracjePotegowa: {srednieIteracjePotegowa}')
        print(f'srednieIlosciLinkowPot: {srednieIlosciLinkowPot}')
        print()
        print(f'Metoda iteracji Seidela:')
        print(f'seria2: {seria2}')
        print(f'srednieIteracjeSeidela: {srednieIteracjeSeidela}')
        print(f'srednieIlosciLinkowSei: {srednieIlosciLinkowSei}')
        print()
               
        wykres = wykresy.Wykresy()
        wykres.badaj_zbieznosc_zadanie_2(
            epsList = self.epsilony,
            tytul = "Porównanie efektywności dwóch metod w wyznaczaniu rankingu stron",
            opis_OY = "Ilość iteracji wymaganych od uzyskania przybliżenia < eps",
            dane1 = srednieIteracjePotegowa,
            opis1 = "metoda potęgowa",
            dane2 = srednieIteracjeSeidela,
            opis2 = "metoda iteracji Seidela"
        )

        return 0

if __name__ == '__main__':
    test1 = Zadanie2()
    # test1.testy()
    test1.badaj_zbieznosc()






