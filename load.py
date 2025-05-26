from tkinter import filedialog as fd
import pandas as pd
from pathlib import Path
from tkinter import messagebox
import os

def load_data():
    """Wczytuje dane produktów i klientów z plików.

    Jeśli plik konfiguracyjny `options.txt` nie istnieje lub jest pusty, 
    użytkownik zostanie poproszony o wskazanie plików danych.

    Returns:
        tuple[pandas.DataFrame, pandas.DataFrame]: 
            DataFrame z danymi produktów oraz DataFrame z danymi klientów.

    Raises:
        FileNotFoundError: Jeśli plik danych nie zostanie znaleziony.
        PermissionError: Jeśli brakuje uprawnień do odczytu pliku.
        pd.errors.EmptyDataError: Jeśli plik danych jest pusty.
        pd.errors.ParserError: Jeśli wystąpi błąd formatu danych w pliku CSV.
        UnicodeDecodeError: Jeśli plik CSV ma nieprawidłowe kodowanie.
        ValueError: Jeśli wystąpi nieoczekiwany błąd.
        Exception: Jeśli wystąpi inny niespodziewany błąd.
    """
    plik = Path("options.txt")
    if not plik.exists() or os.stat(plik).st_size == 0:
        file = open("options.txt", "w")
        products = ""
        customers = ""
        while not products:
            products = fd.askopenfilename(
                title='Wybierz bazę danych produktów',
                initialdir='C:\\',
                filetypes=[('Pliki Excel', '*.xlsx')])
        while not customers:
            customers = fd.askopenfilename(
                title='Wybierz bazę danych klientów',
                initialdir='C:\\',
                filetypes=[('Pliki CSV', '*.csv')])
        file.write(products)
        file.write("\n")
        file.write(customers)
        file.close()
    try:
        with open("options.txt", "r") as f:
            lines = [Path(line.strip()) for line in f]
        if not lines[0].exists() or not lines[1].exists():
            print("Ścieżki nieprawidłowe, wybierz ponownie.")
            plik.unlink()
            return load_data()

        products = pd.read_excel(lines[0])
        with open(lines[1], encoding='cp1250') as f:
            raw = f.readlines()
        columns = [col.strip().strip('"') for col in raw[0].split(',')]
        data = [line.strip().split(',') for line in raw[1:]]
        data = [[value.strip('"') for value in row] for row in data]
        customers = pd.DataFrame(data, columns=columns)
        REQUIRED_PRODUCT_COLUMNS = {"Firma", "Nazwa", "Ważność", "Dowóz", "Rodzaj", "Ilość", "Cena"}
        REQUIRED_CUSTOMER_COLUMNS = {"Imię", "Nazwisko", "E-mail", "Hasło", "ID"}

        if not REQUIRED_PRODUCT_COLUMNS.issubset(products.columns):
            messagebox.showerror("Błąd", "Plik produktów nie zawiera wymaganych kolumn.")
            #plik.unlink()
            return load_data()
        if not REQUIRED_CUSTOMER_COLUMNS.issubset(customers.columns):
            messagebox.showerror("Błąd", "Plik klientów nie zawiera wymaganych kolumn.")
            #plik.unlink()
            return load_data()

        return products, customers
    except FileNotFoundError as e:
        print(f"Nie znaleziono pliku: {e.filename}")
    except PermissionError as e:
        print(f"Brak dostępu do pliku: {e.filename}")
    except pd.errors.EmptyDataError:
        print("Plik jest pusty.")
    except pd.errors.ParserError:
        print("Błąd formatu danych w CSV.")
    except UnicodeDecodeError as e:
        print("Błąd kodowania pliku CSV. Spróbuj innego kodowania, np. cp1250.", e)
    except ValueError as e:
        print(f"Nieoczekiwany błąd: {e}")
    except Exception as e:
        print(f"Inny błąd: {type(e).__name__}: {e}")

def reset_file_paths():
    """
    Resetuje ścieżki plików zapisane w `options.txt`.

    Usuwa plik konfiguracyjny i ponownie uruchamia procedurę wyboru plików.

    Returns:
        None
    """
    Path("options.txt").unlink(missing_ok=True)
    load_data()

def get_database_path():
    """
    Pobiera zapisane ścieżki do plików bazy danych.

    Odczytuje ścieżki zapisane w `options.txt` i zwraca je jako listę.

    Returns:
        list[str]: Lista ścieżek do plików bazy danych.
    """
    with open("options.txt", "r") as f:
        lines = [line.strip() for line in f]
    return lines

#load_data()
