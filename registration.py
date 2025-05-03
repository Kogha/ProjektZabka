from random import randint
from pandas import *


def IDistnieje(noweID):
    filedata = read_csv("customers.csv")
    for i in filedata['ID'].values:
        if i == noweID:
            return True
        else:
            return False


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

    while True:
        generujID = randint(1000,9999)

        if IDistnieje(generujID) == False:
            dodaj_uzytkownika(imie, nazwisko, email, haslo, generujID)
            break
        else:
            continue
