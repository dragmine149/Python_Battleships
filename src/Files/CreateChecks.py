import getpass
import string
import re
import random

from PythonFunctions.CleanFolderData import Clean
from PythonFunctions.utils import n
from PythonFunctions.Save import save


class GameChecks:
    def __init__(self, Location) -> None:
        self.cln = Clean()
        self.Location = Location
        self.sv = save()

    def __Forbidden(self, value: str) -> bool:
        return re.search(r'[\\/:*?"<>|]', value)

    def __getGameList(self, Location):
        return self.cln.clean(self.sv.ListFolder(Location))

    def name(self, value: str = None):
        # Invalid Character Check
        if self.__Forbidden(value):
            return "Invalid Characters!"

        if value not in self.__getGameList(self.Location):
            return value

        randomEnd = ""
        for _ in range(10):
            randomEnd += random.choice(string.ascii_letters)

        return "Exists", f"{value}_{randomEnd}"

    def username(self, value, index, *, pre=None):
        end = ""
        if index == 1:
            end += "(2)"

        if self.__Forbidden(value):
            return "Invalid Characters!"

        if value == "me":
            return getpass.getuser() + end

        if index == 1 and pre == value:
            return pre + end

    def sizeX(self, value):
        if value > 5:
            return n(value, value, str(value))
        return "Low"

    def sizeY(self, value):
        if value > 5:
            return n(value, value, str(value))
        return "Low"

    def save(self, value):
        if value == "~/r!":
            return None

        try:
            self.sv.Write("test", f"{value}/Battleship.test")
            self.sv.RemoveFile(f"{value}/Battleship.test")
        except (FileNotFoundError, OSError):
            return "No permission to write"

        self.Location = value
        return value

    def multiplayer(self, value):
        if self.Location == "Saves":
            return False

        return n(value, "yes", v2="no")

    def Spectate(self, value):
        return n(value, "yes", "no")

    def Password(self, value):
        if self.__Forbidden(value):
            return "Forbidden Characters"

        if value.rstrip() == "":
            return None

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
                return None

    def Translate(self, option, value, *, userIndex=None, PreviousUser=None):
        match option:
            case "Name":
                return self.name(value)
            case "Players":
                return self.username(value, index=userIndex, pre=PreviousUser)
            case "SizeX":
                return self.sizeX(value)
            case "SizeY":
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
