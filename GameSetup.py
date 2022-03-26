import os
import sys
import time
import SaveSystem as save
import Functions
import boardCreate as Create
import platform


class game:
    def __init__(self):
        self.choice = None
        self.name = None
        self.users = None
        self.Placed = None

    # Resets the game class for a new use
    def __reset(self, message=None, choice=None, name=None, users=None, Placed=None, Location=None, Multi=None):  # noqa
        self.name = name
        self.users = users
        self.Placed = Placed
        self.choice = choice
        self.saveLocation = Location
        self.twoPlayer = Multi
        if message:
            print(message)

    # Prints off all games found
    def _loadGames(self, external="saves"):
        print("Games found on disk:")
        if external == "saves":
            print("0: Load from external area")
        games = os.listdir(external)
        for file in games:
            """
            Files that get removed:
            - '.' files
            - '__' files
            """
            if file.startswith(".") or file.startswith('__'):
                games.pop(games.index(file))

        for file in range(len(games)):
            path = "{}: {}".format(file + 1, games[file])
            if os.path.exists("{}/{}/win".format(external, games[file])):
                path += " (finished)"
            print(path)
        return games

    # The range check function for amount of saves
    def _LoadRangeCheck(self, value, path="Saves"):
        amount = len(os.listdir(path))
        if value >= 0 and value <= amount:
            return True
        elif value == -1:
            return True
        return False

    def _LoadGame(self, gamesDir, Path="Saves", game=None):
        gameName = gamesDir[game - 1]
        oldUsers = os.listdir(r"{}/{}".format(Path, gameName))
        users = []
        for user in oldUsers:
            if os.path.isdir(r'{}/{}/{}'.format(Path, gameName, user)):
                users.append(user)
        if os.path.exists("{}/{}/win".format(Path, gameName)):
            Functions.clear()
            # change to a different layout
            for i in range(len(users)):
                if users[i] != "win":
                    print("{} data\ngrid (where they shot)".format(users[i]))  # noqa
                    save.board.DisplayBoard(save.save(Path).readFile(os.path.join(gameName, users[i]), "grid"))  # noqa
                    print("{} data\nships (The ship layout they had)".format(users[i]))  # noqa
                    save.board.DisplayBoard(save.save(Path).readFile(os.path.join(gameName, users[i]), "ships"))  # noqa
            input("Press enter when you are ready to continue.")
            self.__reset()
        else:
            placed = False
            if os.path.exists("{}/{}/{}/ships".format(Path, gameName, users[0])):  # noqa
                if os.path.exists("{}/{}/{}/ships".format(Path, gameName, users[1])):  # noqa
                    placed = True
                else:
                    print("{} not placed".format(users[1]))
            Multi = False
            if os.path.exists(os.path.join("{}".format(gameName), "multi")):
                Multi = True
            self.__reset(None, True, gameName, users, placed, Path, Multi)  # noqa

    # Function to process user inputs
    def _ProcessChoice(self):
        # Errors if files not found.
        if self.choice == 1 and not os.path.exists("Saves"):
            self.__reset("There is no game to load!!")
        elif self.choice == 1 and len(os.listdir("Saves")) == 0:
            self.__reset("There is no game to load!!")
        elif self.choice == 1:
            # load game
            Functions.clear()
            self._loadGames()
            game = Functions.check("Enter number of game to load (-1 to go back): ", self._loadGames, None, self._LoadRangeCheck).InputDigitCheck()  # noqa
            if game == -1:
                self.__reset()
            elif game == 0:
                Functions.clear(1)
                external = None
                while not external:
                    external = input("Please enter location of storage: ").rstrip().replace('"', '')  # noqa
                    if platform.system() != "Windows":
                        external = external.replace("\\", "")  # noqa
                    if not os.path.isdir(external):
                        external = None
                        Functions.clear(2, "Provided directory is not a directory")  # noqa
                games = self._loadGames(external)
                externalgame = Functions.check("Enter number of game to load (-1 to go back): ", self._loadGames, external, self._LoadRangeCheck, external).InputDigitCheck()  # noqa
                if externalgame == -1:
                    self.__reset()
                else:
                    self._LoadGame(games, external, externalgame)  # noqa
            else:
                self._LoadGame(os.listdir("Saves"), "Saves", game)

        elif self.choice == 2:
            self.name, self.users, self.Placed, self.saveLocation, self.twoPlayer = Create.create().setup()  # noqa
        elif self.choice == 0:
            # Quites
            sys.exit("Thank you for playing")
        elif self.choice == 3:
            # Other small stuff
            self.__reset("Settings are comming later, please wait")

    # Read the options. Allows for easy to change menu
    def _fileRead(self):
        with open("Options.txt", "r") as options:
            lines = options.readlines()
            for line in range(len(lines)):
                path = str(lines[line].strip())
                if line == 1:
                    if os.path.exists("Saves"):
                        if len(os.listdir("Saves")) == 0:
                            path += " (disabled)"
                    else:
                        path += " (disabled)"
                print(path)

    def setup(self):
        while not self.choice:
            Functions.clear()
            # Load interface thing...
            self._fileRead()
            # get the user choice
            self.choice = Functions.check("Your Choice (number): ", self._fileRead).InputDigitCheck()  # noqa
            # Process choice
            self._ProcessChoice()
            time.sleep(1)
        return self.name, self.users, self.Placed, self.saveLocation, self.twoPlayer  # noqa
