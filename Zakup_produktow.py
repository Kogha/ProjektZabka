import os
import pandas as pd
from load import get_database_path
from datetime import datetime

DATABASE_DIR = "DATABASE"

def zakup_produktu(client_id, produkt, ilosc):
    sciezka = os.path.join(DATABASE_DIR, str(client_id) + ".txt")
    lines = get_database_path()
    products = pd.read_excel(lines[0])

    indeks = products[products["Nazwa"] == produkt].index[0]
    dostepna_ilosc = products.at[indeks, "Ilość"]

    if ilosc > dostepna_ilosc:
        print(f"Nie można kupić {ilosc} sztuk. Dostępna ilość: {dostepna_ilosc}")
        return

    products.at[indeks, "Ilość"] -= ilosc

    try:
        products.to_excel(lines[0], index=False)
    except Exception as e:
        print(f"Błąd zapisu bazy danych: {e}")
        return

    if not os.path.exists(sciezka):
        f = open(sciezka, "x")

    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(sciezka, "a", encoding="utf-8") as file:
            file.write("{} | {}, ilość: {}\n".format(data, produkt, ilosc))
        print("Zapisano zakup: {}, ilość: {} dla klienta {} ({})".format(produkt, ilosc, client_id, data))
    except IOError as e:
        print("Wystąpił błąd podczas zapisu do pliku: {}".format(e))


#zakup_produktu(2137, "Sok multiwitamina", 4)