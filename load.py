from tkinter import filedialog as fd
import pandas as pd
from pathlib import Path

def load_data():
    plik = Path("options.txt")
    if not plik.exists():
        file = open("options.txt", "w")
        products = ""
        customers = ""
        while not products:
            products = fd.askopenfilename(
                title='Wybierz bazę danych produktów',
                initialdir='C:\\Users\\Kogha\\PycharmProjects\\Zabka\\database',
                filetypes=[('Pliki Excel', '*.xlsx')])
        while not customers:
            customers = fd.askopenfilename(
                title='Wybierz bazę danych klientów',
                initialdir='C:\\Users\\Kogha\\PycharmProjects\\Zabka\\database',
                filetypes=[('Pliki CSV', '*.csv')])
        file.write(products)
        file.write("\n")
        file.write(customers)
        file.close()
    try:
        with open("options.txt", "r") as f:
            lines = [Path(line.strip()) for line in f]

        pd.read_excel(lines[0])
        pd.read_csv(lines[1], encoding='cp1250')
    except FileNotFoundError as e:
        print(f"Nie znaleziono pliku: {e.filename}")
    except PermissionError as e:
        print(f"Brak dostępu do pliku: {e.filename}")
    except pd.errors.EmptyDataError:
        print("Plik jest pusty.")
    except pd.errors.ParserError:
        print("Błąd formatu danych w CSV.")
    except UnicodeDecodeError:
        print("Błąd kodowania pliku CSV. Spróbuj innego kodowania, np. cp1250.")
    except ValueError as e:
        print(f"Nieoczekiwany błąd: {e}")
    except Exception as e:
        print(f"Inny błąd: {type(e).__name__}: {e}")
load_data()