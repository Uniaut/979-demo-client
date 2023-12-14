import tkinter as tk

from src.mainframe import Mainframe

def main():
    root = tk.Tk()
    root.geometry("1480x720")
    Mainframe(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()