import sys
import Functions
import Loader
import ProcessInput as pi
import Settings


# Main menu choices, not a lot.
class Choices:
    def __init__(self):
        self.Loader = Loader.Loader()
        self.Process = pi.Process()
        self.path = self.Loader.path

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
        print(result)
        return result

    def makeGame(self):
        self.path = self.Loader.path
        return self.Process.Inputs(self.path, create=True)

    def settings(self):
        Settings.Settings().showDisplay()
        return "Comming soon..."
