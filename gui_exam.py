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

        self.showData()


    def showData(self):
        # TODO: Add names
        tree = ttk.Treeview(self.top, columns=list(self.examData.columns), show="headings")
        for col in self.examData.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for _, row in self.examData.iterrows():
            tree.insert("", tk.END, values=list(row))
        tree.pack(side=tk.LEFT, fill=tk.X)