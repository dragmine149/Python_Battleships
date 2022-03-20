import os
import sys
import time
import SaveSystem as save
import Functions
import boardCreate as Create


class game:
    def __init__(self):
        self.choice = None
        self.name = None
        self.users = None
        self.Placed = None

    # Resets the game class for a new use
    def __reset(self, message=None, choice=None, name=None, users=None, Placed=None):  # noqa
        self.name = name
        self.users = users
        self.Placed = Placed
        self.choice = choice
        if message:
            print(message)

    # Prints off all games found
    def _loadGames(self):
        print("Games found on disk:")
        games = os.listdir("Saves")
        for file in range(len(games)):
            path = "{}: {}".format(file + 1, games[file])
            if os.path.exists("Saves/{}/win.txt".format(games[file])):
                path += " (finished)"
            print(path)

    # The range check function for amount of saves
    def _LoadRangeCheck(self, value):
        amount = len(os.listdir("Saves"))
        if value > 0 and value <= amount:
            return True
        elif value == -1:
            return True
        return False

    @staticmethod
    def SizeRangeCheck(size):
        # replace with amount of ships in game.
        if size >= 5:  # got to be big enough to hold all ships
            return True
        return False

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
            else:
                gameName = os.listdir('Saves')[game - 1]
                users = os.listdir("Saves/{}".format(gameName))
                if os.path.exists("Saves/{}/win.txt".format(gameName)):
                    Functions.clear()
                    # change to a different layout
                    for i in range(len(users)):
                        if users[i] != "win.txt":
                            print("{} data\ngrid (where they shot)".format(users[i]))  # noqa
                            save.board.DisplayBoard(save.read(gameName, users[i]))  # noqa
                            print("{} data\nships (The ship layout they had)".format(users[i]))  # noqa
                            save.board.DisplayBoard(save.read(gameName, users[i], "ships"))  # noqa
                    input("Press enter when you are ready to continue.")
                    self.__reset()
                else:
                    placed = False
                    if os.path.exists("Saves/{}/{}/ships.txt".format(gameName, users[0])) and os.path.exists("Saves/{}/{}/ships.txt".format(gameName, users[1])):  # noqa
                        placed = True
                    self.__reset(None, True, gameName, users, placed)
        elif self.choice == 2:
            Create.create().setup()
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
        return self.name, self.users, self.Placed
