import tkinter as tk
import threading


class UClass:
    def ui(self):
        self.canvas = tk.Tk("Battleships", "main")

    def __init__(self):
        # self.thread = threading.Thread(target=self.ui)
        # self.thread.daemon = True
        # self.thread.start()
        self.ui()

    def screen(self):
        print("Creating screen")

    def button(self, message, command, grid):
        button = tk.Button(self.canvas, text=message, command=command)
        button.grid(column=grid[0], row=grid[1])
        return button

    def label(self, message, grid):
        label = tk.Label(self.canvas, text=message)
        label.grid(column=grid[0], row=grid[1])
        return grid

    def options(self, message, command, list):
        for i in range(len(list)):
            self.button(message.format(list[i]), command, [0, i])


if __name__ == "__main__":
    c = UClass()
    c.label("Hello World", [0, 0])
    c.button("Quit", c.canvas.destroy, [0, 1])
    c.canvas.mainloop()  # mainloop has to come at the end.
