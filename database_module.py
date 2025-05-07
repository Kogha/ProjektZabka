import pandas as pd
import pathlib
import tkinter as tk
import load

def database_module():
    root = tk.Tk()

    root.geometry("600x400")

    name_var = tk.StringVar()
    passw_var = tk.StringVar()

    def submit():
        name = name_var.get()
        password = passw_var.get()

        name_var.set("")
        passw_var.set("")

    name_label = tk.Label(root, text='Username', font=('calibre', 10, 'bold'))

    name_entry = tk.Entry(root, textvariable=name_var, font=('calibre', 10, 'normal'))

    passw_label = tk.Label(root, text='Password', font=('calibre', 10, 'bold'))

    passw_entry = tk.Entry(root, textvariable=passw_var, font=('calibre', 10, 'normal'), show='*')

    sub_btn = tk.Button(root, text='Add product', command=submit)

    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    passw_label.grid(row=1, column=0)
    passw_entry.grid(row=1, column=1)
    sub_btn.grid(row=2, column=1)

    root.mainloop()
load.load_data()
database_module()