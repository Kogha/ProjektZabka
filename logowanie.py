from pandas import *
from tkinter import *

import Gui
from load import *

def Poprawne_dane(customers, name, surname, password, popup1):
    """
    Sprawdza poprawność danych logowania.

    Args:
        customers (str): Ścieżka do pliku z danymi klientów.
        name (str): Imię użytkownika.
        surname (str): Nazwisko użytkownika.
        password (str): Hasło użytkownika.
        okno (Tk): Instancja głównego okna aplikacji.
        popup1 (Label): Label do wyświetlania informacji o powodzie błędu logowania.

    Returns:
        bool: True, jeśli dane są poprawne, w przeciwnym razie False.
    """
    try:
        data = pd.read_csv(customers,encoding='cp1250')
    except Exception as e:
        popup1.config(text=f"Błąd pliku: {e}")
        return False

    user_row = data[(data['Imię'] == name) & (data['Nazwisko'] == surname)]

    if not user_row.empty:
        correct_password = user_row.iloc[0]['Hasło']
        if correct_password == password:
            return user_row.iloc[0]['ID']
        else:
            popup1.config(text="Podane hasło jest nieprawidłowe.")
            return False
    else:
        popup1.config(text="Nie ma użytkownika o podanym imieniu i nazwisku.")
        return False

def sprawdzanie_danych(customers, name, surname, password, okno, popup2, popup1):
    """
    Weryfikuje dane logowania i aktualizuje komunikaty na ekranie.

    Args:
        customers (str): Ścieżka do pliku z danymi klientów.
        name (str): Imię użytkownika.
        surname (str): Nazwisko użytkownika.
        password (str): Hasło użytkownika.
        okno (Tk): Instancja głównego okna aplikacji.
        popup2 (Label): Label do wyświetlania głównego komunikatu o sukcesie lub błędzie logowania.
        popup1 (Label): Label do wyświetlania informacji o powodzie błędu logowania.
    """
    ID = Poprawne_dane(customers, name, surname, password, popup1)
    if ID:
        popup2.config(text="Logowanie zakończone sukcesem.")
        #okno.after(1000, okno.destroy)
        okno.withdraw()
        Gui.customer_menu(okno, ID)
    else:
        popup2.config(text="Spróbuj ponownie.")

def Login(parent):
    """
    Tworzy i uruchamia okno logowania.
    """
    okno = Toplevel(parent)
    okno.title("Logowanie")
    okno.geometry("300x200")

    sciezki = list(get_database_path())
    customers = sciezki[1]

    Label(okno, text='Imię').grid(row=0, column=0)
    Label(okno, text='Nazwisko').grid(row=1, column=0)
    Label(okno, text='Hasło').grid(row=2, column=0)

    name_entry = Entry(okno)
    surname_entry = Entry(okno)
    password_entry = Entry(okno, show='*')

    name_entry.grid(row=0, column=1)
    surname_entry.grid(row=1, column=1)
    password_entry.grid(row=2, column=1)

    popup1 = Label(okno, text='', fg='red')
    popup1.grid(row=3, column=0, columnspan=2)

    popup2 = Label(okno, text='', fg='blue')
    popup2.grid(row=4, column=0, columnspan=2)

    login_button = Button(okno, text="Zaloguj się", command=lambda: sprawdzanie_danych(
        customers,
        name_entry.get(),
        surname_entry.get(),
        password_entry.get(),
        okno,
        popup2,
        popup1
    ))
    login_button.grid(row=5, column=1)

    def on_close():
        """
        Obsługuje zamknięcie okna aplikacji.

        Funkcja przywraca okno główne aplikacji i niszczy okno logowania.

        Returns:
            None
        """
        parent.deiconify()
        okno.destroy()

    okno.protocol("WM_DELETE_WINDOW", on_close)
    #okno.mainloop()

#Login()
