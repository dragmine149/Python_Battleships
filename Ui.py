import tkinter as tk


class UClass:
    def __init__(self):
        self.canvas = tk.Tk("Battleships", "main")
        self.canvas.mainloop()

    def screen(self):
        print("Creating screen")

    def button(self):
        print("Creating button")


if __name__ == "__main__":
    c = UClass()
