import os
import importlib
Functions = importlib.import_module('Files.Functions')


# Checks and installs all required ui modules
def uiCheck(path="python"):
    print("Checking for ui modules")
    print("----------------------START----------------------")
    print("Tkinter")
    result = None
    changed = False
    try:
        import tkinter as tk
        canvas = tk.Tk("Tkinter Test", "TkTest")
        canvas.destroy()  # unfortantlly doesn't remove program
        result = "Found Tk"
    except ModuleNotFoundError:
        def install():
            print('Installing tkinter...')
            os.system('{} -m pip install tk'.format(path))
            return "Installed Tk", True

        r = Functions.check("Do you want to install Tkinter (ui support)?: ",  # noqa E501
                                          returnFunc=(install, ("Nothing", False))).getInput("ynCheck")  # noqa E501
    result, changed = r
    print("-----------------------END-----------------------")
    return result, changed


# Checks for a virtual evniroment.
# Need to update every time
def env():
    print("Checking for virtual enviroment")
    print("----------------------START----------------------")
    print("venv")
    result = "python"
    changed = False
    if not os.path.exists("./.BattleshipsVenv"):
        def install():
            os.system('python -m venv .BattleshipsVenv')
            return "./.BattleshipsVenv/bin/python", True

        result, changed = Functions.check("Do you want to have the modules in a virtual enviroment?: ",  # noqa E501
                                          returnFunc=(install, ("python", False))).getInput("ynCheck")  # noqa E501
    else:
        print('Found virtual enviroment')
    print("-----------------------END-----------------------")
    return result, changed


# Checks for google modules
def google(path):
    return "No", False


if __name__ == "__main__":
    Functions.clear()
    path = env()
    Functions.clear()
    uiCheck(path)
