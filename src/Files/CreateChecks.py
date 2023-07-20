import getpass
import string
import re
import random

from PythonFunctions.CleanFolderData import Clean
from PythonFunctions.utils import n
from PythonFunctions.Save import save
from PythonFunctions.IsDigit import IsDigit
from PythonFunctions.Check import Check


class GameChecks:
    def __init__(self, Location, p1) -> None:
        self.cln = Clean()
        self.Location = Location
        self.p1 = p1
        self.sv = save()
        self.chk = Check()

    def __Forbidden(self, value: str) -> bool:
        # blank check
        if value == "":
            return True

        # actuall forbidden check
        return re.search(r'[\\/:*?"<>|]', value)

    def __getGameList(self, Location):
        return self.cln.clean(self.sv.ListFolder(Location))

    def name(self, value: str = None):
        # Invalid Character Check
        if self.__Forbidden(value):
            return "Invalid Characters"

        if value not in self.__getGameList(self.Location):
            return value

        randomEnd = ""
        for _ in range(10):
            randomEnd += random.choice(string.ascii_letters)

        return f"{value}_{randomEnd}"

    def P1(self, value: str):
        if self.__Forbidden(value):
            return "Invalid Characters"

        if value.lower() == "me":
            self.p1 = getpass.getuser()
            return getpass.getuser()

        self.p1 = value
        return value

    def P2(self, value):
        end = "(2)"

        if self.__Forbidden(value):
            return "Invalid Characters"

        if value.lower() == "me":
            value = getpass.getuser()

        if value == self.p1:
            return value + " " + end

        return value

    def sizeX(self, value):
        if not IsDigit(value):
            return "NAN"

        value = int(value)
        if value >= 5:
            return n(value, value, str(value))

        return "Low"

    def sizeY(self, value):
        if not IsDigit(value):
            return "NAN"

        value = int(value)
        if value >= 5:
            return n(value, value, str(value))

        return "Low"

    def save(self, value):
        if value == "~/r!":
            return "Return"

        try:
            self.sv.Write("test", f"{value}/Battleship.test")
            self.sv.RemoveFile(f"{value}/Battleship.test")
        except (FileNotFoundError, OSError):
            return "NPTW"

        self.Location = value
        return value

    def multiplayer(self, value):
        if value is False:
            return False

        if self.Location == "Saves":
            return "DSL"

        if value == "True":
            return True

        return self.chk.getInput("", self.chk.ModeEnum.yesno, vCheck=value)

    def Spectate(self, value):
        return n(value, "yes", "no")

    def Password(self, value):
        if self.__Forbidden(value):
            return "Forbidden Characters"

        if value.rstrip() == "":
            return "Empty Password"

        check = None
        while check is None:
            try:
                check = getpass.getpass(
                    "Please re-enter the password (ctrl/cmd + c to go back): "
                )
                if check == value:
                    return value
                check = None
            except KeyboardInterrupt:
                return "Retry"

        return "Retry"

    def Translate(self, option, value, *, userIndex=None, PreviousUser=None):
        match option:
            case "Name":
                return self.name(value)
            case "P1":
                return self.P1(value)
            case "P2":
                return self.P2(value)
            case "X":
                return self.sizeX(value)
            case "Y":
                return self.sizeY(value)
            case "Location":
                return self.save(value)
            case "Multiplayer":
                return self.multiplayer(value)
            case "Spectate":
                return self.Spectate(value)
            case "Password":
                return self.Password(value)

        raise ValueError(f"Invalid option: {option}")
