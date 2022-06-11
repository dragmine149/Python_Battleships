import GameMenu
import Functions
from Functions import Print
import newSave
import json
import os


class Settings:

    # does some pre loading of settings
    def __init__(self):
        print("Loading settings")
        self.save = newSave.save({
            'name': 'Settings',
            'path': 'Data',
        })

        self.data = {
            "path": "Saves",
            "colour": "reset"
        }
        self.defaultData = self.data.copy()

        # checks and makes file if doesn't exist.
        if not self.save.CheckForFile('Settings'):
            self.saveSettings()
        self.loadSettings()

        self.unformatedOptions = """01: Deafult Location -> {}
02: Colour -> {}
03: Clear Cache"""

    def back(self):
        return "Returned"

    def updateDisplay(self):
        return self.unformatedOptions.format(self.data["path"],
                                             self.data["colour"])

    """
    updateSave(obj, data)
    obj -> name of object, e.g. path
    data -> data to save in that object
    """
    def updateSave(self, obj, data):
        self.data[obj] = data
        self.saveSettings()
        self.display.options = self.updateDisplay()

    # Changes default location
    def changeLocation(self):
        data = Functions.changePath()
        self.updateSave("path", data[1])

    # Changes player colour
    def changeColour(self):
        colour = None
        while colour is None:
            # gets input
            colour = input("What colours would you like to be? (leave empty to go back): ")  # noqa E501
            if colour == "":
                return

            # get possible list
            try:
                code = Functions.colourRetrieve(colour)
                colour = code.fullName
            except ValueError:
                Print("Invalid colour chosen!", "red")
                colour = None

        # save
        self.updateSave("colour", colour)
    
    def deleteCache(self):
        Print("Deleting cache...", "Red")
        localDirList = os.listdir('.')
        for file in localDirList:
            if file == "__pycache__":
                print(file)
                newSave.save({
                    'name': '',
                    'path': 'Saves'
                }).Delete(os.path.join(".", file))
        Functions.warn(2, "Waiting...", "green")

    # Loads settings stored
    def loadSettings(self):
        Print("Loading settings... ", 'blue')
        self.data = json.loads(self.save.readFile())

        # checks for missing data in the dictonary of data
        missing = []
        for item in self.defaultData.keys():
            if item not in self.data.keys():
                missing.append(item)
                Print("Error Missing data found: {}".format(item), "red")

        # if missing data, attempts to fix without causing issue
        if len(missing) >= 1:
            Print("Attempting to fix data", "orange")
            for missed in range(len(missing), 0, -1):
                missed = missing[missed - 1]
                Print("Currently fixing: {}".format(missed), "cyan")
                self.data[missed] = self.defaultData[missed]
            Print("Fixed settings, No data lost")
            self.saveSettings()

        Print("Successfully loaded settings", 'green')

    # Saves settings
    def saveSettings(self):
        Print("Saving settings...", 'blue')
        self.save.writeFile(json.dumps(self.data))
        Print("Successfully saved settings", "green")

    # Shows the settings menu
    def showDisplay(self):
        info = """\033[32m--------------------------------------------------------------------
Your personal settings.
--------------------------------------------------------------------
\033[0m"""
        options = self.updateDisplay()
        choices = {
            0: self.back,
            1: self.changeLocation,
            2: self.changeColour,
            3: self.deleteCache
        }
        self.display = GameMenu.menu(info,
                                     options,
                                     choices,
                                     back="Return to main menu")
        result = self.display.getInput(values=(0, 3))
        if result == "Returned":
            return "back"
        return result


# Takes the input data and returns the output
# useful for quick access to settings
def request(data):
    setObj = Settings()
    # no need to load again as automatically done in class call.
    return setObj.data[data]
