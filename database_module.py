import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from load import load_data
from load import get_database_path
import re

def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Wywołano funkcję: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def database_module(parent):
    
    parent.withdraw()
    root = tk.Toplevel(parent)

    products, customers = load_data()
    products_original = products.copy()
    customers_original = customers.copy()

    sort_states = {"products": {}, "customers": {}}

    root.title("Baza danych")
    root.geometry("1800x800")

    frame_products = ttk.LabelFrame(root, text="Produkty")
    frame_products.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=10, pady=10)

    frame_customers = ttk.LabelFrame(root, text="Klienci")
    frame_customers.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=10, pady=10)

    def sort_by_column(df, tree, column, sort_state):
        """
        Sortuje dane według wybranej kolumny i aktualizuje widok tabeli.

        Obsługuje różne typy danych, w tym liczby, daty i tekst. 
        Jeśli kolumna zawiera mieszane typy, podejmuje próbę konwersji.
    
        Args:
            df (pandas.DataFrame): Dane przechowywane w tabeli.
            tree (ttk.Treeview): Widżet tabeli zawierający dane.
            column (str): Nazwa kolumny, według której należy sortować.
            sort_state (dict): Słownik przechowujący stan sortowania dla każdej kolumny.
    
        Returns:
            None
    
        Raises:
            ValueError: Jeśli konwersja danych nie powiedzie się.
            Exception: Jeśli sortowanie nie powiedzie się.
        """
        ascending = not sort_state.get(column, True)
        sort_state[column] = ascending

        try:
            if pd.api.types.is_numeric_dtype(df[column]):
                df.sort_values(by=column, ascending=ascending, inplace=True, ignore_index=True)
            elif pd.api.types.is_datetime64_any_dtype(df[column]):
                df.sort_values(by=column, ascending=ascending, inplace=True, ignore_index=True)
            elif df[column].dtype == "O":
                try:
                    parsed = pd.to_datetime(df[column], format="%Y-%m-%d %H:%M:%S", errors="coerce")
                    if parsed.notna().sum() >= 0.8:
                        df[column] = parsed
                        df.sort_values(by=column, ascending=ascending, inplace=True, ignore_index=True)
                    else:
                        raise ValueError
                except:
                    df["_sort_key"] = df[column].str.lower()
                    df.sort_values(by="_sort_key", ascending=ascending, inplace=True, ignore_index=True)
                    df.drop(columns=["_sort_key"], inplace=True)
            else:
                df.sort_values(by=column, ascending=ascending, inplace=True, ignore_index=True)

            insert_data(tree, df)

        except Exception as e:
            messagebox.showerror("Błąd sortowania", f"Nie udało się posortować: {e}")

    def create_table(frame, df, df_type):
        """
        Tworzy tabelę z danymi produktów lub klientów w określonym kontenerze.

        Dodaje nagłówki kolumn, wypełnia dane i umożliwia sortowanie po kliknięciu.
    
        Args:
            frame (ttk.LabelFrame): Kontener, w którym zostanie umieszczona tabela.
            df (pandas.DataFrame): Dane do wyświetlenia w tabeli.
            df_type (str): Typ danych (np. "products" lub "customers").
    
        Returns:
            ttk.Treeview: Widżet tabeli zawierający dane.
        """
        tree = ttk.Treeview(frame, columns=list(df.columns), show="headings", selectmode="browse")
        for col in df.columns:
            tree.heading(col, text=col, command=lambda c=col: sort_by_column(df, tree, c, sort_states[df_type]))
            tree.column(col, width=100, anchor=tk.CENTER)
        insert_data(tree, df)
        tree.pack(fill=tk.BOTH, expand=True)
        return tree

    def insert_data(tree, df):
        """
        Wstawia dane do drzewa tabeli na podstawie przekazanego dataframe.

        Usuwa istniejące dane w widżecie Treeview i wypełnia tabelę nowymi wartościami.
    
        Args:
            tree (ttk.Treeview): Widżet Treeview służący do wyświetlania danych.
            df (pandas.DataFrame): Zbiór danych do umieszczenia w tabeli.
    
        Returns:
            None
        """
        tree.delete(*tree.get_children())
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

    def delete_selected(tree, df):
        """
        Usuwa zaznaczony wiersz z tabeli.

        Sprawdza, czy użytkownik wybrał wiersz, a następnie usuwa go z tabeli i dataframe.
    
        Args:
            tree (ttk.Treeview): Widżet tabeli zawierający dane.
            df (pandas.DataFrame): Dane przechowywane w tabeli.
    
        Returns:
            None
    
        Raises:
            ValueError: Jeśli użytkownik nie wybierze wiersza.
        """
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Zaznacz wiersz do usunięcia.")
            return
        index = tree.index(selected[0])
        tree.delete(selected[0])
        df.drop(df.index[index], inplace=True)
        df.reset_index(drop=True, inplace=True)

    @log_call
    def save_changes():
        """
        Zapisuje zmiany w plikach danych.

        Eksportuje dane produktów do pliku Excel oraz klientów do pliku CSV.
    
        Returns:
            None
    
        Raises:
            Exception: Jeśli zapis nie powiedzie się.
        """
        try:
            products.to_excel(lines[0], index=False)
            customers.to_csv(lines[1], index=False, encoding='cp1250')
            messagebox.showinfo("Zapisano", "Zmiany zostały zapisane do plików.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać: {e}")

    def restore_data():
        """
        Przywraca oryginalne dane produktów i klientów.

        Kopiuje pierwotne wartości i aktualizuje widok tabeli.
    
        Returns:
            None
        """
        nonlocal products, customers
        products = products_original.copy()
        customers = customers_original.copy()
        insert_data(tree_products, products)
        insert_data(tree_customers, customers)
        messagebox.showinfo("Przywrócono", "Dane zostały przywrócone.")

    def open_add_window(columns, df, tree, title):
        """
        Tworzy okno dialogowe do dodawania nowych wpisów do tabeli.

        Generuje dynamiczne pola wejściowe na podstawie przekazanych kolumn 
        i umożliwia użytkownikowi dodanie nowego wiersza do danych.
    
        Args:
            columns (list[str]): Lista nazw kolumn, które będą używane do wprowadzania danych.
            df (pandas.DataFrame): DataFrame przechowujący dane.
            tree (ttk.Treeview): Widżet tabeli, który zostanie zaktualizowany.
            title (str): Tytuł okna dialogowego.
    
        Returns:
            None
        """
        popup = tk.Toplevel(root)
        popup.title(title)
        entries = {}

        for i, col in enumerate(columns):
            label = tk.Label(popup, text=col)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(popup)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries[col] = entry

        def add_entry():
            """
            Dodaje nowy wpis do tabeli.

            Pobiera wartości z pól wejściowych, tworzy nowy wiersz w DataFrame
            i aktualizuje widok tabeli.

            Returns:
                None

            Raises:
                ValueError: Jeśli użytkownik nie wypełni wszystkich pól.
            """
            new_row = {col: entries[col].get() for col in columns}
            if any(val == "" for val in new_row.values()):
                messagebox.showwarning("Brak danych", "Wypełnij wszystkie pola.")
                return
            df.loc[len(df)] = list(new_row.values())
            insert_data(tree, df)
            popup.destroy()

            add_button = tk.Button(popup, text="Dodaj", command=add_entry)
            add_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

    def open_edit_window(columns, df, tree, title):
        """
        Tworzy okno dialogowe do edycji istniejącego wpisu w tabeli.

        Pobiera zaznaczony wiersz z tabeli, generuje dynamiczne pola wejściowe 
        na podstawie przekazanych kolumn i umożliwia użytkownikowi edycję danych.
    
        Args:
            columns (list[str]): Lista nazw kolumn, które będą używane do edycji danych.
            df (pandas.DataFrame): DataFrame przechowujący dane.
            tree (ttk.Treeview): Widżet tabeli, który zostanie zaktualizowany.
            title (str): Tytuł okna dialogowego.
    
        Returns:
            None
    
        Raises:
            ValueError: Jeśli użytkownik nie wybierze wiersza do edycji.
        """
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Zaznacz wiersz do edycji.")
            return
        index = tree.index(selected[0])
        current_values = df.iloc[index].tolist()

        popup = tk.Toplevel(root)
        popup.title(title)
        entries = {}

        for i, (col, val) in enumerate(zip(columns, current_values)):
            label = tk.Label(popup, text=col)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(popup)
            entry.insert(0, val)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries[col] = entry

        def apply_changes():
            """
            Zapisuje zmiany w edytowanym wierszu.

            Pobiera wartości z pól edycji, aktualizuje dane w DataFrame 
            oraz odświeża widok tabeli.
    
            Returns:
                None
    
            Raises:
                Exception: Jeśli zapis zmian nie powiedzie się.
            """
            new_values = []
            for col in columns:
                val = entries[col].get()
                dtype = df[col].dtype

                if dtype == "int64":
                    try:
                        val = int(val)
                    except ValueError:
                        messagebox.showerror("Błąd", f"'{col}' musi być liczbą całkowitą.")
                        return
                elif dtype == "float64":
                    try:
                        val = float(val)
                    except ValueError:
                        messagebox.showerror("Błąd", f"'{col}' musi być liczbą zmiennoprzecinkową.")
                        return
                new_values.append(val)

            df.iloc[index] = new_values
            insert_data(tree, df)
            popup.destroy()

        apply_button = tk.Button(popup, text="Zapisz zmiany", command=apply_changes)
        apply_button.grid(row=len(columns), column=0, columnspan=2, pady=10)

    def add_search_bar(frame, df, tree, columns):
        """
        Dodaje pasek wyszukiwania do interfejsu aplikacji.

        Tworzy pole tekstowe umożliwiające filtrowanie produktów lub klientów 
        na podstawie wprowadzonego słowa kluczowego.
    
        Args:
            frame (tk.Frame): Kontener, do którego zostanie dodany pasek wyszukiwania.
            df (pandas.DataFrame): Dane do wyszukiwania.
            tree (ttk.Treeview): Widżet tabeli, który zostanie przefiltrowany.
            columns (list[str]): Lista kolumn, które mogą być użyte do wyszukiwania.
    
        Returns:
            None
        """
        search_frame = tk.Frame(frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(search_frame, text="Szukaj:").pack(side=tk.LEFT, padx=5)

        search_var = tk.StringVar()
        entry = tk.Entry(search_frame, textvariable=search_var)
        entry.pack(side=tk.LEFT, padx=5)

        selected_col = tk.StringVar(value=columns[0])
        dropdown = ttk.Combobox(search_frame, textvariable=selected_col, values=list(columns), state="readonly")
        dropdown.pack(side=tk.LEFT, padx=5)

        def perform_search(*args):
            """
            Wykonuje wyszukiwanie na podstawie przekazanego tekstu.

            Pobiera argumenty przekazane przez użytkownika i dopasowuje je
            do dostępnych danych. Aktualizuje widżet `tree` na podstawie wyników wyszukiwania.

            Args:
                *args: Dynamiczna lista argumentów obejmująca frazę wyszukiwania
                        oraz opcjonalnie wybrane kolumny do filtrowania.

            Returns:
                None
            """
            query = search_var.get().strip().lower()
            col = selected_col.get()

            if not query:
                filtered_df = df
            else:
                filtered_df = df[df[col].astype(str).str.lower().str.contains(query)]

            insert_data(tree, filtered_df)

        entry.bind("<KeyRelease>", perform_search)
        dropdown.bind("<<ComboboxSelected>>", perform_search)

    lines = get_database_path()

    tree_products = create_table(frame_products, products, "products")
    tree_customers = create_table(frame_customers, customers, "customers")

    add_search_bar(frame_products, products, tree_products, products.columns)
    add_search_bar(frame_customers, customers, tree_customers, customers.columns)

    tk.Button(frame_products, text="Usuń produkt", command=lambda: delete_selected(tree_products, products)).pack(pady=3)
    tk.Button(frame_products, text="Dodaj produkt", command=lambda: open_add_window(products.columns, products, tree_products, "Dodaj produkt")).pack(pady=3)
    tk.Button(frame_products, text="Edytuj produkt", command=lambda: open_edit_window(products.columns, products, tree_products, "Edytuj produkt")).pack(pady=3)

    tk.Button(frame_customers, text="Usuń klienta", command=lambda: delete_selected(tree_customers, customers)).pack(pady=3)
    tk.Button(frame_customers, text="Dodaj klienta", command=lambda: open_add_window(customers.columns, customers, tree_customers, "Dodaj klienta")).pack(pady=3)
    tk.Button(frame_customers, text="Edytuj klienta", command=lambda: open_edit_window(customers.columns, customers, tree_customers, "Edytuj klienta")).pack(pady=3)

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(fill=tk.X, pady=10)
    tk.Button(bottom_frame, text="💾 Zapisz zmiany", command=save_changes).pack(side=tk.LEFT, padx=20)
    tk.Button(bottom_frame, text="♻️ Przywróć zmiany", command=restore_data).pack(side=tk.LEFT, padx=20)

    def on_close():
        """
        Obsługuje zamknięcie okna aplikacji.

        Funkcja przywraca okno główne aplikacji i niszczy okno logowania.
    
        Returns:
            None
        """
        parent.deiconify()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    #root.mainloop()

#database_module()
