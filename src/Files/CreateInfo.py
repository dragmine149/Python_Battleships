import getpass
import string
import random

from PythonFunctions.CleanFolderData import Clean
from PythonFunctions.Message import Message
from PythonFunctions.Check import Check
from PythonFunctions.Save import save
from PythonFunctions import Board
from Files import ShipInfo


class CreateData:
    def __init__(self, path="Saves", name=None):
        # Load the class and all it's data
        self.Gname = name
        self.usernames = [getpass.getuser(), None]
        self.siZe = [10, 10]
        self.Loc = path
        self.Multi = "no"
        self.password = None
        self.VisiblePassword = "Disabled"
        self.colours = ['\033[31m',
                        ['\033[32m', '\033[31m'],
                        '\033[32m',
                        '\033[32m',
                        '\033[32m',
                        '\033[33m']
        self.msg = Message()
        self.chk = Check()
        self.cln = Clean()
        self.saveModule = save() 

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

            self.msg.clear()
            choice = self.chk.getInput("What would you like to change?: ",
                                       self.chk.ModeEnum.int,
                                       lower=0, higher=7)

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

            games = self.cln.clean(self.Loc)
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

            newName = '{self.Gname}_{randomEnd}'
            self.chk.getInput(
                f"Game with this name already exists. Rename to {newName}",
                self.chk.ModeEnum.yesno,
                y=yesFunc, n=noFunc)

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
                print(f"Please enter player {i + 1}'s name (Blank to keep same)", end='')
                print("\033[%d;%dHPlayers: [{}".format(space) % (3, 0), end='')
                self.usernames[i] = input(
                    f"\033[%d;%dH{pastNameText}" % (3, 11))
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
            print(f"\033[%d;%dHSize: [{' ' * len(str(oldSize))}" % (4, 0))
            print("\033[%d;%dH" % (19, 0))
            x = input("Please enter X coordinate \033[%d;%dHSize: [" % (4, 0))
            print("\033[%d;%dH" % (19, 0))

            if not x.isdigit():
                self.msg.warn(f"X is not a digit!{' ' * 25}", 2)
                x = None

            if x.isdigit():
                x = int(x)
                if x < 5:
                    self.msg.warn("X is too small!", 2)
                    x = None

        while y is None:
            y = input("Please enter Y coordinate\033[%d;%dHSize: [{}, ".format(x) % (4, 0))
            print("]\033[%d;%dH" % (19, 0))

            if not y.isdigit():
                self.msg.warn(f"Y is not a digit!{' ' * 25}", 2)
                y = None

            if y.isdigit():
                y = int(y)
                if y < 5:
                    self.msg.warn("Y is too small!", 2)
                    y = None

        self.siZe = [x, y]
        self.colours[2] = '\033[32m'

    def saveLoc(self):
        # get the game save location
        Location = None
        while Location is None:
            self.msg.clear()
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
                    self.msg.warn(
                        "Error occured whilst trying to change location.", 2)

        print({"Loc": Location})
        self.Loc = Location
        self.colours[4] = "\033[32m"

    def MultiPlayer(self):
        if self.Loc == "Saves":
            self.msg.clear(
                "Disabled! Save location is default, Please change to have multiplayer support!", 2
            )
            return
        # get if multiplayer or not
        
        multi = self.chk.getInput(
            "Online multiplayer? (y = different devices, n = same device)",
            self.chk.ModeEnum.yesno)
        self.Multi = "yes" if multi else "no"

    def Password(self):
        self.password = None  # change to ask for password?
        self.VisiblePassword = "Disabled"

        while self.password is None:
            password = getpass.getpass(
                "Enter a password (blank for no passwords): ")
            if password.rstrip() == "":
                self.password = None
                self.VisiblePassword = "Disabled"
                self.colours[5] = '\033[33m'
                return
            check = None
            while check is None:
                check = getpass.getpass(
                    "Please re-enter the password (-1 to change password): ")
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
            self.msg.clear("Please enter a name!", 2)
            return "Name"
        if self.usernames[0] is None or self.usernames[1] is None:
            self.msg.clear("Please enter player names!", 2)
            return "Username"

        for user in self.usernames:
            if user.find('/') > -1 or user.find('\\') > -1:
                self.msg.clear("Username cannot have '/' or '\\' in!", 2)
                return "Invalid Name"

        # Password better than no password, Check
        if self.password is None:
            continueChoice = self.chk.getInput(
                "No password has been set, Continue?: ",
                self.chk.ModeEnum.yesno,
                y=None,
                n="password"
            )
            if continueChoice is not None:
                return continueChoice
        return True

    def save(self):
        if self.check() is not True:
            self.msg.clear("Please check settings", 2)
            return False

        # Get the user to enter the password to save
        if self.password is not None:
            check = getpass.getpass("Please enter the password to save the game: ")
            if check != self.password:
                self.msg.clear("Please make sure you can remember the password", 2)
                return False

        # Create board
        board = Board.CreateBoard(self.siZe)

        # Create folder for the game
        gameLoc = f'{self.Loc}/{self.Gname}'
        self.saveModule.MakeFolders(gameLoc)

        userFolders = []
        for user in self.usernames:
            # create user data
            userLoc = f'{gameLoc}/{user}'
            self.saveModule.MakeFolders(userLoc)
            userFolders.append(userLoc)
            self.saveModule.Write(board, f'{userLoc}/ships',
                                  encoding=self.saveModule.encoding.BINARY)

            placedData = {}
            for ship in ShipInfo.getShips():
                placedData[ship.Name] = False

            self.saveModule.Write(board, f'{userLoc}/placedData',
                                  encoding=self.saveModule.encoding.BINARY)

        # make turn file, notes whos turn it is.
        data = {
            'turn': self.usernames[0],
            'multi': self.Multi[0],
            'password': self.password,
            'size': self.siZe,
        }
        self.saveModule.Write(data, f'{gameLoc}/GameData',
                              encoding=self.saveModule.encoding.BINARY)

        return "Save"  # success!!!


if __name__ == '__main__':
    c = CreateData("Saves")
    result = c.getOption()
    # print(result)
