import os


def uiCheck(path):
    print("Checking for ui modules")
    print("----------------------START----------------------")
    print("Tkinter")
    tkMod = False
    while not tkMod:
        try:
            import tkinter as tk
            tkMod = True
        except ModuleNotFoundError:
            install = input("Do you want to install Tkinter (ui support) (y or n)?: ")
            if install[0].lower() == 'y':
                os.system('python -m pip install tk')
    print("-----------------------END-----------------------")
