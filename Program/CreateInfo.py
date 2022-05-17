import Functions
import Save
import random
import string


class CreateData:
    def __init__(self):
        # Load the class and all it's data
        self.Gname = None
        self.usernames = None
        self.siZe = [10, 10]
        self.Loc = "Saves"
        self.Multi = "no"

    def showOptions(self):
        # Prints off the current settings and what options are alvalible
        print('''Current Settings:
Name: {}
Players: {}
Size: {}
Save Location: {}
Multiplayer: {}
'''.format(self.Gname, self.usernames, self.siZe, self.Loc, self.Multi))
        print('''Options:
0: Quit
1: Game Name
2: Usernames
3: Board Size
4: Save Location
5: Multiplayer (both on same device, or different devices)
6: Save and make game
''')

    def getOption(self):
        # Get the option inputed and do the command required / called.
        choice = None
        while choice != 0:
            result = True
            Functions.clear()
            choice = Functions.check("What would you like to change?: ", self.showOptions, None, Functions.NumberRangeCheck, 6).InputDigitCheck()  # noqa E501
            if choice == 1:
                self.name()
            elif choice == 2:
                self.username()
            elif choice == 3:
                self.size()
            elif choice == 4:
                self.saveLoc()
            elif choice == 5:
                if self.Loc == "Saves":
                    Functions.clear(2, "Disabled! Please use a directory other than the default!")  # noqa E501
                else:
                    self.MultiPlayer()
            elif choice == 6:
                result = self.save()
                if result:
                    choice = 0  # end, result is good.
                # return [name, users, Location, online]

    def name(self):
        # Gets the name of the game
        self.Gname = None
        while self.Gname is None:
            self.Gname = input("Please enter the game name: ")

    def username(self):
        # Get the players names
        self.usernames = []

        while len(self.usernames) < 2:
            user1 = input("Please enter player 1's name: ")
            if user1 != "":
                user2 = None
                while user2 is None:
                    # \033[F\r -> Sends the cursor back to the start of the previous line  # noqa E501
                    # In this case, overwrites previous input with new input
                    user2 = input("\033[F\rPlease enter player 2's name: ")
                    if user2 == user1:
                        user2 = None
                        Functions.clear(1, "Player 2's name can not be the same as player 1!")  # noqa E501
                    if user2 == "":
                        user2 = None
                        Functions.clear("Player 2's name can't be nothing!")
                self.usernames = [user1, user2]
            else:
                user1 = None
                Functions.clear("Player 1's name can't be nothing!")

    def size(self):
        # get the size of the game board.
        self.siZe = []
        while len(self.siZe) < 2:
            gridSize = input("Please enter board size (Format: XxY): ")
            if gridSize.find('x') > -1:
                gridSize = gridSize.split("x")
                notDigit = None
                if not gridSize[0].isdigit() or not gridSize[1].isdigit():
                    notDigit = "Neither inputs are digits!"
                elif not gridSize[0].isdigit():
                    notDigit = "First value is not a digit!"
                elif not gridSize[1].isdigit():
                    notDigit = "Second value is not a digit!"
                else:
                    self.siZe = [int(gridSize[0]), int(gridSize[1])]
                if notDigit is not None:
                    Functions.clear(2, notDigit)
            else:
                Functions.clear(2, "Invalid format! 'x' was not found in the input")  # noqa E501

    def saveLoc(self):
        # get the game save location
        Location = None
        while Location is None:
            Functions.clear()
            print("""Save Location:
- Supports google drive folder id (if google drive api installed)
- Leave blank for default location
- Type path to folder for different location than the default
""")
            Location = input("Save location: ")

            # Saves is the default location, only chosen if the input is blank.
            if Location == "":
                Location = "Saves"

            # If default, don't need to do much
            # If drive, run test
            # If external, run test

            # skip doing stuff to saves
            if Location != "Saves":
                # attmepts to write file and read file from dir specified
                # creates save obj
                saveInfo = Save.save(Location, False, {
                    'name': 'Test',
                    'file': 'test'
                })
                print(vars(saveInfo))

                # creates file
                savedLocation = saveInfo.writeFile("This is a test file")

                # reads file from same place
                data = saveInfo.readFile('Test')
                print(data)

                if data != "This is a test file":
                    # Oh oh, doesn't work... Return error
                    Functions.clear(3, "Please make sure that this program has read and write ability to {}".format(Location))  # noqa
                    Location = None

                saveInfo.Delete(savedLocation)

        print({"Loc": Location})
        self.Loc = Location

    def MultiPlayer(self):
        # get if multiplayer or not
        multi = None
        while multi is None:
            def returnFunc():
                Functions.clear(2, "Please enter y or n!")
                return None

            multi = Functions.ynCheck(input("Online Multiplayer (y = 2 people on different devices. n = 2 people on same device): "), "yes", "no", returnFunc)  # noqa E501

    def check(self):
        # Checks if all fields are valid.
        # This is done because game name might relay on save location but will still let you enter it.  # noqa E051
        if self.Gname is None:
            Functions.clear(2, "Please enter a name!")
            return "Name"
        if self.usernames is None:
            Functions.clear(2, "Please enter player names!")

        games = Functions.RemoveNonGames(self.Loc)
        if self.Gname in games:
            randomEnd = ''
            for _ in range(10):
                randomEnd += random.choice(string.ascii_letters)

            def yesFunc():
                self.Gname = '{}_{}'.format(self.Gname, randomEnd)

            def noFunc():
                Functions.clear(0, "Please enter a new game name!")
                return "Name"

            if Functions.ynCheck(input("Game with this name already exists. Rename to '{}_{}'?: ".format(self.Gname, randomEnd)), yesFunc, noFunc) == "Name":  # noqa E501
                return "Name"

        if self.Loc == "Saves" and self.Multi == "yes":
            print("Automatically set multiplayer to false because you are using the default directory")  # noqa E051
            self.Multi = "no"
            return "Multi"
        return True

    def save(self):
        if self.check() is not True:
            Functions.clear(2, "Please check settings")
            return False
        # Create board
        board = Functions.board.CreateBoard(self.siZe)

        # Create folder for the game
        gameData = Save.save(self.Loc, data={
            'name': self.Gname,
            'file': ''
        })

        gameFolder = gameData.makeFolder(replace=True)
        gameFolder = gameFolder[0]

        userFolders = []
        for user in self.usernames:
            # create user data
            userData = Save.save(gameFolder, data={
                'name': user,
                'file': ''
            })
            # create user folder
            folder = userData.makeFolder(replace=True)
            userFolders.append(folder[0])

            # create files for users
            userData.writeFile({
                'data': board,
            }, 'ships')

        # make turn file, notes whos turn it is.
        gameData.writeFile({
            'data': self.usernames[0]
        }, 'turn')
        gameData.writeFile({
            'data': self.Multi[0]
        }, 'multi')

        return True  # success!!!


if __name__ == '__main__':
    c = CreateData()
    c.getOption()
