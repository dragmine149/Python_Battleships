import getpass
import shutil
import string
import random
from colorama import Fore
from PythonFunctions.PrintTraceback import PrintTraceback
from PythonFunctions.CleanFolderData import Clean
from PythonFunctions.Watermark import LINKCODE
from PythonFunctions.Check import Check
from PythonFunctions.Save import save
from PythonFunctions import Board, Message, cursor, SPACE, lenstr, n, clearLine
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
        self.chk = Check()
        self.cln = Clean()
        self.saveModule = save()

    def SetDefaults(self, name, users, sizeX, sizeY, Multi):
        # Perpare screen for information later on
        Message.clear()
        self.showOptions()

        if name is not None:
            self.name(name)
        if users is not None:
            self.username(users)
        self.size(sizeX, sizeY)
        self.MultiPlayer(Multi)
        print('Defaults have been set')

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
        value = data.get('value')
        if value is not None:
            return f"{setting}: {data.get('colour')}{value}{Fore.RESET}"

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
        print('-' * shutil.get_terminal_size().columns)
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
                4: self.SaveLocation,
                5: self.MultiPlayer,
                6: self.Password,
                7: self.save
            }
            Message.clear()

            self.showOptions()
            choice = self.chk.getInput("What would you like to change?: ",
                                       self.chk.ModeEnum.int,
                                       lower=0, higher=7, clear=False)

            result = options.get(choice)()
            if result == "Save":
                return

    def name(self, passedName: str = None) -> str:
        gameName = None
        while gameName is None:
            gameName = passedName
            if passedName is None:
                print("Please enter the game name (blank to keep same)")
                gameName = input(f"\033[{2};{7}H")
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

            newName = f'{gameName}_{randomEnd}'
            self.chk.getInput(
                f"Game already exists in location. Rename to {newName}?: ",
                self.chk.ModeEnum.yesno,
                y=SetName, yA=newName
            )

    def __nameCheck(self, name: str, old: str, other: str = None):
        if name is None:
            return name

        name = name.rstrip()
        newName = name

        # Use system name if 'me'
        if name.lower()[:2] == 'me':
            newName = getpass.getuser()
            if name[2:] != '':
                newName += f'({name[2:]})'

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

    def username(self, users: list[str] = None) -> None:
        def checkName(name, old, other=None) -> str:
            name: str = self.__nameCheck(name, old, other)
            name = n(None, name, name, False)
            return name

        if users is None:
            users = [None, None]

        oldusers = [self.getInfoFieldValue('Players', 'Player 1'),
                    self.getInfoFieldValue('Players', 'Player 2')]

        puser: str = None
        for i, olduser in enumerate(oldusers):
            newuser: str = checkName(users[i], olduser, puser)
            while newuser is None:
                cursor(19, 0)
                print(
                    f'Please enter player {i + 1} name (blank to keep same)',
                    end='')
                clearLength = SPACE * lenstr(oldusers, -1)
                print(
                    f'{cursor(3, 0, True)}Players: [{clearLength}',
                    end='')

                newuser = input(
                    f'{cursor(3, 11, True)}{n(puser, "")}{n(",", "", i, 1)}')
                newuser = checkName(newuser, olduser, puser)
                cursor(19, 0)

            if i == 0:
                puser = newuser

            self.info['Players'][f'Player {i + 1}'].update(
                value=newuser, colour=Fore.GREEN)

    def size(self, x: int = None, y: int = None):
        x = n(x, x, v2=str(x))
        x = n(y, y, v2=str(y))

        print(f"{cursor(4, 0, True)}{clearLine(True)}")
        cursor(19, 0)
        # get the size of the game board.
        x = self.chk.getInput(
            f"Please enter X length {cursor(4, 0, True)}Size: [",
            self.chk.ModeEnum.int,
            lower=5, vCheck=x)

        cursor(19, 0)
        y = self.chk.getInput(
            f"Please enter Y length {cursor(4, 0, True)}Size: [{x}, ",
            self.chk.ModeEnum.int,
            lower=5, vCheck=y)
        cursor(19, 0)

        self.info['Size']['X']['value'] = x
        self.info['Size']['X']['colour'] = Fore.GREEN
        self.info['Size']['Y']['value'] = y
        self.info['Size']['Y']['colour'] = Fore.GREEN

    def SaveLocation(self):
        Location = None
        while Location is None:
            fss = LINKCODE(
                ('https://python-functions.readthedocs.io/en/latest/' +
                    'Modules/Save.html#file-system-support'),
                'File System Support')
            print(f"""Enter save location
NOTE: Multiple types of file systems are supported. use FILESYSTEM://LOCATION
Please check out {fss} for more information about supported filesystems
To return to the default save location, use: ~/r!""")

            # Move curosr
            cursor(5, 0, end='')
            result, Location = self.chk.getInput("Location: ",
                                                 self.chk.ModeEnum.path,
                                                 rCheck=True)
            if Location == '~/r!':
                enc = [self.saveModule.encoding.JSON,
                       self.saveModule.encoding.BINARY]
                Location = self.saveModule.Read('Data/Settings',
                                                encoding=enc).get('path')

            if result is False:
                continue

            try:
                self.saveModule.Write('test', f'{Location}/test')
                self.saveModule.RemoveFile(f'{Location}/test')
            except (FileNotFoundError, OSError):
                PrintTraceback()
                Message.warn(
                    "Error occured whilst trying to change location.",
                    timeS=2)
                Location = None

        self.info['Location']['value'] = Location
        self.info['Location']['colour'] = Fore.GREEN

    def MultiPlayer(self, Multiplayer: bool = None):
        if self.getInfoFieldValue('Location') == "Saves":
            Message.clear(
                "Save location is default. Multiplayer is disabled!",
                timeS=2
            )
            return
        # get if multiplayer or not

        multi = Multiplayer
        if Multiplayer is None:
            multi = self.chk.getInput(
                "Online multiplayer? (y = different devices, n = same device)",
                self.chk.ModeEnum.yesno)

        self.info['Multiplayer']['value'] = "yes" if multi else "no"

    def __setPasswordUI(self, value: str, colour: str, shown: str):
        self.info['Password']['true'] = value
        self.info['Password']['colour'] = colour
        self.info['Password']['value'] = shown

    def Password(self):
        self.__setPasswordUI(None, Fore.YELLOW, "Disabled")
        while self.info.get('Password').get('true') is None:
            password = getpass.getpass(
                "Enter a password (blank for no passwords): ")
            if password.rstrip() == "":
                return self.__setPasswordUI(None, Fore.YELLOW, "Disabled")

            check = None
            while check is None:
                check = getpass.getpass(
                    "Please re-enter the password (-1 to change password): ")
                if check == password:
                    self.__setPasswordUI(password, Fore.GREEN, "Enabled")
                    return True
                if check == -1:
                    self.__setPasswordUI(None, Fore.YELLOW, "Disabled")

    def check(self):
        # Checks if all fields are valid.

        if self.getInfoFieldValue('Name') == 'None':
            Message.warn("Please enter a name")
            return "Name"

        users = [
            self.getInfoFieldValue('Players', 'Player 1'),
            self.getInfoFieldValue('Players', 'Player 2')
        ]

        if any(user == 'None' for user in users):
            Message.warn("Please check players name. (Someone has 'None')")
            return "Username"

        if any(('/' in user or '\\' in user for user in users)):
            Message.clear("Usernames cannot have '/' or '\\' in!", timeS=2)
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
            Message.clear("Please check settings", timeS=2)
            return False

        # Get the user to enter the password to save
        password = self.info.get('Password').get('true')
        if password is not None:
            check = getpass.getpass(
                "Please enter the password to save the game: ")
            if check != password:
                Message.clear(
                    "Please make sure you can remember the password", timeS=2)
                return False

        # Create board
        board = Board.CreateBoard(self.getInfoFieldValue('Size', 'X'),
                                  self.getInfoFieldValue('Size', 'Y'))

        # Create folder for the game
        loc = self.getInfoFieldValue("Location")
        name = self.getInfoFieldValue("Name")
        gameLoc = f'{loc}/{name}'
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
        turn = random.randrange(2) + 1
        data = {
            'turn': self.getInfoFieldValue('Players', f'Player {turn}'),
            'multi': self.getInfoFieldValue('Multiplayer'),
            'password': self.info.get('Password').get('true'),
            'size': [self.getInfoFieldValue('Size', 'X'),
                     self.getInfoFieldValue('Size', 'Y')],
        }
        self.saveModule.Write(data, f'{gameLoc}/GameData',
                              encoding=self.saveModule.encoding.BINARY)

        return "Save"  # success!!!
