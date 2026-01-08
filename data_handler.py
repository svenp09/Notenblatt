from importlib.metadata import metadata
import pandas as pd
from tkinter import ttk, messagebox, filedialog

def load_data():
    file_path = filedialog.askopenfilename(
        title="Select a data file",
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"),  ("All files", "*.*")]
        )

    #file_path = "./Test/testdata.xlsx"
    if not file_path:
        return

    try:
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path, index_col=0)
        else:
            df = pd.read_csv(file_path)
        messagebox.showinfo("Loaded", f"Loaded data from:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load data:\n{e}")

    bins = [0.00,0.24,0.25,0.38,0.39,0.56,0.57,0.76,0.77,0.90,0.91,1.01]
    grades =[6,5,5,4,4,3,3,2,2,1,1]

    # Calculate row offset
    df_non_numeric ={}
    if "Kategorie" in df.index:
        df_non_numeric = df.iloc[0:1]   
        df = df.iloc[1:]  # Exclude non-numeric rows
    else:
        df_non_numeric = pd.DataFrame()
    
    metadata = {}
    df["Gesamt Punkte"] = df.sum(axis=1)
    df["Punkte Relativ"] = df["Gesamt Punkte"]/df["Gesamt Punkte"].iloc[0]
    df["Note"] = pd.cut(df["Punkte Relativ"],bins=bins, labels=grades, right=False, ordered=False) 
    print(df["Note"].iloc[1:].dtype)

    # Calculate meta data
    metadata["mean"] = pd.to_numeric(df["Note"].iloc[1:], errors="coerce").mean()

    return df,df_non_numeric, metadata

def save_data(df, path):
    df.to_csv(path, index=False)