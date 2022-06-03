import GameMenu
import Functions
from Functions import Print
import newSave


class Settings:
    def __init__(self):
        print("Loading settings")
    
    def back(self):
        return "Returned"

    def changeLocation(self, args):
        print(args)
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
            0: self.back,
            1: self.changeLocation
        }
        self.display = GameMenu.menu(info,
                                     options,
                                     choices,
                                     back="Return to main menu")
        result = self.display.getInput(-0.5, (0, 1))
        return result
