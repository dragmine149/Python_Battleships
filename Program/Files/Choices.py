import importlib
import sys
Functions = importlib.import_module('Files.Functions')
Loader = importlib.import_module('Files.Loader')
pi = importlib.import_module('Files.ProcessInput')
Settings = importlib.import_module('Files.Settings')


# Main menu choices, not a lot.
class Choices:
    def __init__(self):
        self.Loader = Loader.Loader()
        self.path = self.Loader.path
        self.Settings = Settings.Settings()
        self.Process = pi.Process(self.path)

    # doesn't really generate, hard coded list
    def generate(self, mode="main"):
        if mode == "main":
            return {
                0: self.quit,
                1: self.selectGame,
                2: self.makeGame,
                3: self.settings
            }
        sys.exit("Error")

    def quit(self):
        sys.exit("Thank you for playing")

    def selectGame(self):
        Functions.clear()
        self.Loader.game = None
        result = self.Loader.selectGame()
        return result

    def makeGame(self):
        self.path = self.Loader.path
        return self.Process.Inputs(create=True)

    def settings(self):
        result = self.Settings.showDisplay()
        return result
