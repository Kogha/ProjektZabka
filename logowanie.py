from pandas import *
from tkinter import *

def Poprawne_dane(name, surname, password, okno, popup1):
    data = read_csv('customers.csv')
    user_row = data[(data['Imię'] == name) & (data['Nazwisko'] == surname)]

    if not user_row.empty:
        correct_password = user_row['Hasło'].values[0]
        if correct_password == password:
            return True
        else:
            popup1.config(text="Podane hasło jest nie prawidłowe.")
            return False
    else:
        popup1.config(text="Nie ma użytkownika o podanym imieniu i nazwisku.")
        return False

def sprawdzanie_danych(name, surname, password, okno, popup2, popup1):
    if Poprawne_dane(name, surname, password, okno, popup1) == True:
        popup2.config(text="Logowanie zakończone sukcesem.")
        okno.destroy()
    else:
        popup2.config(text="Spróbuj ponownie.")

def Login():
    okno = Tk(className = "login")
    
    Label(okno, text='Imie').grid(row=0)
    Label(okno, text='Nazwisko').grid(row=1)
    Label(okno, text='Haslo').grid(row=2)
    popup1 = Label(okno, text='')
    popup1.grid(row=3)
    popup2 = Label(okno, text='')
    popup2.grid(row=4)

    popup1.pack()
    popup2.pack()
    
    name = Entry(okno)
    surname = Entry(okno)
    password = Entry(okno)

    Button(okno, text = "Zaloguj się", command = lambda: sprawdzanie_danych(name.get(), surname.get(), password.get(), okno, popup2, popup1)).grid(row = 5, column = 1)
    
    #name = input("Podaj imię: ")
    #surname = input("Podaj nazwisko: ")
    #password = input("Podaj hasło: ")

    okno.mainloop()
