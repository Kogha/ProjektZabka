import pandas as pd
import pathlib
import tkinter as tk
from load import load_data

def database_module():
    products, customers = load_data()
    print(products, customers)
database_module()