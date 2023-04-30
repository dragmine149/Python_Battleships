import os
from PythonFunctions.Save import save
from PythonFunctions.TerminalDisplay import Display
from PythonFunctions.Check import Check
from PythonFunctions.Searching import search
from PythonFunctions import Message
from colorama import Fore


class Settings:

    # does some pre loading of settings
    def __init__(self):
        print("Loading settings")
        self.display = Display()
        self.save = save()
        self.chk = Check()

        self.data = {
            "path": "Saves",
            "Timeout": 3,
        }
        self.defaultData = self.data.copy()

        # checks and makes file if doesn't exist.
        if not os.path.exists('Data/Settings'):
            print(f"{Fore.RED}DETECTED MISSING SETTINGS FILE!{Fore.RESET}")
            self.save.MakeFolders('Data')
            self.saveSettings()
        self.loadSettings()

        self.display.SetOptions(
            {
                -2: (self.deleteCache, "Delete Cache"),
                -1: (self.loadFromFile, "Load fron file"),
                0: (self.back, "Back"),
                1: (self.changeLocation,
                    f"Change Location (Current: {self.data.get('path')})"),
                2: (self.changeWait,
                    f"Timeout (Current: {self.data.get('Timeout')})"),
            }
        )

    def back(self, _):
        return "Returned"

    # Changes default location
    def changeLocation(self, _):
        check, path = self.chk.getInput(
            "Enter new save location (Leave blank to return): ",
            self.chk.ModeEnum.path, rCheck=True)
        if check is False:
            return

        self.display.RemoveOption(1)
        self.display.AddOption((self.changeLocation,
                                f"Change Location (Current: {path})"),
                               index=1)
        self.saveSettings("path", path)

    # Change the wait time between checks
    def changeWait(self, _):
        time = self.chk.getInput(
            "Please enter the wait time (leave blank to keep the same): ",
            self.chk.ModeEnum.int, lower=0, higher=20)

        self.display.RemoveOption(2)
        self.display.AddOption((self.changeLocation,
                                f"Change Timeout (Current: {time})"),
                               index=2)
        self.saveSettings("CheckTimeout", time)

    def deleteCache(self, _):
        print(f"{Fore.RED}Deleting Cache...{Fore.RESET}")
        Data = search().Locate(['*.pyc', '*_cache', '.Temp'], logging=True)
        print(f"Data found: {Data}")
        for file in Data:
            self.save.RemoveFile(file)

    # Loads settings stored
    def loadSettings(self):
        print(f"{Fore.BLUE}Loading settings...{Fore.RESET}")
        if not os.path.exists('Data/Settings'):
            return self.saveSettings()

        self.data = self.save.Read('Data/Settings',
                                   encoding=[self.save.encoding.JSON,
                                             self.save.encoding.BINARY])

        # checks for missing data in the dictonary of data
        missing = []
        for item in self.defaultData.keys():
            if item not in self.data.keys():
                missing.append(item)
                print(
                    f"{Fore.RED}Error Missing data found: {item}{Fore.RESET}")

        # if missing data, attempts to fix without causing issue
        if len(missing) >= 1:
            print(
                f"{Fore.YELLOW}Attempting to fix data{Fore.RESET}")
            for missed in range(len(missing), 0, -1):
                missed = missing[missed - 1]
                print(
                    f"{Fore.CYAN}Currently fixing {missed}{Fore.RESET}")
                self.data[missed] = self.defaultData[missed]
            print("Fixed settings, No data lost")
            self.saveSettings()

        print(
            f"{Fore.GREEN}Successfully loaded settings!{Fore.RESET}")

        return None

    # Saves settings
    def saveSettings(self, obj=None, data=None):
        if None not in (obj, data):
            self.data[obj] = data

        print(f"{Fore.BLUE}Saving Settings...{Fore.RESET}")
        self.save.Write(self.data, 'Data/Settings',
                        encoding=[self.save.encoding.JSON,
                                  self.save.encoding.BINARY])
        print(f"{Fore.GREEN}Saved Settings!{Fore.RESET}")

    def loadFromFile(self, _):
        file = self.chk.getInput(
            "Please enter location of file (leave blank to stop): ",
            self.chk.ModeEnum.path)
        if file is False:
            return

        self.data = self.save.Read(file, encoding=[self.save.encoding.JSON,
                                                   self.save.encoding.BINARY])
        self.saveSettings()

    # Shows the settings menu
    def showDisplay(self):
        result = None
        while result != "Returned":
            Message.clear()
            self.display.ShowHeader(text="Options")
            result = self.display.ShowOptions(useList=True)
