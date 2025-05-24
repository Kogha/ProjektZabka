import os

DATABASE_DIR = "DATABASE"

def zakup_produktu(client_id, produkt, ilosc):
    #Sprawdzenie czy można kupić produkt (czy jest wystarczająca ilość w bazie danych)
    #Niech zapisuje więcej informacji: Data zakupu
    #Odjęcie kupionych produktów od ich ilości z bazy danych
    sciezka = os.path.join(DATABASE_DIR, str(client_id) + ".txt")
    if not os.path.exists(sciezka):
        f = open(sciezka, "x")

    with open(sciezka, "a", encoding="utf-8") as plik:
        linia = "{}, ilość: {}\n".format(produkt, ilosc)
        plik.write(linia)

    print("Zapisano zakup: " + produkt + ", ilość: " + str(ilosc) + " dla klienta " + str(client_id))

#zakup_produktu(2137, "Sok multiwitamina", 4)