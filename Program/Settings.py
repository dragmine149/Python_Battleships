import GameMenu
import Functions
from Functions import Print
import newSave
import json


class Settings:

    # does some pre loading of settings
    def __init__(self):
        print("Loading settings")
        self.save = newSave.save({
            'name': 'Settings',
            'path': 'Data',
        })

        # checks and makes file if doesn't exist.
        if not self.save.CheckForFile('Settings'):
            self.data = {
                "path": "Saves",
            }
            self.saveSettings()
        self.loadSettings()

        self.unformatedOptions = """01: Deafult Location -> {}"""

    def back(self):
        return "Returned"

    # Changes default location
    def changeLocation(self):
        data = Functions.changePath()
        self.data["path"] = data[1]
        print(self.data)
        self.saveSettings()
        self.display.options = self.unformatedOptions.format(self.data["path"])

    # Loads settings stored
    def loadSettings(self):
        Print("Loading settings... ", 'blue')
        self.data = json.loads(self.save.readFile())
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
        options = self.unformatedOptions.format(self.data["path"])
        choices = {
            0: self.back,
            1: self.changeLocation
        }
        self.display = GameMenu.menu(info,
                                     options,
                                     choices,
                                     back="Return to main menu")
        result = self.display.getInput(values=(0, 1))
        if result == "Returned":
            return "back"
        return result


# Takes the input data and returns the output
# useful for quick access to settings
def request(data):
    setObj = Settings()
    setObj.loadSettings()
    return setObj.data[data]
