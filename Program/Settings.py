import GameMenu
import Functions
from Functions import Print
import newSave


class Settings:
    def __init__(self):
        print("Loading settings")

    def changeLocation(self):
        print("Changing location")

    def showDisplay(self):
        info = """--------------------------------------------------------------------
    Your personall settings.
    --------------------------------------------------------------------
    """
        options = """01: Deafult Location ->
        02: WIP
        """
        choices = {
            1: self.showDisplay
        }
        self.display = GameMenu.menu(info,
                                     options,
                                     choices,
                                     back="Return to main menu")
        self.display.getInput(.5, (0, 1))
