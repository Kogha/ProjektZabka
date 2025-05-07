import pandas as pd
import pathlib
import tkinter as tk
import load

def database_module():
    products, customers = load.load_data()

database_module()