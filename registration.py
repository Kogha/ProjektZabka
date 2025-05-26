from random import randint
from dostepneID import *
from pandas import *
from tkinter import *
from load import *
import re
import Gui

def waliduj_dane(imie, nazwisko, email, haslo):
    """
    Walidacja danych podanych przez użytkownika.

    Args:
        imie (str): Imię użytkownika.
        nazwisko (str): Nazwisko użytkownika.
        email (str): Adres E-mail użytkownika.
        haslo (str): Hasło użytkownika.
    Returns:
        None
    """
    if not imie.isalpha():
        return "Imię powinno zawierać tylko litery."
    if not nazwisko.isalpha():
        return "Nazwisko powinno zawierać tylko litery."
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Niepoprawny adres e-mail."
    if len(haslo) < 6:
        return "Hasło powinno mieć co najmniej 6 znaków."
    return None


def dodaj_uzytkownika(customers, imie, nazwisko, email, haslo, ID, okno, etykieta_bledu):
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
        etykieta_bledu (TK): Label wyświetlający błąd przy podaniu błędnych danych

    Returns:
        None
    """
    blad = waliduj_dane(imie, nazwisko, email, haslo)
    if blad:
        etykieta_bledu.config(text=f"Błąd: {blad}")
        return
    else:
        lines = get_database_path()
        file = read_csv(lines[1], encoding='cp1250')
        nowy_uzytkownik = DataFrame([{"Imię": imie, "Nazwisko": nazwisko, "E-mail": email, "Hasło": haslo, "ID": ID}])
        file = concat([file, nowy_uzytkownik], ignore_index=True)
        file.to_csv(customers, index=False, encoding="cp1250")
    okno.withdraw()
    Gui.customer_menu(okno, ID)


def rejestracja(parent):
    """
    Tworzy i uruchamia okno rejestracji użytkownika.

    Funkcja inicjalizuje interfejs graficzny dla procesu rejestracji, 
    pobiera dane użytkownika i przekazuje je do funkcji dodającej użytkownika do bazy danych.

    Returns:
        None
    """
    scieszki = list(get_database_path())
    customers = scieszki[1]
    okno = Toplevel(parent)
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

    etykieta_bledu = Label(okno, text="")
    etykieta_bledu.grid(row=5, column=1)

    #imie = input("Podaj imie: ")
    #nazwisko = input("Podaj nazwisko: ")
    #email = input("Podaj e-mail: ")
    #haslo = input("Podaj haslo: ")
    generujID = 999
    while generujID not in DID:
        generujID = randint(list(DID)[0], list(DID)[-1])
    #dodaj_uzytkownika(imie, nazwisko, email, haslo, generujID)
    Button(okno, text="Zarejestruj", command=lambda: dodaj_uzytkownika(customers, imie.get(), nazwisko.get(), email.get(), haslo.get(), generujID,okno, etykieta_bledu)).grid(row=4, column=1)

    def on_close():
        parent.deiconify()
        okno.destroy()

    okno.protocol("WM_DELETE_WINDOW", on_close)
#rejestracja()