import tkinter as tk


class UClass:
    def __init__(self):
        self.canvas = tk.Tk("Battleships", "main")
        self.canvas.title("Battleships")

    def screen(self):
        print("Creating screen")

    def button(self, message, command, grid):
        button = tk.Button(self.canvas, text=message, command=command)
        button.grid(column=grid[0], row=grid[1])
        return button


if __name__ == "__main__":
    c = UClass()
    c.button("Quit", c.canvas.destroy, [0, 0])
    c.canvas.mainloop()  # mainloop has to come at the end.
