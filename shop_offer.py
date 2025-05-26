import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from load import load_data
from Zakup_produktow import zakup_produktu

def pokaz_oferte_sklepu(parent, client_id):
    """
    Tworzy i wyświetla okno z ofertą sklepu Żabka.

    Pobiera listę dostępnych produktów, tworzy interfejs użytkownika 
    i umożliwia interakcję z tabelą zawierającą dane produktów.

    Args:
        parent (tk.Tk): Główne okno aplikacji.
        client_id (int): Identyfikator klienta.

    Returns:
        None
    """
    root = tk.Toplevel(parent)
    root.title("Oferta sklepu Żabka")
    root.geometry("1000x600")

    frame = ttk.LabelFrame(root, text="Produkty dostępne w sklepie")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    products, _ = load_data()
    sort_state = {}

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

    def sort_by_column(df, tree, column):
        """
        Sortuje dane według wybranej kolumny i aktualizuje widok tabeli.

        Odwraca bieżący stan sortowania dla wskazanej kolumny i ponownie
        renderuje tabelę.
    
        Args:
            df (pandas.DataFrame): Dane przechowywane w tabeli.
            tree (ttk.Treeview): Widżet Treeview zawierający dane.
            column (str): Nazwa kolumny, według której należy sortować.
    
        Returns:
            None
    
        Raises:
            Exception: Jeśli sortowanie nie powiedzie się.
        """
        ascending = not sort_state.get(column, True)
        sort_state[column] = ascending

        try:
            df.sort_values(by=column, ascending=ascending, inplace=True, ignore_index=True)
            insert_data(tree, df)
        except Exception as e:
            messagebox.showerror("Błąd sortowania", f"Nie udało się posortować: {e}")

    def create_table(frame, df):
        """
        Tworzy tabelę z danymi produktów w określonym kontenerze.

        Dodaje nagłówki kolumn, wypełnia dane i umożliwia sortowanie po kliknięciu.
    
        Args:
            frame (ttk.LabelFrame): Kontener, w którym zostanie umieszczona tabela.
            df (pandas.DataFrame): Dane do wyświetlenia w tabeli.
    
        Returns:
            ttk.Treeview: Widżet tabeli zawierający produkty.
        """
        tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")
        for col in df.columns:
            tree.heading(col, text=col, command=lambda c=col: sort_by_column(df, tree, c))
            tree.column(col, width=120, anchor=tk.CENTER)
        insert_data(tree, df)
        tree.pack(fill=tk.BOTH, expand=True)
        return tree

    def add_search_bar(frame, df, tree, columns):
        """
        Dodaje pasek wyszukiwania do interfejsu aplikacji.

        Tworzy pole tekstowe umożliwiające filtrowanie produktów na podstawie 
        wprowadzonego słowa kluczowego. Użytkownik może wyszukiwać po dowolnej 
        kolumnie z listy `columns`.
    
        Args:
            frame (tk.Frame): Kontener, do którego zostanie dodany pasek wyszukiwania.
            df (pandas.DataFrame): Dane produktów do wyszukiwania.
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
        do dostępnych produktów. Aktualizuje widżet `tree` na podstawie 
        wyników wyszukiwania.
        
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

    tree = create_table(frame, products)
    add_search_bar(frame, products, tree, products.columns)

    # Funkcja zakupu
    def kup_produkt():
        """
        Obsługuje proces zakupu wybranego produktu.

        Sprawdza zaznaczony produkt w tabeli, wywołuje mechanizm zakupu 
        oraz wyświetla komunikat potwierdzający transakcję.
    
        Returns:
            None
    
        Raises:
            ValueError: Jeśli użytkownik nie wybierze produktu.
            Exception: Jeśli zakup nie powiedzie się.
        """
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Zaznacz produkt do zakupu.")
            return
        index = tree.index(selected[0])
        produkt = products.iloc[index]

        try:
            max_ilosc = int(produkt["Ilość"])
        except KeyError:
            messagebox.showerror("Błąd", "Brakuje kolumny 'ilosc' w bazie danych.")
            return

        if max_ilosc <= 0:
            messagebox.showinfo("Brak towaru", "Produkt jest niedostępny.")
            return

        ilosc_str = simpledialog.askstring("Zakup", f"Podaj ilość (max {max_ilosc}):", parent=root)
        if ilosc_str is None:
            return
        if not ilosc_str.isdigit():
            messagebox.showerror("Błąd", "Podaj poprawną liczbę.")
            return

        ilosc = int(ilosc_str)
        if ilosc <= 0:
            messagebox.showerror("Błąd", "Podaj poprawną liczbę.")
            return
        if ilosc > max_ilosc:
            messagebox.showwarning("Błąd", f"Podana ilość przekracza dostępny stan ({max_ilosc}).")
            return

        try:
            zakup_produktu(client_id, produkt["Nazwa"], ilosc)
            messagebox.showinfo("Sukces", f"Kupiono {ilosc} x {produkt['Nazwa']}")
        except Exception as e:
            messagebox.showerror("Błąd zakupu", str(e))

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="🛒 Kup produkt", command=kup_produkt).pack()

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
