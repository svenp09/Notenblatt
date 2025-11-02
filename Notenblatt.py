import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Beispiel-Daten
# Master Data
masterData = {"Name":["Schüler A", "Schüler B", "Schüler C"]}
dfMasterData = pd.DataFrame(masterData)

data = {"Monat": ["Jan", "Feb", "Mär", "Apr", "Mai"],
        "Umsatz": [1200, 1500, 1700, 1300, 1600]}
df = pd.DataFrame(data)

root = tk.Tk()
root.title("Notenblatt")
root.geometry("700x500")

allData ={}
allData["masterData"] = dfMasterData

nProben = 0

def newStudent():
    pass

def open_input_window():
    # Create subwindow
    popup = tk.Toplevel(root)
    popup.title("Gib einen Wert ein")
    popup.geometry("250x150")

    tk.Label(popup, text="Anzahl der Aufgaben:").pack(pady=10)
    spinbox_var = tk.StringVar(value="3")
    spinbox = tk.Spinbox(
        popup,
        from_=0,
        to=20,
        textvariable=spinbox_var,
    )
    spinbox.pack(padx=5, pady=20, fill="x")

    # close subwindow
    tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)
    return int(spinbox_var.get())

def createNewExam():
   
    nTasks = open_input_window()
    nProben = 3

    tasks = {}
    tasks["Name"] = allData["masterData"]["Name"]
    for task in range(nTasks):
        tasks["Aufgabe " + str(task)] ={}

    dfExam = pd.DataFrame(tasks)
    allData["Probe " + str(nProben)] =  dfExam

    # --- Tabelle Probe ---
    frame_table = ttk.Frame(root)
    frame_table.pack(side=tk.RIGHT, fill=tk.X, padx=10, pady=10)

    tree = ttk.Treeview(frame_table, columns=list(allData["Probe 3"].columns), show="headings")
    for col in allData["Probe 3"].columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for _, row in allData["Probe 3"].iterrows():
        tree.insert("", tk.END, values=list(row))
    tree.pack(side=tk.LEFT, fill=tk.X)
     

# Add new student
btn_newStudent = tk.Button(root, text="Neuer Schüler", command=newStudent)
btn_newStudent.pack(padx=10, pady=10)

# Add new student
btn_newStudent = tk.Button(root, text="Neue Probe Hinzufügen", command=createNewExam)
btn_newStudent.pack(padx=10, pady=10)

# --- Tabelle ---
frame_table = ttk.Frame(root)
frame_table.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

tree = ttk.Treeview(frame_table, columns=list(dfMasterData.columns), show="headings")
for col in dfMasterData.columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
for _, row in dfMasterData.iterrows():
    tree.insert("", tk.END, values=list(row))
tree.pack(side=tk.LEFT, fill=tk.X)





# --- Diagramm ---
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(df["Monat"], df["Umsatz"], marker="o", color="blue")
ax.set_title("Umsatzentwicklung")
ax.set_xlabel("Monat")
ax.set_ylabel("Umsatz (€)")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# --- Speichern-Funktion ---
def speichern():
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV-Dateien", "*.csv"), ("Alle Dateien", "*.*")]
    )
    if filename:
        df.to_csv(filename, index=False)
        messagebox.showinfo("Gespeichert", f"Daten gespeichert als:\n{filename}")

btn_save = ttk.Button(root, text="Daten speichern", command=speichern)
btn_save.pack(side=tk.BOTTOM, pady=10)

root.mainloop()