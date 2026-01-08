from gui_main import MainApp
import tkinter as tk

def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("300x150+500+300")
    label = tk.Label(splash, text="Loading...", font=("Helvetica", 20))
    label.pack(expand=True, fill="both")
    return splash

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide main window

    splash = show_splash()
    root.after(2000, splash.destroy)  # Simulate loading, destroy splash after 2s

    # ... load your data, setup GUI, etc. ...

    root.deiconify()  # Show main window

    app = MainApp(root)
    root.mainloop()
