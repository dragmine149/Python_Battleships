import Functions

class CreateData:
    def __init__(self):
        print("Loading")
        self.Gname = None
        self.usernames = None
        self.siZe = None

    def showOptions(self):
        print('0: Quit. 1: Game Name. 2: Usernames. 3: Board Size. 4: Save Location. 5: Save and make game.')
        print('Current Settings:')
        print('Name: {}'.format(self.Gname))
        print('UserNames: {}'.format(self.usernames))
        print('Size: {}'.format(self.siZe))

    def getOption(self):
        choice = None
        while choice != 0:
            choice = Functions.check("What would you like to change?: ", self.showOptions, None, Functions.NumberRangeCheck, 5).InputDigitCheck()
            if choice == 1:
                self.name()
            elif choice == 2:
                self.username()
            elif choice == 3:
                self.size()
            elif choice == 4:
                self.saveLoc()
            elif choice == 5:
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
                user2 = input("Please enter player 2's name: ")
                if user2 == user1:
                    user2 = None
                    Functions.clear(1, "Player 2's name can not be the same as player 1!")
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
                Functions.clear(2, "Invalid format! 'x' was not found in the input")

    def saveLoc(self):
        print("saveLoc")

    def save(self):
        print("save")

if __name__ == '__main__':
    c = CreateData()
    c.getOption()
