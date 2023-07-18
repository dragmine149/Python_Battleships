import getpass
import shutil
import string
import random
import re

from colorama import Fore
from PythonFunctions.PrintTraceback import PrintTraceback
from PythonFunctions.TerminalDisplay import Display
from PythonFunctions.Watermark import LINKCODE
from PythonFunctions.Check import Check
from PythonFunctions.Save import save
from PythonFunctions import Board, Message
from PythonFunctions.utils import cursor, SPACE, lenstr, n, clearLine
from Files import ShipInfo, CreateChecks


class CreateGame:
    def __init__(self, path: str = "Saves") -> None:
        self.info = {
            "Name": {"value": "None", "colour": Fore.RED},
            "Players": {
                "1": {"value": getpass.getuser(), "colour": Fore.GREEN},
                "2": {"value": "None", "colour": Fore.RED},
            },
            "Size": {
                "X": {"value": 10, "colour": Fore.GREEN},
                "Y": {"value": 10, "colour": Fore.GREEN},
            },
            "Location": {"value": path, "colour": Fore.GREEN},
            "Multiplayer": {"value": "no", "colour": Fore.GREEN},
            "Spectate": {"value": "no", "colour": Fore.GREEN},
            "Password": {"true": None, "value": "Disabled", "colour": Fore.YELLOW},
        }
        self.display = Display()
        self.cck = CreateChecks.GameChecks(path)
        self.__CreateArguments()
        self.display.SetQuitMessage("returning")

    def __getValue(self, field: str, *, sub: str = None, c: bool = False):
        Field = self.info.get(field)
        if sub:
            subField = Field.get(sub)
            subFieldData = str(subField.get("value"))
            if c:
                return subField.get("colour") + subFieldData + Fore.RESET
            return subFieldData

        if c:
            FieldData = str(Field.get("value"))
            return Field.get("colour") + FieldData + Fore.RESET
        return FieldData

    def ChangeValue(self, value):
        value = value[1]
        uI = None
        while uI is None:
            uI = input("Please enter a new value: ")
            nuI = self.cck.Translate(value, uI)
            if nuI == uI:
                self.info.get(value)["value"] = uI
                self.info.get(value)["colour"] = Fore.GREEN
                return

    def CreateGame(self):
        print("Creating Game!")

    def __CreateArguments(self):
        self.display.AddOption(
            self.ChangeValue,
            f"Game Name: {self.__getValue('Name', c=True)}",
            args="Name",
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Player 1: {self.__getValue('Players', sub='1', c=True)}",
            args="P1",
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Player 2: {self.__getValue('Players', sub='2', c=True)}",
            args="P2",
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Board X Length: {self.__getValue('Size', sub='X', c=True)}",
            args="SizeX",
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Board Y Length: {self.__getValue('Size', sub='Y', c=True)}",
            args="SizeY",
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Save Location: {self.__getValue('Location', c=True)}",
            args="Location",
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Multiplayer: {self.__getValue('Multiplayer', c=True)}",
            args="Multiplayer",
        )
        # self.display.AddOption(self.ChangeValue, "Spectate", args="Spectate")
        self.display.AddOption(
            self.ChangeValue,
            f"Password: {self.__getValue('Password', c=True)}",
            args="Password",
        )
        self.display.AddOption(self.CreateGame, "Save and Create Game")

    def Main(self):
        result = None
        while result is None:
            Message.clear()
            self.display.ShowHeader(
                text="""Change settings for a new game

Red = needs changing. Yellow = Ok, but not recommended, Green = Good."""
            )
            result = self.display.ShowOptions(quitIsBack=True)
            if result in ("saving", "returning"):
                return

            result = None
