import tkinter as tk
from tkinter import ttk, messagebox
from gui_popup import InputPopup
from data_handler import load_data
from gui_exam import exam
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modular Tkinter App")
        self.root.geometry("900x600")

        # Sample DataFrame
        masterData = {"Name":["Schüler A", "Schüler B", "Schüler C"]}
        self.dfMasterData = pd.DataFrame(masterData)

        # ---- GRID CONFIG ----
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=3)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # ---- FRAMES ----
        self.frame_controls = ttk.Frame(self.root, padding=10)
        self.frame_controls.grid(row=0, column=0, sticky="nsew")

        self.frameTableMaster = ttk.Frame(self.root, padding=10)
        self.frameTableMaster.grid(row=1, column=0, sticky="nsew")

        self.frameTableExam = ttk.Frame(self.root, padding=10)
        self.frameTableExam.grid(row=0, column=1, rowspan=2, sticky="nsew")

        # ---- CONTROLS ----
        ttk.Button(self.frame_controls, text="Add Value", command=self.open_popup).grid(row=0, column=0, padx=5)
        ttk.Button(self.frame_controls, text="Save Data", command=self.save_data).grid(row=0, column=1, padx=5)
        ttk.Button(self.frame_controls, text="Lade Probe", command=self.read_data).grid(row=1, column=1, padx=5)

        # ---- MASTER DATA TABLE ----
        self.tree = ttk.Treeview(self.frameTableMaster, columns=list(self.dfMasterData.columns), show="headings")
        for col in self.dfMasterData.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.frameTableMaster.rowconfigure(0, weight=1)
        self.frameTableMaster.columnconfigure(0, weight=1)
        self.update_table()

        # ---- PLOT ----
        self.fig, self.ax = plt.subplots(figsize=(4, 3))
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.frameTableExam)
        self.plot_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.update_plot()

    # --- Update functions ---
    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row in self.dfMasterData.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def update_plot(self):
        pass

    # --- Actions ---
    def open_popup(self):
        popup = InputPopup(self.root)
        self.root.wait_window(popup.top)  # wait for popup to close
        if popup.values:
            self.df.loc[len(self.df)] = popup.values
            self.update_table()
            self.update_plot()

    def save_data(self):
        self.df.to_csv("data.csv", index=False)
        messagebox.showinfo("Saved", "Data saved to data.csv")

    def read_data(self):
        data, meta =load_data()
        exam(self.root, data, meta)

