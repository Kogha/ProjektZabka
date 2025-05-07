from random import randint
from dostepneID import *
from pandas import *

def dodaj_uzytkownika(imie, nazwisko, email, haslo, ID):
    file = read_csv("customers.csv")
    nowy_uzytkownik = DataFrame([{"Imię": imie, "Nazwisko": nazwisko, "E-mail": email, "Hasło": haslo, "ID": ID}])
    file = concat([file, nowy_uzytkownik], ignore_index=True)
    file.to_csv("customers.csv", index=False)

def rejestracja():
    imie = input("Podaj imie: ")
    nazwisko = input("Podaj nazwisko: ")
    email = input("Podaj e-mail: ")
    haslo = input("Podaj haslo: ")

    generujID = randint(DID)
    dodaj_uzytkownika(imie, nazwisko, email, haslo, generujID)
