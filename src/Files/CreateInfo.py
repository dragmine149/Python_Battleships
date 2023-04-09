import getpass
import string
import random
from colorama import Fore
from PythonFunctions.PrintTraceback import PrintTraceback
from PythonFunctions.CleanFolderData import Clean
from PythonFunctions.Message import Message
from PythonFunctions.Check import Check
from PythonFunctions.Save import save
from PythonFunctions import Board
from Files import ShipInfo


class CreateData:
    def __init__(self, path="Saves", name=None):
        # Load the class and all it's data
        self.info = {
            'Name': {
                'value': str(name),
                'colour': Fore.RED
            },
            'Players': {
                'Player 1': {
                    'value': getpass.getuser(),
                    'colour': Fore.GREEN
                },
                'Player 2': {
                    'value': 'None',
                    'colour': Fore.RED
                }
            },
            'Size': {
                'X': {
                    'value': 10,
                    'colour': Fore.GREEN
                },
                'Y': {
                    'value': 10,
                    'colour': Fore.GREEN
                }
            },
            'Location': {
                'value': path,
                'colour': Fore.GREEN
            },
            'Multiplayer': {
                'value': 'no',
                'colour': Fore.GREEN
            },
            'Password': {
                'true': None,
                'value': 'Disabled',
                'colour': Fore.YELLOW
            }
        }
        self.msg = Message()
        self.chk = Check()
        self.cln = Clean()
        self.saveModule = save()

    def getGameList(self):
        return self.cln.clean(self.saveModule.ListFolder(
            self.info.get('Location').get('value')))

    def getInfoFieldValue(self, name: str, subname: str = None):
        field = self.info.get(name)
        if subname:
            return field.get(subname).get('value')
        return field.get('value')

    def PrintSetting(self, setting):
        data = self.info.get(setting)
        if data.get('value') is not None:
            return f"{setting}: {data.get('colour')}{data.get('value')}{Fore.RESET}"

        msg = f"{setting}: ["
        for index, value in enumerate(data):
            keyData = data.get(value)
            msg += f"{keyData.get('colour')}{keyData.get('value')}{Fore.RESET}"
            if index != len(data.keys()) - 1:
                msg += ', '
        msg += ']'
        return msg

    def showOptions(self):
        # Prints off the current settings and what options are alvalible
        print(f"""Current Settings:
{self.PrintSetting('Name')}
{self.PrintSetting('Players')}
{self.PrintSetting('Size')}
{self.PrintSetting('Location')}
{self.PrintSetting('Multiplayer')}
{self.PrintSetting('Password')}""")

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

    def main(self):
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

            self.showOptions()
            choice = self.chk.getInput("What would you like to change?: ",
                                       self.chk.ModeEnum.int,
                                       lower=0, higher=7)

            choiceFunction = options[choice]
            result = choiceFunction()
            if result == "Save":
                return [
                    self.getInfoFieldValue('Name'),
                    [self.getInfoFieldValue('Players', 'Player 1'),
                     self.getInfoFieldValue('Players', 'Player 2')],
                    self.getInfoFieldValue('Location'),
                    self.getInfoFieldValue('Multiplayer')
                ]
        return None

    def name(self) -> str:
        gameName = None
        while gameName is None:
            gameName = input(
                "Please enter the game name (blank to keep same)\033[%d;%dH" % (2, 7))
            if gameName == "":
                return gameName

            def SetName(name: str):
                self.info['Name']['value'] = name
                self.info['Name']['colour'] = Fore.GREEN
                return gameName

            if gameName not in self.getGameList():
                return SetName(gameName)

            randomEnd = ''
            for _ in range(10):
                randomEnd += random.choice(string.ascii_letters)

            self.chk.getInput(
                f"Game already exists in location. Rename to {gameName}_{randomEnd}?: ",
                self.chk.ModeEnum.yesno,
                y=SetName, yA=f'{gameName}_{randomEnd}'
            )

    def __nameCheck(self, name: str, old: str, other: str = None):
        name = name.rstrip()
        newName = name

        # Use system name if 'me'
        if name.lower()[:2] == 'me':
            newName = getpass.getuser()
            if name[2:] != '':
                newName += '({})'.format(name[2:])

        # check for blank
        if name == '':
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
        oldUsers = [
            self.getInfoFieldValue('Players', 'Player 1'),
            self.getInfoFieldValue('Players', 'Player 2')
        ]
        usernames = [None, None]

        # loop
        for i in range(2):
            while usernames[i] is None:
                # get the last name
                pastName = None
                pastNameText = ''
                if i >= 1:
                    pastName = usernames[i - 1]
                    pastNameText = pastName + ', '

                # Move cursor and stuff
                print("\033[%d;%dH" % (19, 0))
                space = " " * (len(str(oldUsers)) - 1)
                print(
                    f"Please enter player {i + 1}'s name (Blank to keep same)",
                    end='')
                print("\033[%d;%dHPlayers: [{}".format(space) % (3, 0), end='')
                usernames[i] = input(
                    f"\033[%d;%dH{pastNameText}" % (3, 11))
                print("\033[%d;%dH" % (19, 0))

                # Process input
                nameResult = self.__nameCheck(usernames[i],
                                              oldUsers[i],
                                              pastName)

                # annoyed
                if not nameResult:
                    usernames[i] = None
                    print("Player {} name is not allowed!".format(i + 1))
                    continue

                # save
                usernames[i] = nameResult

        self.info['Players']['Player 1']['value'] = usernames[0]
        self.info['Players']['Player 2']['value'] = usernames[1]
        self.info['Players']['Player 1']['colour'] = Fore.GREEN
        self.info['Players']['Player 2']['colour'] = Fore.GREEN

    def size(self):
        # get the size of the game board.
        x = self.chk.getInput("Please enter X length: ",
                              self.chk.ModeEnum.int,
                              lower=5)
        y = self.chk.getInput("Please enter Y length: ",
                              self.chk.ModeEnum.int,
                              lower=5)

        self.info['Size']['X']['value'] = x
        self.info['Size']['X']['colour'] = Fore.GREEN
        self.info['Size']['X']['value'] = y
        self.info['Size']['Y']['colour'] = Fore.GREEN

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
                # automatically reset multiplayer
                self.info['Multiplayer']['value'] = "no"

            # If default, don't need to do much
            # If drive, run test
            # If external, run test

            # skip doing stuff to saves
            if Location != "Saves":
                # attmepts to write file and read file from dir specified
                # creates save obj
                try:
                    self.saveModule.Write('test', f'{Location}/test')
                    self.saveModule.RemoveFile(f'{Location}/test')
                except Exception as e:
                    PrintTraceback()
                    Location = None
                    self.msg.warn(
                        "Error occured whilst trying to change location.", 2)

        self.info['Location']['value'] = Location
        self.info['Location']['colour'] = Fore.GREEN

    def MultiPlayer(self):
        if self.getInfoFieldValue('Location') == "Saves":
            self.msg.clear(
                "Disabled! Save location is default, Please change to have multiplayer support!", timeS=2
            )
            return
        # get if multiplayer or not

        multi = self.chk.getInput(
            "Online multiplayer? (y = different devices, n = same device)",
            self.chk.ModeEnum.yesno)
        self.info['Multiplayer']['value'] = "yes" if multi else "no"

    def __setPasswordUI(self, value: str, colour: str, shown: str):
        self.info['Password']['true'] = shown
        self.info['Password']['colour'] = colour
        self.info['Password']['value'] = value

    def Password(self):
        self.__setPasswordUI(None, Fore.YELLOW, "Disabled")

        while self.info['Password']['true'] is None:
            password = getpass.getpass(
                "Enter a password (blank for no passwords): ")
            if password.rstrip() == "":
                return self.__setPasswordUI(None, Fore.YELLOW, "Disabled")

            check = None
            while check is None:
                check = getpass.getpass(
                    "Please re-enter the password (-1 to change password): ")
                if check == password:
                    self.__setPasswordUI(password, Fore.GREEN, "Disabled")
                    return True
                if check == -1:
                    self.__setPasswordUI(None, Fore.YELLOW, "Disabled")

    def check(self):
        # Checks if all fields are valid.
        # This is done because game name might relay on save location but will still let you enter it.  # noqa E051

        if self.getInfoFieldValue('Name') is None:
            self.msg.clear("Please enter a name!", 2)
            return "Name"

        users = [
            self.getInfoFieldValue('Players', 'Player 1'),
            self.getInfoFieldValue('Players', 'Player 2')
        ]

        if any(user is None for user in users):
            self.msg.clear("Please enter player names!", 2)
            return "Username"

        if any(['/' in user or '\\' in user for user in users]):
            self.msg.clear("Usernames cannot have '/' or '\\' in!", 2)
            return "Invalid Name"

        # Password better than no password, Check
        if self.info.get('Password').get('true') is None:
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
        password = self.info.get('Password').get('true')
        if password is not None:
            check = getpass.getpass(
                "Please enter the password to save the game: ")
            if check != password:
                self.msg.clear(
                    "Please make sure you can remember the password", 2)
                return False

        # Create board
        board = Board.CreateBoard(self.getInfoFieldValue('Size', 'X'),
                                  self.getInfoFieldValue('Size', 'Y'))

        # Create folder for the game
        gameLoc = f'{self.getInfoFieldValue("Location")}/{self.getInfoFieldValue("Name")}'
        self.saveModule.MakeFolders(gameLoc)

        users = [
            self.getInfoFieldValue('Players', 'Player 1'),
            self.getInfoFieldValue('Players', 'Player 2')
        ]

        placed = ShipInfo.getDefaultPlaced()
        for user in users:
            # create user data
            userLoc = f'{gameLoc}/{user}'
            self.saveModule.MakeFolders(userLoc)
            self.saveModule.Write(board, f'{userLoc}/ships',
                                  encoding=self.saveModule.encoding.BINARY)
            self.saveModule.Write(placed, f'{userLoc}/placedData',
                                  encoding=self.saveModule.encoding.BINARY)

        # make turn file, notes whos turn it is.
        data = {
            'turn': self.getInfoFieldValue('Players', f'Player {random.randrange(2) + 1}'),
            'multi': self.getInfoFieldValue('Multiplayer'),
            'password': self.getInfoFieldValue('Password'),
            'size': [self.getInfoFieldValue('Size', 'X'),
                     self.getInfoFieldValue('Size', 'Y')],
        }
        self.saveModule.Write(data, f'{gameLoc}/GameData',
                              encoding=self.saveModule.encoding.BINARY)

        return "Save"  # success!!!


if __name__ == '__main__':
    c = CreateData("Saves")
    result = c.getOption()
    # print(result)
