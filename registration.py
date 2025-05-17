from random import randint
from dostepneID import *
from pandas import *
from tkinter import *
from load import *

def dodaj_uzytkownika(customers, imie, nazwisko, email, haslo, ID, okno):
    """
    Dodaje nowego użytkownika do bazy danych.

    Args:
        customers (str): Ścieżka do pliku z danymi klientów.
        imie (str): Imię użytkownika.
        nazwisko (str): Nazwisko użytkownika.
        email (str): Adres e-mail użytkownika.
        haslo (str): Hasło użytkownika.
        ID (int): Unikalne ID użytkownika.
        okno (Tk): Instancja głównego okna aplikacji.

    Returns:
        None
    """
    file = read_csv(customers)
    nowy_uzytkownik = DataFrame([{"Imię": imie, "Nazwisko": nazwisko, "E-mail": email, "Hasło": haslo, "ID": ID}])
    file = concat([file, nowy_uzytkownik], ignore_index=True)
    file.to_csv(customers, index=False)
    
    okno.destroy()

def rejestracja():
    """
    Tworzy i uruchamia okno rejestracji użytkownika.

    Funkcja inicjalizuje interfejs graficzny dla procesu rejestracji, 
    pobiera dane użytkownika i przekazuje je do funkcji dodającej użytkownika do bazy danych.

    Returns:
        None
    """
    scieszki = list(get_database_path())
    customers = scieszki[1]
    okno = Tk(className = "rejestracja")
    Label(okno, text='Imie').grid(row=0)
    Label(okno, text='Nazwisko').grid(row=1)
    Label(okno, text='E-mail').grid(row=2)
    Label(okno, text='Haslo').grid(row=3)
    
    imie = Entry(okno)
    nazwisko = Entry(okno)
    email = Entry(okno)
    haslo = Entry(okno)
    
    imie.grid(row=0, column=1)
    nazwisko.grid(row=1, column=1)
    email.grid(row=2, column=1)
    haslo.grid(row=3, column=1)

    #imie = input("Podaj imie: ")
    #nazwisko = input("Podaj nazwisko: ")
    #email = input("Podaj e-mail: ")
    #haslo = input("Podaj haslo: ")

    generujID = randint(DID)
    #dodaj_uzytkownika(imie, nazwisko, email, haslo, generujID)
    Button(okno, text="Zarejestruj", command=lambda: dodaj_uzytkownika(customers, imie.get(), nazwisko.get(), email.get(), haslo.get(), generujID,okno)).grid(row=4, column=1)

    okno.mainloop()
