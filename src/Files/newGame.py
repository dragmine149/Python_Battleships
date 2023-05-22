import getpass
import typing

from secrets import compare_digest
from PythonFunctions import Message
from PythonFunctions.Save import save
from PythonFunctions.CleanFolderData import Clean
from PythonFunctions.Check import Check
from PythonFunctions.Logic import MultiCheck

from Files import Place, newFire, Spectate


class GameLoader:
    def __init__(self, gameInfo: dict) -> None:
        self.gamePath = gameInfo.get("path")
        self.gameName = gameInfo.get("name")

        self.sv = save()

        self.gameData = self.sv.Read(
            f"{self.gamePath}/{self.gameName}/GameData",
            encoding=self.sv.encoding.BINARY,
        )
        self.users = self.gameData.get("users")
        self.chk = Check()

    def GetUser(self):
        Message.clear()
        print("Attempting to get user by account name")
        user = getpass.getuser()
        result = self.chk.getInput(f"Are you {user}?: ", self.chk.ModeEnum.yesno)

        if result:
            return user

        result, user = self.chk.getInput(
            "Please enter your username: ",
            self.chk.ModeEnum.str,
            info=self.users,
            rCheck=True,
        )

        if result:
            return user

        print("User not detected in game database!")
        print("Spectating coming in update 3")
        return False

    def Password(self):
        password = self.gameData.get("password")
        if password is None:
            return True

        if compare_digest(password, "Disabled"):
            return True

        wordInput = getpass.getpass()
        return compare_digest(password, wordInput)

    def ShipPlacement(self):
        print("Shipment")
        print(self.gamePath, self.gameName)
        u1P = self.sv.CheckIfExists(
            f"{self.gamePath}/{self.gameName}/{self.users[0]}/shots"
        )
        u2P = self.sv.CheckIfExists(
            f"{self.gamePath}/{self.gameName}/{self.users[1]}/shots"
        )

        return [u1P, u2P]

    def PlaceShips(self):
        placement = self.ShipPlacement()

        print("PLACE")
        print(placement)
        print(MultiCheck(placement))

        if MultiCheck(placement):
            # Skip each individual placement stuff
            return True

        if not placement[0]:
            Place.Place(f"{self.gamePath}/{self.gameName}", self.users[0]).Main()
        if not placement[1]:
            Place.Place(f"{self.gamePath}/{self.gameName}", self.users[1]).Main()

        return self.ShipPlacement()

    def Fire(self):
        pass

    def main(self):
        _ = self.GetUser()
        print("Loaded user")
        if self.Password():
            print("Passed Password")
            if self.PlaceShips():
                print("Passed Placement")
                return self.Fire()

            return "Ended during placement"

        return "Invalid password"
