import os

DATABASE_DIR = "DATABASE"

def rejestruj_klienta(client_id):
    sciezka = os.path.join(DATABASE_DIR, client_id + ".txt")
    if os.path.exists(sciezka):
        print("Klient o ID " + client_id + " już istnieje.")
    else:
        with open(sciezka, "w") as plik:
            plik.write("Zakupy klienta:\n")
        print("Zarejestrowano klienta o ID: " + client_id)

def zakup_produktu(client_id, produkt, ilosc):
    sciezka = os.path.join(DATABASE_DIR, client_id + ".txt")
    if not os.path.exists(sciezka):
        print("Błąd: klient o ID " + client_id + " nie istnieje. Najpierw zarejestruj klienta.")
        return

    with open(sciezka, "a") as plik:
        linia = "{}, ilość: {}\n".format(produkt, ilosc)
        plik.write(linia)

    print("Zapisano zakup: " + produkt + ", ilość: " + str(ilosc) + " dla klienta " + client_id)