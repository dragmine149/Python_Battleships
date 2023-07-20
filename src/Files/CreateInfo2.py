import getpass
import shutil
import string
import random
import re

from colorama import Fore
from PythonFunctions.CleanFolderData import Clean
from PythonFunctions.PrintTraceback import PrintTraceback
from PythonFunctions.TerminalDisplay import Display
from PythonFunctions.Watermark import LINKCODE
from PythonFunctions.Check import Check
from PythonFunctions.Save import save
from PythonFunctions import Board, Message
from PythonFunctions.utils import cursor, SPACE, lenstr, n, clearLine, passOrInput
from Files import ShipInfo, CreateChecks


class CreateGame:
    def __init__(self, path: str = "Saves") -> None:
        self.info = {
            "Name": {"value": "None", "colour": Fore.RED},
            "Players": {
                "P1": {"value": getpass.getuser(), "colour": Fore.GREEN},
                "P2": {"value": "None", "colour": Fore.RED},
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
        self.cck = CreateChecks.GameChecks(path, getpass.getuser())
        self.__CreateArguments()
        self.display.SetQuitMessage("returning")
        self.chk = Check()
        self.currentPos: list[int] = [0, 0]

    def __getValue(self, field: str, *, sub: str = None, c: bool = False):
        Field = self.info.get(field)
        if sub:
            subField = Field.get(sub)
            subFieldData = str(subField.get("value"))
            if c:
                return subField.get("colour") + subFieldData + Fore.RESET
            return subFieldData

        FieldData = str(Field.get("value"))
        if c:
            return Field.get("colour") + FieldData + Fore.RESET
        return FieldData

    def SetValue(self, sub, value, new):
        if sub:
            self.info.get(sub).get(value)["value"] = new
            self.info.get(sub).get(value)["colour"] = Fore.GREEN
            return

        self.info.get(value)["value"] = new
        self.info.get(value)["colour"] = Fore.GREEN
        return

    def set(self, sub, value, uI):
        self.SetValue(sub, value, uI)

        self.currentPos = self.display.GetCursorPosition()
        self.display.RemoveAllOptions()
        self.__CreateArguments()

    def ChangeValue(self, value, default=None):
        sub = None

        value = value[1]
        if len(value) == 2:
            sub = value[1]
            value = value[0]

        uI = None
        while uI is None:
            uI = default
            if default is None:
                uI = passOrInput(
                    f"Please enter a new value for {value}: ", value == "Password"
                )
            nuI = self.cck.Translate(value, uI)

            default = None

            if value == "Password":
                self.info.get("Password")["real"] = nuI
                self.info.get("Password")["value"] = "Enabled"
                self.info.get("Password")["colour"] = Fore.GREEN
                self.display.RemoveAllOptions()
                self.__CreateArguments()
                return

            if value == "Location":
                self.info.get("Name")["colour"] = Fore.YELLOW

            if nuI == uI:
                return self.set(sub, value, uI)

            if nuI == "Invalid Characters":
                print("Invalid characters in name. Please choose a new name.")
                uI = None
                continue

            if nuI == "NAN":
                print("Number inputted is not a number. Please enter a number")
                uI = None
                continue

            if nuI == "Low":
                print("Number inputted is too low. Please enter a higher number")
                uI = None
                continue

            if nuI == "Return":
                return

            if nuI == "NPTW":
                print(
                    "The save location does not grant the program permission to write."
                    " Please make sure this program has permission and/or that path"
                    " exists."
                )
                uI = None
                continue

            if nuI == "DSL":
                print(
                    "Default Save Location is active. Online multiplayer can not be"
                    " enabled"
                )
                uI = None
                continue

            if nuI == "Empty Password":
                print("You entered no password. Please enter a password")
                uI = None
                continue

            if nuI == "Retry":
                uI = None
                continue

            if value == "Multiplayer":
                return self.set(sub, value, "yes" if nuI is True else "no")

            if value in ("X", "Y"):
                return self.set(sub, value, uI)

            resuslt = self.chk.getInput(
                (
                    f"The system has determind that there is a better value. ({nuI})"
                    " Accept? (y or n): "
                ),
                self.chk.ModeEnum.yesno,
            )

            if resuslt:
                return self.set(sub, value, nuI)

    def __check(self, users):
        # Checks if all fields are valid.

        if self.__getValue("Name") == "None":
            Message.warn("Please enter a name")
            return "Name"

        if self.__getValue("Name") in Clean().clean(
            save().ListFolder(self.__getValue("Location"))
        ):
            Message.warn("Game name already exists. Please choose a new name!")
            return "Name2"

        if any(user == "None" for user in users):
            Message.warn("Please check players name. (Someone has 'None')")
            return "Username"

        if any(("/" in user or "\\" in user for user in users)):
            Message.clear("Usernames cannot have '/' or '\\' in!", timeS=2)
            return "Invalid Name"

        # Password better than no password, Check
        if self.info.get("Password").get("real") is None:
            continueChoice = self.chk.getInput(
                "No password has been set, Continue?: ",
                self.chk.ModeEnum.yesno,
                y=None,
                n="password",
            )
            if continueChoice is not None:
                return continueChoice

        return True

    def CreateGame(self):
        users = [
            self.__getValue("Players", sub="P2"),
            self.__getValue("Players", sub="P2"),
        ]

        chkResult = self.__check(users)
        if chkResult is not True:
            Message.clear(f"Please check settings. Reason: {chkResult}", timeS=2)
            return False

        password = self.info.get("Password").get("real")
        if password is not None:
            check = getpass.getpass("Please enter the password to create the game: ")
            if check != password:
                Message.clear("Please try again or change the password!", timeS=2)
                return False

        size = [
            self.__getValue("Size", sub="X"),
            self.__getValue("Size", sub="Y"),
        ]

        brd = Board.CreateBoard(int(size[0]), int(size[1]))
        saveLocation = self.__getValue("Location")
        name = self.__getValue("Name")
        gameLocation = f"{saveLocation}/{name}"

        sv = save()

        sv.MakeFolders(gameLocation)

        placed = ShipInfo.getDefaultPlaced()
        for user in users:
            userLocation = f"{gameLocation}/{user}"
            sv.MakeFolders(userLocation)
            sv.Write(brd, f"{userLocation}/ships", encoding=sv.encoding.BINARY)
            sv.Write(placed, f"{userLocation}/placedData", encoding=sv.encoding.BINARY)

        turn = random.randrange(2) + 1
        data = {
            "turn": self.__getValue("Players", sub=f"P{turn}"),
            "multi": self.__getValue("Multiplayer"),
            "password": "",
            "size": size,
            "users": users,
            "spectate": self.__getValue("Spectate"),
        }
        sv.Write(data, f"{gameLocation}/GameData", encoding=sv.encoding.BINARY)
        return "Saving"

    def __CreateArguments(self):
        self.display.AddOption(
            self.ChangeValue,
            f"Game Name: {self.__getValue('Name', c=True)}",
            args="Name",
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Player 1: {self.__getValue('Players', sub='P1', c=True)}",
            args=("P1", "Players"),
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Player 2: {self.__getValue('Players', sub='P2', c=True)}",
            args=("P2", "Players"),
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Board X Length: {self.__getValue('Size', sub='X', c=True)}",
            args=("X", "Size"),
        )
        self.display.AddOption(
            self.ChangeValue,
            f"Board Y Length: {self.__getValue('Size', sub='Y', c=True)}",
            args=("Y", "Size"),
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
            result = self.display.ShowOptions(
                quitIsBack=True, cursorPosition=self.currentPos
            )
            if result in ("Saving", "returning"):
                return

            result = None

    def SetDefaults(self, name, users, sizeX, sizeY, Multi, Spec):
        Message.clear()
        if name is not None:
            self.ChangeValue((None, "Name"), name)

        if users is not None:
            if len(users) == 2:
                self.ChangeValue((None, ("P1", "Players")), users[0])
                self.ChangeValue((None, ("P2", "Players")), users[1])

        if sizeX is not None:
            self.ChangeValue((None, ("X", "Size")), str(sizeX))

        if sizeY is not None:
            self.ChangeValue((None, ("Y", "Size")), str(sizeY))

        self.ChangeValue((None, "Multiplayer"), Multi)
        self.ChangeValue((None, "Spectate"), Spec)
