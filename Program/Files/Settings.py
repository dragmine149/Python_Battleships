import os
import importlib

GameMenu = importlib.import_module('Files.GameMenu')
Functions = importlib.import_module('Files.Functions')
colours = importlib.import_module('Files.colours')
newSave = importlib.import_module('Files.newSave')
Setup = importlib.import_module('Files.Setup')

Print = colours.Print
colourRetrieve = colours.colourRetrieve
c = colours.c


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
            "colour": "yellow",
            "clear": True
        }
        self.defaultData = self.data.copy()

        # checks and makes file if doesn't exist.
        if not self.save.CheckForFile('Settings'):
            self.saveSettings()
        self.loadSettings()

        self.unformatedOptions = """01: Deafult Location (game saves) -> {}
02: Colour -> {}{}{}
03: Console Clear -> {}
04: Clear Cache
05: Setup (Install optional modules)"""
        self.choices = {
            0: self.back,
            1: self.changeLocation,
            2: self.changeColour,
            3: self.changeClear,
            4: self.deleteCache,
            5: self.setup,
        }

    def back(self):
        return "Returned"

    def updateDisplay(self):
        return self.unformatedOptions.format(self.data["path"],
                                             c(self.data["colour"]),
                                             self.data["colour"],
                                             c(),
                                             self.data["clear"])

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
            colour = input("What colour would you like to be? (leave empty to keep the same): ")  # noqa E501
            if colour == "":
                return

            # get possible list
            try:
                code = colourRetrieve(colour)
                colour = code.fullName
                Print(f"Colour chosen: {colour}", "cyan")
            except ValueError:
                Print("Invalid colour chosen!", "red")
                colour = None

        # save
        self.updateSave("colour", colour)
    
    # Changes how the terminal gets cleared
    def changeClear(self):
        self.updateSave("clear", not self.data['clear'])

    def deleteCache(self):
        Print("Deleting cache...", "Red")

        Data = Functions.search('..', ('*.pyc', '*_cache', '.Temp'), 2, 0).Locate()  # noqa E501
        print("Data Found: {}".format(Data))
        for file in Data:
            Print(f"Deleting: {file}", "orange")
            newSave.save.delete(file)

        Functions.warn(1, "Waiting...", "green")

    def setup(self):
        path, changed = Setup.env()
        Functions.clear(1)
        _, changed1 = Setup.uiCheck(path)
        Functions.clear(1)
        _, changed2 = Setup.google(path)
        Functions.clear(1)
        if changed or changed1 or changed2:
            os.sys.exit("Please run `{} mainTemp.py` to use new modules.".format(path))  # noqa E501

    # Loads settings stored
    def loadSettings(self):
        Print("Loading settings... ", 'blue')
        self.data = self.save.readFile()

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
        self.save.writeFile(self.data, True)
        Print("Successfully saved settings", "green")

    def loadFromFile(self):
        file = False
        while file is False:
            file = input("Please enter location of file (-1 to stop): ")

            if file == -1:
                return

            if os.path.exists(file):
                try:
                    pathData = newSave.save({
                        'path': file
                    })
                    data = pathData.readFile(nameAllowed=False)
                    print({'path': data["path"]})
                    print({'colour': data["colour"]})

                    # TODO: add way to keep old settings in case they want them
                    os.system('mv {} Data/Settings'.format(file))

                except Exception as e:
                    print("{} occured!".format(e))
                    file = False
                    Functions.clear(2)

    # Shows the settings menu
    def showDisplay(self):
        dashText = '-' * os.get_terminal_size().columns
        info = """\033[32m{}
Your personal settings.
{}
\033[0m""".format(dashText, dashText)
        options = self.updateDisplay()
        external = {
            -1: 'Load settings from file'
        }
        self.display = GameMenu.menu(info,
                                     options,
                                     self.choices,
                                     external,
                                     "Return to main menu")
        result = self.display.getInput(values=(-1, len(self.choices) -1))
        if result == "Returned":
            return "back"
        return result


# Takes the input data and returns the output
# useful for quick access to settings
def request(data):
    setObj = Settings()
    # no need to load again as automatically done in class call.
    try:
        return setObj.data[data]
    except KeyError:
        return None
