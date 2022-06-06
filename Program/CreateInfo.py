import Functions
import newSave
import random
import string
import getpass


class CreateData:
    def __init__(self, path="Saves", name=None):
        # Load the class and all it's data
        self.Gname = name
        self.usernames = [getpass.getuser(), 'None']
        self.siZe = [10, 10]
        self.Loc = path
        self.Multi = "no"
        self.password = None
        self.VisiblePassword = "Disabled"

    def showOptions(self):
        # Prints off the current settings and what options are alvalible
        print('''Current Settings:
Name: {}
Players: {}
Size: {}
Save Location: {}
Multiplayer: {}
Password: {}
'''.format(
            self.Gname,
            self.usernames,
            self.siZe,
            self.Loc,
            self.Multi,
            self.VisiblePassword))
        print('''Options:
0: Quit
1: Game Name
2: Usernames
3: Board Size
4: Save Location
5: Multiplayer (both on same device, or different devices)
6: Password
7: Save and make game
''')

    def quit(self):
        return

    def getOption(self):
        # Get the option inputed and do the command required / called.
        choice = None
        while choice != 0:
            options = {
                0: self.quit,
                1: self.name,
                2: self.username,
                3: self.size,
                4: self.saveLoc,
                5: self.MultiPlayer,
                6: self.Password,
                7: self.save
            }

            Functions.clear()
            choice = Functions.check("What would you like to change?: ",
                                     self.showOptions,
                                     (0, 7)).getInput()

            choiceFunction = options[choice]
            result = choiceFunction()
            if result == "Save":
                return [self.Gname, self.usernames, self.Loc, self.Multi]
        return None

    def name(self):
        # Gets the name of the game
        self.Gname = None
        while self.Gname is None:
            self.Gname = input("Please enter the game name\033[%d;%dH" % (2, 7))  # noqa

    def username(self):
        # Get the players names
        self.usernames = []

        while len(self.usernames) < 2:
            user1 = input("Please enter player 1's name")
            if user1 == "me":
                # sets them to use the username on their account.
                user1 = getpass.getuser()
                print("\033[F\rPlease enter player 1's name: {}".format(user1))
            if user1 != "":
                user2 = None
                while user2 is None:
                    # \033[F\r -> Sends the cursor back to the start of the previous line  # noqa E501
                    # In this case, overwrites previous input with new input
                    extra = " " * len(user1)
                    print("\033[F\rPlease enter player 2's name: {}".format(extra))
                    user2 = input("\033[F\rPlease enter player 2's name: ")
                    if user2 == "me":
                        user2 = getpass.getuser()

                    if user2 == user1:
                        user2 = None
                        Functions.warn(1, "\033[F\rPlayer 2's name can not be the same as player 1!")  # noqa E501
                        print("\033[F\r                                                ")  # noqa E501
                        # ^^ clears input, resets
                    if user2 == "":
                        user2 = None
                        Functions.warn(1, "\033[F\rPlayer 2's name can't be nothing!")  # noqa E501
                        print("\033[F\r                                                ")  # noqa
                self.usernames = [user1, user2]
            else:
                user1 = None
                Functions.clear("Player 1's name can't be nothing!")

    def size(self):
        # get the size of the game board.
        oldSize = self.siZe
        self.siZe = []
        while len(self.siZe) < 2:
            # Formatting and moving cursor (PAIN kinda)
            print("\033[%d;%dHSize: [{}".format(" " * len(str(oldSize))) % (4, 0))  # noqa E501
            print("\033[%d;%dH" % (19, 0))
            x = input("Please enter X coordinate\033[%d;%dHSize: [" % (4, 0))
            print("\033[%d;%dH" % (19, 0))
            y = input("Please enter Y coordinate\033[%d;%dHSize: [{}, ".format(x) % (4, 0))  # noqa E501
            print("]\033[%d;%dH" % (19, 0))

            # processing inputs
            notDigit = ""
            if not x.isdigit():
                notDigit = "X is not a digit! "
            if not y.isdigit():
                notDigit += "Y is not a digit!"

            if not notDigit:
                small = ""
                x = int(x)
                y = int(y)
                if x < 5:
                    small = "X is too small! "
                if y < 5:
                    small += "Y is too small!"
                if not small:
                    self.siZe = [x, y]
                    return

                Functions.warn(2, small + "\033[F\r", "red")
                print("{}\033[F\r".format(" " * len(small)))

            if notDigit:
                Functions.warn(2, notDigit + "\033[F\r", "red")
                print("{}\033[F\r".format(" " * len(notDigit)))
            oldSize = str([x, y])

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
                Functions.LocationTest(Location)

        print({"Loc": Location})
        self.Loc = Location

    def MultiPlayer(self):
        if self.Loc == "Saves":
            Functions.clear(2, "Disabled! Save location is default, Please change to have multiplayer support!", "red")  # noqa E501
            return
        # get if multiplayer or not
        multi = None
        while multi is None:
            def returnFunc():
                Functions.clear(2, "Please enter y or n!")
                return None

            multi = Functions.check("Online Multiplayer (y = 2 players on different devices, n = 2 players on the same device): ", returnFunc=("yes", "no", returnFunc)).getInput("ynCheck")  # noqa E501
        self.Multi = multi

    def Password(self):
        self.password = None  # change to ask for password?
        self.VisiblePassword = "Disabled"

        while self.password is None:
            password = getpass.getpass("Enter a password (blank for no passwords): ")  # noqa E501
            if password.rstrip() == "":
                self.password = None
                self.VisiblePassword = "Disabled"
                return
            check = None
            while check is None:
                check = getpass.getpass("Please re-enter the password (-1 to change password): ")  # noqa E501
                if check == password:
                    self.VisiblePassword = "Enabled"
                    return True
                if check == -1:
                    self.VisiblePassword = "Disabled"
                    self.password = None

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

            result = Functions.check("Game with this name already exists. Rename to '{}_{}'?: ".format(self.Gname, randomEnd), returnFunc=(yesFunc, noFunc)).getInput("ynCheck")  # noqa E501
            if result == "Name":
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
        gameData = newSave.save({
            'name': self.Gname,
            'path': self.Loc,
            'Json': True
        })

        gameFolder = gameData.makeFolder(replace=True)
        print(gameFolder)
        gameFolder = gameFolder

        userFolders = []
        for user in self.usernames:
            # create user data
            userData = newSave.save({
                'name': user,
                'path': gameFolder,
                'Json': True
            })
            # create user folder
            folder = userData.makeFolder(replace=True)
            userFolders.append(folder[0])

            # create files for users
            userData.writeFile(board, name='ships')
# userData.writeFile(board, name='shots')

        # make turn file, notes whos turn it is.
        data = {
            'turn': self.usernames[0],
            'multi': self.Multi[0],
            'password': self.password[0]
        }
        gameData.writeFile(data, name="GameData")

        return "Save"  # success!!!


if __name__ == '__main__':
    c = CreateData("Saves")
    result = c.getOption()
    print(result)
