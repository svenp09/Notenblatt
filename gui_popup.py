import tkinter as tk
from tkinter import ttk

class InputPopup:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Add Entry")
        self.top.geometry("300x200")
        self.top.transient(parent)
        self.top.grab_set()

        tk.Label(self.top, text="Month:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_month = tk.Entry(self.top)
        self.entry_month.grid(row=0, column=1)

        tk.Label(self.top, text="Revenue:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_revenue = tk.Entry(self.top)
        self.entry_revenue.grid(row=1, column=1)

        ttk.Button(self.top, text="OK", command=self.submit).grid(row=2, column=0, columnspan=2, pady=10)

        self.values = None

    def submit(self):
        month = self.entry_month.get().strip()
        revenue = self.entry_revenue.get().strip()
        if month and revenue:
            try:
                self.values = [month, float(revenue)]
            except ValueError:
                self.values = None
        self.top.destroy()
