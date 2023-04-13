import getpass
import typing

from PythonFunctions.Save import save
from PythonFunctions.Message import Message
from PythonFunctions.CleanFolderData import Clean
from PythonFunctions.Check import Check
from PythonFunctions.Logic import MultiCheck

from Files import newFire, newPlace


class Game:
    def __init__(self, gamePath: str, gameName: str):
        print("Game.py loading!")
        self.save = save()
        self.msg = Message()
        self.cln = Clean()
        self.chk = Check()

        self.name = gameName
        self.gamePath = f'{gamePath}/{gameName}'
        self.gameData = self.save.Read(f'{self.gamePath}/GameData',
                                       encoding=self.save.encoding.BINARY)
        self.localUser = {}

        self.GetGameInfo()

    def GetGameInfo(self):
        self.users = self.cln.clean(self.save.ListFolder(self.gamePath),
                                    'GameData')
        self.multiplayer = self.gameData.get('multi')

    def Place(self):
        print("Placement check")
        placed = self.__checkShipPlacement(self.users)
        if MultiCheck(*placed):
            return True

        if self.multiplayer[0] != 'y':
            # Go through each user and get them to place things
            for user in range(len(self.users)):
                if not placed[user]:
                    userPlace = newPlace.Place(self.gamePath,
                                               self.users[user])
                    placed[user] = userPlace.Main()
                    if placed[user] is False:
                        # person A quit, no need for person B to place.
                        return False

            print("Finished placement")
            return MultiCheck(*self.placed)

        # Checks if the local user has placed in this multiplayer game
        if not self.placed[self.localUserIndex]:
            userPlace = newPlace.Place(self.gamePath,
                                       self.localUser.get('name'))
            return userPlace.Main()

        return True

    def __checkShipPlacement(self, users: typing.List):
        user1Placed = self.save.Read(f'{self.gamePath}/{users[0]}/shots')
        user2Placed = self.save.Read(f'{self.gamePath}/{users[1]}/shots')
        return [user1Placed, user2Placed]

    def Fire(self):
        print("Time to fire!")
        # Easy call to fire system
        newFire.Fire([self.name,
                      self.location,
                      self.multiplayer],
                     self.users,
                     self.localUser).Fire()

    def Password(self):
        # Checks if there is a password stored and gets them to enter it.
        password = self.gameData.get('password')
        if password != 'Disabled':
            word = getpass.getpass("Please enter game password: ")
            return word == password
        return True

    def UsernameCheck(self):
        if self.multiplayer == 'yes':
            # Check to see if same to account name
            localUser = getpass.getuser()
            if localUser in self.users:
                return {
                    'name': localUser,
                    'index': self.users.index(localUser)
                }

            user = None
            while user is None:
                found, user = self.chk.getInput("Please enter you username: ",
                                                self.chk.ModeEnum.str,
                                                rCheck=True,
                                                info=self.users)

                if not found:
                    self.msg.clear(
                        "User not found! (Spectating comming in Update 3)",
                        timeS=2)
                    user = None

            return {
                'name': user,
                'index': self.users.index(localUser)
            }
        return None

    def MultiPlaceCheck(self):
        # Multiplayer placement check
        if self.multiplayer == 'y':
            placed = False

            opponenet = 0 if self.localUserIndex == 1 else 1
            # Loop for checking placement
            while placed is False:
                placing = self.PlaceCheck()  # checks files

                # Waiting simulator if waiting on opponenet.
                if not placing[opponenet]:
                    msg = "Waiting for '{}' to place".format(
                        self.users[opponenet])
                    result = Functions.waiting(msg)
                    if result == "Back":
                        return "Ended whilst waiting for opponent to palce"
                    continue
                placed = True

            return True

    def Main(self):
        # Main loop
        self.localUser = self.UsernameCheck()
        if self.Password():
            result = self.Place()

            if result is False:
                return "Ended during placement."

            multiCheckResult = self.MultiPlaceCheck()
            # Checks and checks
            if multiCheckResult is not None:
                if multiCheckResult is not True:
                    return multiCheckResult

            if result:
                return self.Fire()
            return "Ended during placement."
        return "Incorrect password entered!"
