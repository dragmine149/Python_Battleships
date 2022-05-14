import Functions
import Save


class CreateData:
    def __init__(self):
        print("Loading")
        self.Gname = None
        self.usernames = None
        self.siZe = None
        self.Loc = None
        self.Multi = False

    def showOptions(self):
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
        choice = None
        while choice != 0:
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
                self.save()

    def name(self):
        self.Gname = None
        while self.Gname is None:
            self.Gname = input("Please enter the game name: ")
            # Check?

    def username(self):
        self.usernames = []
        while len(self.usernames) < 2:
            user1 = input("Please enter player 1's name: ")
            user2 = None
            while user2 is None:
                user2 = input("\033[F\rPlease enter player 2's name: ")
                if user2 == user1:
                    user2 = None
                    Functions.clear(1, "Player 2's name can not be the same as player 1!")  # noqa E501
            self.usernames = [user1, user2]

    def size(self):
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
        multi = None
        while multi is None:
            multi = input("Online Multiplayer (y = 2 people on different devices. n = 2 people on same device): ")  # noqa E501
            if multi.lower()[0] == "y":
                self.Multi = "yes"
            elif multi.lower()[0] == "n":
                self.Multi = "no"
            else:
                multi = None
                Functions.clear(2, "Please enter y or n!")

    def save(self):
        print("save")


if __name__ == '__main__':
    c = CreateData()
    c.getOption()
