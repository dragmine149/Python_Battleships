import os
import platform
import time


# Checks and installs all required ui modules
def uiCheck(path="python"):
    print("Checking for ui modules")
    print("----------------------START----------------------")
    print("Tkinter")
    try:
        import tkinter as tk
    except ModuleNotFoundError:
        install = None
        while install is None:
            install = input("Do you want to install Tkinter (ui support) (y or n)?: ")
            if install[0].lower() == 'y':
                os.system('{} -m pip install tk'.format(path))
            elif not install[0].lower() == 'n':
                install = None
    print("-----------------------END-----------------------")


# Checks for a virtual evniroment.
def env():
    print("Checking for virtual enviroment")
    print("----------------------START----------------------")
    print("venv")
    if not os.path.exists("./.BattleshipsVenv"):
        virtualEnv = None
        while virtualEnv is None:
            virtualEnv = input("Do you want to have the modules in a virtual enviroment? (y or n):")
            if virtualEnv[0].lower() == "y":
                os.system('python -m venv .BattleshipsVenv')
            elif virtualEnv[0].lower() == "n":
                return 'python'
            else:
                virtualEnv = None

    else:
        print('Found virtual enviroment')
    print("-----------------------END-----------------------")
    # This is different per python version. Big statement here.
    pythonVersion = platform.python_version()
    if pythonVersion[0:3] == '3.8':
        return './.BattleshipsVenv/bin/python'
    else:
        return 'python'


def clearWait():
    time.sleep(1)
    os.system('clear')

if __name__ == "__main__":
    clearWait()
    path = env()
    clearWait()
    uiCheck(path)
