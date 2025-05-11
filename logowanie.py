from pandas import *

def Poprawne_dane(name, surname, password):
    data = read_csv('customers.csv')
    user_row = data[(data['Imię'] == name) & (data['Nazwisko'] == surname)]

    if not user_row.empty:
        correct_password = user_row['Hasło'].values[0]
        if correct_password == password:
            return True
        else:
            print("Podane hasło jest nie prawidłowe. \n")
            return False
    else:
        print("Nie ma użytkownika o podanym imieniu i nazwisku. \n")
        return False

def Login():
    name = input("Podaj imię: ")
    surname = input("Podaj nazwisko: ")
    password = input("Podaj hasło: ")

    if Poprawne_dane(name, surname, password) == True:
        print("Logowanie zakończone sukcesem. \n")
    else:
        print("Spróbuj ponownie. \n")