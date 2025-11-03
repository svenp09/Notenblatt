import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

class exam:
    def __init__(self, parent,examData, metaData):
        self.top = tk.Toplevel(parent)
        self.top.title("Probe")
        self.top.geometry("1000x600")
        self.top.transient(parent)
        self.top.grab_set()
        self.examData = examData
        self.metaData = metaData

        # ---- GRID CONFIG ----
        self.top.rowconfigure(0, weight=1)
        self.top.rowconfigure(1, weight=3)
        self.top.columnconfigure(0, weight=1)
        self.top.columnconfigure(1, weight=1)

         # ---- FRAMES ----
        self.frameNumericalStats = ttk.Frame(self.top, padding=10)
        self.frameNumericalStats.grid(row=0, column = 0)
        self.frameTable = ttk.Frame(self.top, padding=10)
        self.frameTable.grid(row=1, column=0, sticky="nw")

        self.showTable()
        self.showNumericalData()


    def showTable(self):
        # Create a new list of columns that includes the index as the first column
        columns = ["Name"] + list(self.examData.columns)

        tree = ttk.Treeview(self.frameTable, columns=columns, show="headings", height=25)
        for col in self.examData.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for index, row in self.examData.iterrows():
            tree.insert("", tk.END, values=[index]+list(row))
        tree.grid(row=0, column=0, sticky="nsew")
        self.top.rowconfigure(1, weight=3)
        self.top.columnconfigure(0, weight=1)

    def showNumericalData(self):
        
        tree = tk.Label(self.top,
                 text= f"Notenschnitt: {self.metaData["mean"]:.2f}",
                 font=("Helvetica", 20),
                 )
        tree.grid(row = 0, column= 0 )
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

    def showDiagrams(self):
        pass

    
