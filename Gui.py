import tkinter as tk
from PIL import Image, ImageTk
from database_module import database_module

### Funkcje Administratora
def add_product():
    window = tk.Toplevel()
    window.title("Dodaj produkt")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj jest dodawanie produktów.").pack(pady=20)

def remove_product():
    window = tk.Toplevel()
    window.title("Usuń produkt")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj jest usuwanie produktów.").pack(pady=20)

def register_customer():
    window = tk.Toplevel()
    window.title("Zarejestruj klienta")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj jest zarejestrowanie klienta.").pack(pady=20)

def remove_customer():
    window = tk.Toplevel()
    window.title("Usuń klienta")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj jest usuwanie klienta.").pack(pady=20)

def purchase_product():
    window = tk.Toplevel()
    window.title("Zakup produktu")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj jest zakup produktu.").pack(pady=20)

def admin_menu():
    window = tk.Toplevel()
    window.title("Menu Administratora")
    window.geometry("400x600")
    window.configure(bg="green")

    tk.Label(window, text="Menu Administratora Żabki", font=("Arial", 16), bg="#6DBE45", fg="white").pack(pady=20)

    tk.Button(window, text="Zarządzaj bazą danych", command=database_module, width=25).pack(pady=5)

### Funkcje Klienta
def shop_offer():
    window = tk.Toplevel()
    window.title("Oferty sklepu")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj są oferty sklepu Żabka.").pack(pady=20)

def shop_menu():
    window = tk.Toplevel()
    window.title("Menu sklepu")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj jest menu sklepu Żabka.").pack(pady=20)

def coupon_zone():
    window = tk.Toplevel()
    window.title("Strefa kuponów")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj znajdziesz kupony.").pack(pady=20)

def anything_for_zapps():
    window = tk.Toplevel()
    window.title("Wszystko za żappsony")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj możesz wydać żappsony!").pack(pady=20)

def customer_menu():
    window = tk.Toplevel()
    window.title("Menu Klienta")
    window.geometry("400x600")
    window.configure(bg="green")

    tk.Label(window, text="Witamy w Żabce", font=("Arial", 16), bg="green", fg="white").pack(pady=20)

    tk.Button(window, text="Oferty sklepu", command=shop_offer, width=25).pack(pady=5)
    tk.Button(window, text="Menu sklepu", command=shop_menu, width=25).pack(pady=5)
    tk.Button(window, text="Strefa kuponów", command=coupon_zone, width=25).pack(pady=5)
    tk.Button(window, text="Wszystko za żappsony", command=anything_for_zapps, width=25).pack(pady=5)

###Start menu
def start_screen():
    root = tk.Tk()
    root.title("Wybierz Tryb")
    root.geometry("1000x1000")
    root.configure(bg="lightgreen")
    img = Image.open("Zabka1.png")
    img = img.resize((400, 300))
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=photo)
    label.pack()

    tk.Label(root, text="Wybierz tryb użytkownika:", font=("Arial", 16), bg="lightgreen").pack(pady=30)
    tk.Button(root, text="Administrator", command=admin_menu, width=25).pack(pady=10)
    tk.Button(root, text="Klient", command=customer_menu, width=25).pack(pady=10)

    root.mainloop()

def start_Gui():
    start_screen()
