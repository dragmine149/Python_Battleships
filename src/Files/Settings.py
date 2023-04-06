import os
import importlib
import getpass
import colorama
from PythonFunctions.Save import save
from PythonFunctions.TerminalDisplay import Display
from PythonFunctions.Check import Check
from PythonFunctions.Searching import search

GameMenu = importlib.import_module('Files.GameMenu')


class Settings:

    # does some pre loading of settings
    def __init__(self):
        print("Loading settings")
        self.display = Display()
        self.save = save()
        self.chk = Check()

        self.data = {
            "path": "Saves",
            "clear": True,
            "loadTimes": False,
            "CheckTimeout": 3,
        }
        self.defaultData = self.data.copy()

        # checks and makes file if doesn't exist.
        if not os.path.exists('Data/Settings'):
            self.saveSettings()
        self.loadSettings()

        self.display.SetOptions(
            {
                -2: (self.deleteCache, "Delete Cache"),
                -1: (self.loadFromFile, "Load fron file"),
                0: (self.back, "Back"),
                1: (self.changeLocation, "Change Location"),
                2: (self.changeClear, "Change Console Clear"),
                3: (self.changeLoad, "Change Load"),
                4: (self.changeWait, "Check Timeout"),
            }
        )

    def back(self):
        return "Returned"

    """
    updateSave(obj, data)
    obj -> name of object, e.g. path
    data -> data to save in that object
    """

    def updateSave(self, obj, data):
        self.data[obj] = data
        self.saveSettings()
        if self.display is not None:
            self.display.options = self.updateDisplay()

    # Changes default location
    def changeLocation(self):
        path = self.chk.getInput(
            "Enter new save location (Leave blank to return): ",
            self.chk.ModeEnum.path)
        if path is False:
            return

        self.updateSave("path", path)

    # Changes how the terminal gets cleared
    def changeClear(self):
        self.updateSave("clear", not self.data['clear'])

    # Change whever to show the load time
    def changeLoad(self):
        self.updateSave("loadTimes", not self.data['loadTimes'])

    # Change the wait time between checks
    def changeWait(self):
        time = self.chk.getInput(
            "Please enter the wait time (leave blank to keep the same): ",
            self.chk.ModeEnum.int, lower=0, higher=20)

        self.updateSave("CheckTimeout", time)

    def deleteCache(self):
        print(f"{colorama.Fore.RED}Deleting Cache...{colorama.Fore.RESET}")
        Data = search().Locate(['*.pyc', '*_cache', '.Temp'], directory='..')
        print("Data Found: {}".format(Data))
        for file in Data:
            self.save.RemoveFile(file)

    # Loads settings stored
    def loadSettings(self):
        print(f"{colorama.Fore.BLUE}Loading settings...{colorama.Fore.RESET}")
        self.data = self.save.Read('Data/Settings',
                                   encoding=[self.save.encoding.BINARY])

        # checks for missing data in the dictonary of data
        missing = []
        for item in self.defaultData.keys():
            if item not in self.data.keys():
                missing.append(item)
                print(
                    f"{colorama.Fore.RED}Error Missing data found: {item}{colorama.Fore.RESET}")

        # if missing data, attempts to fix without causing issue
        if len(missing) >= 1:
            print(
                f"{colorama.Fore.YELLOW}Attempting to fix data{colorama.Fore.RESET}")
            for missed in range(len(missing), 0, -1):
                missed = missing[missed - 1]
                print(
                    f"{colorama.Fore.CYAN}Currently fixing {missed}{colorama.Fore.RESET}")
                self.data[missed] = self.defaultData[missed]
            print("Fixed settings, No data lost")
            self.saveSettings()

        print(
            f"{colorama.Fore.GREEN}Successfully loaded settings!{colorama.Fore.RESET}")

    # Saves settings
    def saveSettings(self):
        print(f"{colorama.Fore.BLUE}Saving Settings...{colorama.Fore.RESET}")
        self.save.Write(self.data, 'Data/Settings.json',
                        encoding=[self.save.encoding.JSON,
                                  self.save.encoding.BINARY])
        print(f"{colorama.Fore.GREEN}Saved Settings!{colorama.Fore.RESET}")

    def loadFromFile(self):
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
        self.display.ShowHeader(text="Options")
        self.display.ShowOptions(useList=True)


# Takes the input data and returns the output
# useful for quick access to settings
def request(data=[]):
    setObj = Settings()
    # no need to load again as automatically done in class call.
    result = []
    for item in data:
        try:
            result.append(setObj.data[item])
        except KeyError:
            result.append(None)
    return result
