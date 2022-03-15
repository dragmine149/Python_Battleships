import tkinter as tk
import threading
import time

root = tk.Tk("Test thread")
print("Main thread", threading.get_ident())

label = tk.Label(root, text="Start")
label.grid(row=0, column=0)


def next():
    intvar.set(str(int(intvar.get()) + 1))
    print(intvar.get())


def timer():
    while True:
        print(time.time())
        time.sleep(1)


button = tk.Button(root, text="Next", command=next)
button.grid(row=0, column=1)

intvar = tk.StringVar()
intvar.set("0")
intV = tk.Label(root, textvariable=intvar)
intV.grid(row=0, column=2)


button = tk.Button(root, text="Quit", command=root.destroy)
button.grid(row=1, column=0)

thd = threading.Thread(target=timer)
thd.daemon = True
thd.start()

root.mainloop()
