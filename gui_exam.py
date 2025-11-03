import tkinter as tk
from tkinter import ttk

class exam:
    def __init__(self, parent,examData):
        self.top = tk.Toplevel(parent)
        self.top.title("Probe")
        self.top.geometry("1000x200")
        self.top.transient(parent)
        self.top.grab_set()
        self.examData = examData

        self.showTable()


    def showTable(self):
        # Create a new list of columns that includes the index as the first column
        columns = ["Name"] + list(self.examData.columns)

        tree = ttk.Treeview(self.top, columns=columns, show="headings")
        for col in self.examData.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for index, row in self.examData.iterrows():
            tree.insert("", tk.END, values=[index]+list(row))
        tree.pack(side=tk.LEFT, fill=tk.X)

