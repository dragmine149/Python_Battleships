import getpass
import string
import random
import importlib
Functions = importlib.import_module('Files.Functions')
Save = importlib.import_module('Files.Save')
ShipInfo = importlib.import_module('Files.ShipInfo')


class CreateData:
    def __init__(self, path="Saves", name=None):
        # Load the class and all it's data
        self.Gname = name
        self.usernames = [getpass.getuser(), None]
        self.siZe = [10, 10]

        self.Loc = path
        result = Functions.LocationTest(path)
        if not result:
            self.Loc = "Saves"

        self.Multi = "no"
        self.password = None
        self.VisiblePassword = "Disabled"
        self.colours = ['\033[31m',
                        ['\033[32m', '\033[31m'],
                        '\033[32m',
                        '\033[32m',
                        '\033[32m',
                        '\033[33m']

    def showOptions(self):
        # Prints off the current settings and what options are alvalible
        print('''Current Settings:
Name: {}{}\033[0m
Players: [{}{}, {}{}\033[0m]
Size: {}{}\033[0m
Save Location: {}{}\033[0m
Multiplayer: {}{}\033[0m
Password: {}{}\033[0m
'''.format(
            self.colours[0],
            self.Gname,
            self.colours[1][0],
            self.usernames[0],
            self.colours[1][1],
            self.usernames[1],
            self.colours[2],
            self.siZe,
            self.colours[3],
            self.Loc,
            self.colours[4],
            self.Multi,
            self.colours[5],
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
                return [self.Gname, self.usernames, self.Loc, self.Multi[0]]
        return None

    def name(self):
        # Gets the name of the game
        self.Gname = None
        while self.Gname is None:
            # get input
            self.Gname = input("Please enter the game name\033[%d;%dH" % (2, 7))  # noqa
            if self.Gname == "None":
                self.Gname = None
                continue

            games = Functions.RemoveNonGames(self.Loc)
            if self.Gname not in games:
                self.colours[0] = '\033[32m'
                return

            randomEnd = ''
            for _ in range(10):
                randomEnd += random.choice(string.ascii_letters)

            def yesFunc():
                self.Gname = '{}_{}'.format(self.Gname, randomEnd)
                self.colours[0] = '\033[32m'

            def noFunc():
                self.colours[0] = '\033[33m'
                # Functions.clear(0, "Please enter a new game name!")
                # return "Name"

            result = Functions.check("Game with this name already exists. Rename to '{}_{}'?: ".format(self.Gname, randomEnd), returnFunc=(yesFunc, noFunc)).getInput("ynCheck")  # noqa E501

    def __nameCheck(self, name, old, other=None):
        newName = name

        # Use system name if 'me'
        if name.rstrip().lower()[:2] == 'me':
            newName = getpass.getuser()
            if name[2:] != '':
                newName += '({})'.format(name[2:])

        # check for blank
        if name.rstrip() == '':
            newName = old

        # Add (2) is both names same
        if other is not None:
            if other == newName:
                newName += '(2)'

        if str(newName) == "None":
            return False
        return newName

    def username(self):
        # Get the players names
        oldUsers = self.usernames
        self.usernames = [None, None]

        # loop
        for i in range(2):
            while self.usernames[i] is None:

                # get the last name
                pastName = None
                pastNameText = ''
                if i >= 1:
                    pastName = self.usernames[i - 1]
                    pastNameText = pastName + ', '

                # Move cursor and stuff
                print("\033[%d;%dH" % (19, 0))
                space = " " * (len(str(oldUsers)) - 1)
                print("Please enter player {}'s name (Blank to keep same)".format(i + 1), end='')  # noqa E501
                print("\033[%d;%dHPlayers: [{}".format(space) % (3, 0), end='')
                self.usernames[i] = input("\033[%d;%dH{}".format(pastNameText) % (3, 11))  # noqa E501
                print("\033[%d;%dH" % (19, 0))

                # Process input
                nameResult = self.__nameCheck(self.usernames[i],
                                              oldUsers[i], pastName)

                # annoyed
                if not nameResult:
                    self.usernames[i] = None
                    print("Player {} name is not allowed!".format(i + 1))
                    continue

                # save
                self.usernames[i] = nameResult

        # finish
        self.colours[1] = ['\033[32m', '\033[32m']

    def size(self):
        # get the size of the game board.
        oldSize = self.siZe
        self.siZe = []
        x = None
        y = None

        while x is None:
            print("\033[%d;%dHSize: [{}".format(" " * len(str(oldSize))) % (4, 0))  # noqa E501
            print("\033[%d;%dH" % (19, 0))
            x = input("Please enter X coordinate \033[%d;%dHSize: [" % (4, 0))
            print("\033[%d;%dH" % (19, 0))

            if not x.isdigit():
                Functions.warn(2, "X is not a digit!{}".format(" " * 25), "red")  # noqa E501
                x = None

            if x.isdigit():
                x = int(x)
                if x < 5:
                    Functions.warn(2, "X is too small!", "red")
                    x = None

        while y is None:
            y = input("Please enter Y coordinate\033[%d;%dHSize: [{}, ".format(x) % (4, 0))  # noqa E501
            print("]\033[%d;%dH" % (19, 0))

            if not y.isdigit():
                Functions.warn(2, "Y is not a digit!{}".format(" " * 25), "red")  # noqa E501
                y = None

            if y.isdigit():
                y = int(y)
                if y < 5:
                    Functions.warn(2, "Y is too small!", "red")
                    y = None

        self.siZe = [x, y]
        self.colours[2] = '\033[32m'

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
                self.Multi = "no"  # automatically reset multiplayer

            # If default, don't need to do much
            # If drive, run test
            # If external, run test

            # skip doing stuff to saves
            if Location != "Saves":
                # attmepts to write file and read file from dir specified
                # creates save obj
                allowed = Functions.LocationTest(Location)
                if not allowed[0]:
                    Location = None
                    Functions.warn(2, "Error occured whilst trying to change location.", ["", "red"])

        print({"Loc": Location})
        self.Loc = Location
        self.colours[4] = "\033[32m"

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
                self.colours[5] = '\033[33m'
                return
            check = None
            while check is None:
                check = getpass.getpass("Please re-enter the password (-1 to change password): ")  # noqa E501
                if check == password:
                    self.VisiblePassword = "Enabled"
                    self.colours[5] = '\033[32m'
                    self.password = password
                    return True
                if check == -1:
                    self.VisiblePassword = "Disabled"
                    self.colours[5] = '\033[31m'
                    self.password = None

    def check(self):
        # Checks if all fields are valid.
        # This is done because game name might relay on save location but will still let you enter it.  # noqa E051
        if self.Gname is None:
            Functions.clear(2, "Please enter a name!")
            return "Name"
        if self.usernames[0] is None or self.usernames[1] is None:
            Functions.clear(2, "Please enter player names!")
            return "Username"

        for user in self.usernames:
            if user.find('/') > -1 or user.find('\\') > -1:
                Functions.clear(2, "Username cannot have '/' or '\\' in!")
                return "Invalid Name"

        # Password better than no password, Check
        if self.password is None:
            continueChoice = Functions.check("No password has been set, Continue?: ", returnFunc=(None, "password")).getInput("ynCheck")  # noqa E501
            if continueChoice is not None:
                return continueChoice
        return True

    def save(self):
        if self.check() is not True:
            Functions.clear(2, "Please check settings")
            return False

        # Get the user to enter the password to save
        if self.password is not None:
            check = getpass.getpass("Please enter the password to save the game: ")  # noqa E501
            if check != self.password:
                Functions.clear(2, "Please make sure you can remeber the password")  # noqa E501
                return False

        # Create board
        board = Functions.board.CreateBoard(self.siZe)

        # Create folder for the game
        gameData = Save.save({
            'name': self.Gname,
            'path': self.Loc,
        })

        gameFolder = gameData.makeFolder()

        userFolders = []
        for user in self.usernames:
            # create user data
            userData = Save.save({
                'name': user,
                'path': self.Loc + "/" + gameFolder,
            })
            # create user folder
            folder = userData.makeFolder()
            userFolders.append(folder[0])

            # create files for users
            userData.writeFile(board, 'ships')

            placedData = {}
            for ship in ShipInfo.getShips():
                placedData[ship.Name] = False

            # print(placedData)
            userData.writeFile(placedData, "placedData")
# userData.writeFile(board, name='shots')

        # make turn file, notes whos turn it is.
        data = {
            'turn': self.usernames[0],
            'multi': self.Multi[0],
            'password': self.password,
            'size': self.siZe,
        }
        gameData.ChangeDirectory(gameFolder)
        gameData.writeFile(data, "GameData")

        return "Save"  # success!!!


if __name__ == '__main__':
    c = CreateData("Saves")
    result = c.getOption()
    # print(result)
