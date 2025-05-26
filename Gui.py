import tkinter as tk
from PIL import Image, ImageTk
from database_module import database_module
from registration import rejestracja
from logowanie import Login
from load import reset_file_paths
from shop_offer import pokaz_oferte_sklepu
### Funkcje Administratora
def purchase_product():
    window = tk.Toplevel()
    window.title("Zakup produktu")
    window.geometry("300x200")
    tk.Label(window, text="Tutaj jest zakup produktu.").pack(pady=20)

def admin_menu(parent):
    parent.withdraw()

    window = tk.Toplevel()
    window.title("Menu Administratora")
    window.geometry("400x600")
    window.configure(bg="green")

    tk.Label(window, text="Menu Administratora Żabki", font=("Arial", 16), bg="#6DBE45", fg="white").pack(pady=20)
    tk.Button(window, text="Zarządzaj bazą danych", command=lambda: database_module(window), width=25).pack(pady=5)
    tk.Button(window, text="Wybierz inne pliki z bazami danych", command=reset_file_paths, width=25).pack(pady=5)

    def on_close():
        parent.deiconify()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

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

def customer_menu(parent, id):
    window = tk.Toplevel(parent)
    window.title("Menu Klienta")
    window.geometry("400x600")
    window.configure(bg="green")

    tk.Label(window, text="Witamy w Żabce", font=("Arial", 16), bg="green", fg="white").pack(pady=20)

    tk.Button(window, text="Oferty sklepu", command=lambda: (window.withdraw(),pokaz_oferte_sklepu(window, id)), width=25).pack(pady=5)
    #tk.Button(window, text="Menu sklepu", command=shop_menu, width=25).pack(pady=5)
    #tk.Button(window, text="Strefa kuponów", command=coupon_zone, width=25).pack(pady=5)
    #tk.Button(window, text="Wszystko za żappsony", command=anything_for_zapps, width=25).pack(pady=5)

    def on_close():
        parent.deiconify()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

def customer_options(parent):
    parent.withdraw()

    window = tk.Toplevel()
    window.title("Menu Klienta")
    window.geometry("400x600")
    window.configure(bg="green")

    tk.Label(window, text="Witamy w Żabce", font=("Arial", 16), bg="green", fg="white").pack(pady=20)
    tk.Button(window, text="Rejestracja", command=lambda: (window.withdraw(), rejestracja(window)), width=25).pack(pady=5)
    tk.Button(window, text="Logowanie", command=lambda: (window.withdraw(),Login(window)), width=25).pack(pady=5)

    def on_close():
        parent.deiconify()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

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
    tk.Button(root, text="Administrator", command=lambda: admin_menu(root), width=25).pack(pady=10)
    tk.Button(root, text="Klient", command=lambda: customer_options(root), width=25).pack(pady=10)

    root.mainloop()

def start_Gui():
    start_screen()
