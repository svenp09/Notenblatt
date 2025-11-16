import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class exam:
    def __init__(self, parent,examData, metaData:pd.DataFrame):
        self.top = tk.Toplevel(parent)
        self.top.title("Probe")
        self.top.geometry("1600x600")
        self.top.transient(parent)
        self.top.grab_set()
        self.examData = examData
        self.metaData = metaData

        # Count number of tasks from examData columns 
        self.nTasks = len(self.examData.columns) - 3

        # ---- GRID CONFIG ----
        self.top.rowconfigure(0, weight=1)
        self.top.rowconfigure(1, weight=3)
        self.top.rowconfigure(2, weight=1)
        self.top.rowconfigure(3, weight=1)
        
        # Add column for each task
        for i in range(self.nTasks + 1):
                self.top.columnconfigure(i, weight=1)
        
        self.top.columnconfigure(self.nTasks + 1, weight=1)

         # ---- FRAMES ----
        self.frameNumericalStats = ttk.Frame(self.top, padding=10)
        self.frameNumericalStats.grid(row=0, column = 0)
        self.frameTable = ttk.Frame(self.top, padding=10)
        self.frameTable.grid(row=1, column=0, sticky="nw", columnspan= self.nTasks)
        self.frameFigureExam = ttk.Frame(self.top, padding=10)
        self.frameFigureExam.grid(row=0, column=self.nTasks + 1, rowspan=2)
        self.frameDiagrams = ttk.Frame(self.top, padding=10)
        self.frameDiagrams.grid(row=2, column=0)

        self.showTable()
        self.showNumericalData()
        self.showStats()
        for i in range(self.nTasks):
            self.showTaskDiagram(i) 


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
                 text= f"Notenschnitt: {self.metaData['mean']:.2f}",
                 font=("Helvetica", 20),
                 )
        tree.grid(row = 0, column= 0 )
        self.top.rowconfigure(0, weight=1)
        self.top.columnconfigure(0, weight=1)

    def showStats(self):
        self.fig, self.ax = plt.subplots(nrows=2, ncols=1,figsize=(8, 4))
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=self.frameFigureExam)

        bins = np.arange(0.5, 6.500001, 1)  # edges -> centers will be 1,2,...,6

        counts, edges, patches = self.ax[0].hist(self.examData["Note"], bins=bins, rwidth=0.8)
        # place labels directly under each bin (centered)
        centers = 0.5 * (edges[:-1] + edges[1:])
        self.ax[0].set_xticks(centers)
        self.ax[0].set_xticklabels([str(int(c)) for c in centers])
        self.ax[0].set_title("Notenverteilung")

        # compute spacing so labels don't leave the plot
        y_max = counts.max() if counts.size else 0
        pad = max(0.5, y_max * 0.05)            # vertical padding
        top = max(y_max + pad * 2, 1)           # room above highest bar
        self.ax[0].set_ylim(0, top)

        # annotate counts: put inside bar if there's space, otherwise above
        for ct, x in zip(counts, centers):
            txt = str(int(ct))
            if ct >= pad * 4:  # enough room to draw inside the bar
                # place inside near the top of the bar, use contrasting color
                self.ax[0].text(x, ct - pad/2, txt, ha="center", va="top",
                                color="white", fontsize=9, weight="bold", clip_on=True)
            else:
                # place above the bar
                self.ax[0].text(x, ct + pad, txt, ha="center", va="bottom",
                                color="black", fontsize=9, clip_on=True)

        self.plot_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.plot_canvas.draw()
        pass


    def showTaskDiagram(self, taskIndex):

        currentFrame = ttk.Frame(self.top, padding=10)
        currentFrame.grid(row=2, column=taskIndex)

        fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(5, 3))
        plot_canvas = FigureCanvasTkAgg(fig, master=currentFrame)

        # Plot points distribution for single task

        bins = np.arange(-0.5, self.examData[f"Aufgabe {taskIndex+1}"][0]+0.500001, 1)  # edges -> centers will be 0,1,...,maxPoints

        counts, edges, patches = ax.hist(self.examData[f"Aufgabe {taskIndex+1}"], bins=bins, rwidth=0.8)
        # place labels directly under each bin (centered)
        centers = 0.5 * (edges[:-1] + edges[1:])
        ax.set_xticks(centers)
        ax.set_xticklabels([str(int(c)) for c in centers], rotation=90)
        ax.set_title(f"Aufgabe {taskIndex+1}")

        # compute spacing so labels don't leave the plot
        y_max = counts.max() if counts.size else 0
        pad = max(0.5, y_max * 0.05)            # vertical padding
        top = max(y_max + pad * 2, 1)           # room above highest bar
        ax.set_ylim(0, top)

        # annotate counts: put inside bar if there's space, otherwise above
        for ct, x in zip(counts, centers):
            txt = str(int(ct))
            if ct >= pad * 4:  # enough room to draw inside the bar
                # place inside near the top of the bar, use contrasting color
                ax.text(x, ct - pad/2, txt, ha="center", va="top",
                                color="white", fontsize=9, weight="bold", clip_on=True)
            else:
                # place above the bar
                ax.text(x, ct + pad, txt, ha="center", va="bottom",
                                color="black", fontsize=9, clip_on=True) 
                
        # Add average line 
        abs_avg = self.examData[f"Aufgabe {taskIndex+1}"].mean()
        rel_avg = (abs_avg / self.examData[f"Aufgabe {taskIndex+1}"][0]) * 100
        ax.axvline(abs_avg, color='red', linestyle='dashed', linewidth=1)
        ax.text(abs_avg + 0.1, top * 0.9, f'\xF8: {rel_avg:.2f} %', color='red', fontsize=8)   

        plot_canvas.get_tk_widget().pack(fill="both", expand=True)
        plot_canvas.draw()

        # Add text below for average absolute and relative
        currentFrame.grid(row=3, column=taskIndex)
        tree = tk.Label(currentFrame,
                        text = f'Abs \xF8: {abs_avg:.2f}\nRel \xF8: {rel_avg:.2f}%',
                        font=("Helvetica", 8),
            )
            # Align text below each subplot

        tree.pack(side="left", padx=5)
        
    
    
