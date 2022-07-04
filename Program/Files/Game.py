import importlib
import getpass
import os
newSave = importlib.import_module('Files.newSave')
Functions = importlib.import_module('Files.Functions')
newPlace = importlib.import_module('Files.newPlace')
newFire = importlib.import_module('Files.newFire')


class Game:
    def __init__(self, data):
        self.name = data[0]
        self.users = data[1]
        self.placed = data[2]
        self.location = data[3]
        self.gamePath = os.path.join(self.location, self.name)
        self.multiplayer = data[4]
        self.gameData = newSave.save({
            'name': self.name,
            'path': self.location,
        })

        self.localUser = None
        self.localUserIndex = None

    def Place(self):
        if self.multiplayer[0] != 'y':
            # Go through each user and get them to place things
            for user in range(len(self.users)):
                if not self.placed[user]:
                    userPlace = newPlace.Place(self.name,
                                               [self.location,
                                                os.path.join(
                                                    self.name,
                                                    self.users[user]
                                                )],
                                               self.users[user])
                    self.placed[user] = userPlace.Main()
                    if self.placed[user] is False:
                        # person A quit, no need for person B to place.
                        return False

            return self.placed[0] and self.placed[1]

        # Checks if the local user has placed in this multiplayer game
        if not self.placed[self.localUserIndex]:
            userPlace = newPlace.Place(self.name,
                                       [self.location,
                                        os.path.join(
                                            self.name,
                                            self.users[self.localUserIndex]
                                        )],
                                       self.users[self.localUserIndex])
            return userPlace.Main()

        return True

    def PlaceCheck(self):
        placed = [False, False]
        for user in range(len(self.users)):
            folder = newSave.save({
                'path': os.path.join(self.gamePath, self.users[user])
            }).CheckForFile('shots')
            if folder:
                placed[user] = True
        return placed

    def Fire(self):
        # Easy call to fire system
        newFire.Fire([self.name,
                      self.location,
                      self.multiplayer],
                     self.users,
                     self.localUser).Fire()

    def Password(self):
        # Checks if there is a password stored and gets them to enter it.
        gameData = self.gameData.readFile('{}/GameData'.format(self.name))
        if gameData['password'] is not None:
            word = getpass.getpass("Please enter game password: ")
            if word == gameData['password']:
                return True
            return False
        return True

    def UsernameCheck(self):
        if self.multiplayer == 'y':
            # Gets the user username for the game
            users = self.gameData.ls(True, True)

            # Check to see if same to account name
            localUser = getpass.getuser()
            if localUser in users:
                return localUser, self.users.index(localUser)

            # Gets them to manualy enter it in.
            user = None
            while user is None:
                user = input("Please enter your username: ")
                if user in users:
                    return user
                Functions.clear(2, "User not found! (Spectating comming in Update 3)")  # noqa E501
                user = None
        return None, None

    def MultiPlaceCheck(self):
        # Multiplayer placement check
        if self.multiplayer == 'y':
            placed = False

            # Loop for checking placement
            while placed is False:
                placing = self.PlaceCheck()  # checks files
                opponenet = 0 if self.localUserIndex == 1 else 1

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
        self.localUser, self.localUserIndex = self.UsernameCheck()
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
