import time
import os
import newSave
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class Print:
    """
    Colours:
    foreground : {
        black, red, green, orange, blue, purple, cyan, light grey, dark grey,
        light red, light green, yellow, light blue, pink, cyan
    }
    background : {
        black, red, green, orange, blue, purple, cyan, light grey
    }
    options = [
        reset, bold, disable, underline, reverse, strikethrough, invisible
    ]
    """

    def __init__(self, msg, colour=[None, None], options=[
        None, None, None, None, None, None, None
    ]):
        self.msg = msg

        # gets the colour and checks it
        self.colour = self.__ColourCheck(colour)
        self.options = options
        if not self.colour:
            # print if no colour, saving time
            print(msg)
        else:
            # print with colour
            self.__defineColours()
            self.__output()

    def __ColourCheck(self, colour):
        if colour is None:  # if none, return
            return False
        if isinstance(colour, list):
            if len(colour) > 2:  # if more than 2, shrink
                return colour[0:1]
            if len(colour) == 2:
                # only care if they are both none
                if colour[0] is None and colour[1] is None:
                    return False
                return colour
            # assume foreground
            if len(colour) == 1:
                return [colour[0], None]
        return [colour, None]

    def __getOptionValues(self):
        optStr = ''
        _FormatOptions = [
            'reset',
            'bold',
            'disable',
            'underline',
            'reverse',
            'strikethrough',
            'invisible'
        ]
        # checks if string
        if isinstance(self.options, str):
            if self.options in _FormatOptions:
                return self._format[self.options]

        # loops through and get all the options
        for option in self.options:
            if option in _FormatOptions:
                optStr += self._format[option]
        return optStr

    def __output(self):
        # Take colour and message and print them correctly
        colourValues = ['', '']

        # get the foreground colour value
        for i in range(2):
            if self.colour[i] is None:
                colourValues[i] = ''
                break

            # background and foreground colour set
            try:
                colourValue = self.colour[i].lower()
                if i == 0:
                    colourValues[i] = self._colours['fg'][colourValue]
                if i == 1:
                    colourValues[i] = self._colours['bg'][colourValue]

            except KeyError:
                colourValues[i] = ''  # don't include one if not present
            except AttributeError:
                colourValue[i] = ''

        # print out colours
        print('{}{}{}{}'.format(self.__getOptionValues(),
                                colourValues[0],
                                colourValues[1],
                                self.msg),
              end='')  # no end so it reset bg colour as well

        # reset to normal afterwards
        print(self._format['reset'])

    def __defineColours(self):
        # defines the colours and what they do
        self._format = {
            'reset': '\033[0m',
            'bold': '\033[01m',
            'disable': '\033[02m',
            'underline': '\033[04m',
            'reverse': '\033[07m',
            'strikethrough': '\033[09m',
            'invisible': '\033[08m',
        }
        self._colours = {
            'fg': {
                'black': '\033[30m',
                'red': '\033[31m',
                'green': '\033[32m',
                'orange': '\033[33m',
                'blue': '\033[34m',
                'purple': '\033[35m',
                'cyan': '\033[36m',
                'light grey': '\033[37m',
                'dark grey': '\033[90m',
                'light red': '\033[91m',
                'light green': '\033[92m',
                'yellow': '\033[93m',
                'light blue': '\033[94m',
                'pink': '\033[95m',
                'light cyan': '\033[96m'
            },
            'bg': {
                'black': '\033[40m',
                'red': '\033[41m',
                'green': '\033[42m',
                'orange': '\033[43m',
                'blue': '\033[44m',
                'purple': '\033[45m',
                'cyan': '\033[46m',
                'light grey': '\033[47m'
            }
        }


# Converts the input to a valid location (a1 -> [0,0])
class LocationConvert:
    def __init__(self, value):
        self.input = value
        self.letters = ""
        self.y = ""

    # Thanks to Guy_732
    # changes letter to number based in the alphabet
    def _decode(self, s: str) -> int:
        s = s.lower()
        ref = ord('a') - 1
        v = 0
        exp = 1
        for c in reversed(s):
            v += (ord(c) - ref) * exp
            exp *= 26

        return v

    def Convert(self):
        if len(self.input) >= 2:
            # lower input
            self.input = self.input.lower()
            # splits the input into numbers and letters
            for v in self.input:
                if v.isdigit():
                    self.y += v
                else:
                    self.letters += v
            if self.letters == self.input:
                clear(1, "Must be at least two digits, a letter (x) and a number (y)")  # noqa
                return None, None
            # convert letters into numbers
            return self._decode(self.letters) - 1, (int(self.y) - 1)
        clear(1, "Must be at least two digits, a letter (x) and a number (y)")  # noqa
        return None, None


# Remove games that begin with '.' or '__' or are not directoies at all.
# TODO: Better hidden folder check
def RemoveNonGames(path="Saves"):
    # returns empty if nothing put in.
    if path is None:
        return []
    games = None
    api = False
    if isinstance(path, list):
        api = True
        games = path
    else:
        try:
            games = os.listdir(path)
        except FileNotFoundError:
            return []

    newlist = []
    for folder in games:
        # Removes non directories
        """ WINDOWS ALERT!!! # noqa E501
        So, after doing some testing on windows, i noticed a file called 'desktop.ini'
        This file is hidden and thankfully is at the end of the list but still needs
        to be removed. I could add a list of hidden files and check for them but would
        rather not do that to save time and stuff.
        """
        if not api:
            if os.path.isdir(os.path.join(path, folder)):
                if not folder.startswith(".") and not folder.startswith("__"):
                    if folder != ".Temp":  # Remove google files
                        newlist.append(folder)
        else:
            folder = folder['name']
            if not folder.startswith(".") and not folder.startswith("__"):  # noqa
                # Get more information from google Better check.
                if not folder.lower() == "multi" and not folder.lower() == "turn" and not folder.lower() == "win":  # noqa
                    newlist.append(folder)
    return newlist


def __messageSort(timeS=0, message=None, clear=False, colour=[None, None]):
    if isinstance(timeS, str):
        Print("Automatically fixed error! `timeS` was string instead of number!", 'light red')  # noqa E501
        time.sleep(2)  # force wait
        message = timeS
        timeS = 2  # default time, 2 seconds for message

    if message:
        Print(message, colour)
    time.sleep(timeS)
    # Windows doesn't have 'clear' so having to use the other option.
    # Mac / Linux doesn't have 'cls' same issue as windows
    if clear:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")


# Clears the console with a message before clear.
def clear(timeS=0, message=None, colour=[None, None]):
    __messageSort(timeS, message, True, colour)


# does the same as clear, just doesn't clear it.
def warn(timeS=2, message=None, colour=[None, None]):
    __messageSort(timeS, message, False, colour)


# Check if the input is a valid input using a whole bunch of data
class check:
    """
    request -> String
        - What you want to ask the user
    extra -> (function, value)
        - What you want to show the user. function arg can be string
    rangeCheck -> (value, value)
        - The 2 numbers to compair the input with
        - INT CHECK ONLY
    returnFunc -> (function, function, function)
        - what happens after completion of running
        - Yes No Check ONLY
    """
    __slots__ = ("__input", "_request", "_extra", "_rangeCheck", "_returnFunc")

    def __init__(self, request,
                 extra=(None, None),  # function, value
                 rangeCheck=(None, None),  # value, value
                 returnFunc=(None, None, None)  # function, function, function
                 ):
        self._request = request
        self._extra = extra
        self._rangeCheck = rangeCheck  # int check
        self._returnFunc = returnFunc  # ynCheck

        self.__input = None

    def _IntCheck(self):
        if self._rangeCheck[0] is None or self._rangeCheck[1] is None:
            clear(1, "INVALID INPUT No values to check between", ['red'])
            return "qiagho"  # try using this lol
        # Checks to see if the value is okay
        if IsDigit(self.__input):
            self.__input = int(self.__input)
            # inclusive of 2 end values
            if self.__input >= self._rangeCheck[0]:
                if self.__input <= self._rangeCheck[1]:
                    return self.__input
                clear(1, "Out of range. (above max value: {})".format(self._rangeCheck[1]), [None, 'red'])  # noqa E501
                return None
            clear(1, "Out of range. (below min value: {})".format(self._rangeCheck[0]), [None, 'red'])  # noqa E501
            return None
        self._FailCheck()

    def _FailCheck(self):
        # user notification
        clear(1, "Please enter a valid input", 'light red')
        self.__input = None

    def _CallExtra(self):  # repeats any information the user needs to know
        # check if any extra information to show
        if self._extra is not None:
            function = self._extra
            functionVars = None

            # checks if function can be called
            if callable(function):
                return function()

            # checks for more info
            if len(self._extra) == 2:
                if self._extra[0] is None and self._extra[1] is None:
                    return
                function = self._extra[0]
                functionVars = self._extra[1]

            # tries again
            if callable(function):
                if functionVars is not None:
                    return function(functionVars)
                return function()

            print(function)
            return

    def _ynCheck(self):
        # remove all spaces, make lower, get first character
        self.__input = self.__input[0].replace(" ", "").lower()

        # yes check
        if self.__input == "y":
            if callable(self._returnFunc[0]):
                return self._returnFunc[0]()
            return self._returnFunc[0]

        # no check
        if self.__input == "n":
            if callable(self._returnFunc[1]):
                return self._returnFunc[1]()
            return self._returnFunc[1]

        # unknown check
        if callable(self._returnFunc[2]):
            return self._returnFunc[2]()
        return self._returnFunc[2]

    def getInput(self, check="Int"):
        while not self.__input:
            # gets inputs
            self._CallExtra()  # show information as needed
            self.__input = input(str(self._request))

            # sorts out inputs
            if check == "Int":
                self.__input = self._IntCheck()
                if self.__input is not None:
                    return self.__input

            if check == "ynCheck":
                return self._ynCheck()


# Everything to do with the board. Prints it and creates it.
class board:
    def CreateBoard(size):
        board = []
        for _ in range(size[1]):  # Y size (height)
            x = []
            for _ in range(size[0]):  # X size (width)
                x.append('-')
            board.append(x)
        return board

    def DisplayBoard(board):
        for y in board:
            for x in y:
                print(x, end="")
            print()


# Gets board information
# This function is annoying with the ammount of checks and stuff
# Rewrite to be better, quicker and more comments to understand what i did.
class boardRetrieve:
    def __init__(self, user, saveLocation, game, name):  # noqa
        self.user = user
        self.saveLocation = saveLocation
        self.game = game
        self.name = name
        self.dir = None
        foundLocation = self.saveLocation.find(self.game)
        if foundLocation != -1:
            self.saveLocation = self.saveLocation[:foundLocation - 1]
        print({
            'self.user': self.user,
            'self.saveLocation': self.saveLocation,
            'self.game': self.game,
            'self.name': self.name,
            'self.dir': self.dir
            })

    def getBoard(self):
        # Call the other class, this is temparary (works without breaking yet)
        data = userData(self.saveLocation, self.game, self.user, self.name).getBoard()  # noqa E501
        return data


class userData:
    def __init__(self, saveLocation, gameName, user, data="grid"):
        # These have to be differnet to make easier to do stuff
        # Also got to add in drive support
        self.saveLocation = saveLocation
        self.gameName = gameName
        self.user = user
        self.data = data

    def getBoard(self):
        """
        Process of getting a board
        - Find user folder
        - Find user file
        - Return request board data
        """
        userData = self.getUserFolder()
        for file in userData:
            if file == self.data:
                data = save.save(self.EndPath, True, {
                    'name': '',
                    'file': ''
                }).readFile({
                    'name': file
                })
                return data, self.EndPath

    def getUserFolder(self):
        # join together saveLocation and path
        gameData = os.path.join(self.saveLocation, self.gameName)

        # api test
        # Excepted data: Data in game Folder
        gameSaveData = save.save(gameData).ListDirectory(dir=True)

        # Checks if the data returned a folder exists for the user
        for data in gameSaveData:
            if data == self.user:
                # TODO: work with Google drive
                self.EndPath = os.path.join(self.saveLocation, self.gameName, data)  # noqa E501

                # Get user data and return it
                userData = save.save(self.EndPath).ListDirectory()
                return userData


class search:
    """
    directory -> where to start search
    target -> what to search for
    layers -> How many directories above the current directory to search.
              Default 3: '../../../' (WIP)
    sti -> how long to wait between messages and stuff, just for fun.
           Recommendation don't add.
    """
    def __init__(self, directory, target, layers=3, sti=0):
        self.directory = directory
        self.target = target
        self.searched = ''
        self.layers = layers
        self.sti = sti

    def Locate(self):
        return self.__searchDirectory(self.directory)

    """
    __searchDirectory(self, directory, sub)
    - Searches for a file in directory
    Loops though pretty much the whole fs until the file is found.
    Goings us directories, down into directories and more!
    """
    def __searchDirectory(self, directory, sub=False):
        if self.layers > 0:
            print('Searching Dir: "{}". Target file: "{}"'.format(directory, self.target)) # noqa E501
            time.sleep(self.sti)  # makes it look cool

            # checks if in current directory, returns if it is.
            targetFile = os.path.join(directory, self.target)
            if os.path.exists(targetFile):
                print("Found file: {}".format(targetFile))

                def yes():
                    return "Found!", targetFile

                def no():
                    return None

                checkResult = ynCheck(input("Is this the right file?: "), yes, no)  # noqa E501
                if checkResult is not None:
                    return checkResult

            # get files in current directory and remove the folder the user
            # just came out of (doesn't search the folder again)
            try:
                files = os.listdir(directory)
            except PermissionError:
                return
            if self.searched in files:
                files.remove(self.searched)

            # loops though all the files
            for file in files:
                time.sleep(self.sti)
                print('Looking at {}'.format(file))
                # checks if the folder / file is marked as hidden
                if file.startswith('.') or file.startswith('__'):
                    print('Hidden file')
                    continue

                # checks if the folder is not Saves, probably not there
                if file == "Saves":
                    print("Probably not here...")
                    continue

                # checks if the folder is a directory
                newFile = os.path.join(directory, file)
                if os.path.isdir(newFile):
                    result = self.__searchDirectory(newFile, True)  # noqa E501

                    # checks for the subdir and the result returned.
                    if result is not None:
                        if len(result) == 2:
                            if result[0] == "Found!" or result[0] == "Failed":
                                return result[1]

            # if sub directory, don't go back up 1 directory.
            if not sub:
                self.searched = os.path.basename(os.path.abspath(directory))
                self.layers -= 1
                return self.__searchDirectory(os.path.abspath(os.path.join(directory, '../')))  # noqa
        else:
            return "Failed!", None


def LocationTest(Location):
    saveInfo = newSave.save({
        'name': 'Test',
        'path': Location,
        'Json': False
    })
    print(vars(saveInfo))

    # Creates test folder
    folder = saveInfo.makeFolder(replace=True)
    print(folder)

    # creates file
    savedLocation = saveInfo.writeFile("This is a test file")
    print(savedLocation)

    # reads file from same place
    data = saveInfo.readFile()
    print(data)

    if data != "This is a test file":
        # Oh oh, doesn't work... Return error
        Functions.clear(3, "Please make sure that this program has read and write ability to {}".format(Location))  # noqa
        Location = None

    saveInfo.Delete(folder)

    return True, saveInfo._api


def IsDigit(var):
    # returns true if interger
    if isinstance(var, int):
        return True

    # Checks to see if negative or not
    try:
        if var[0] == '-':
            # negative
            return var[1:].isdigit()
        return var.isdigit()
    except IndexError:  # if error, return false
        return False


def tests():
    # Run a series of tests for all things
    r1 = LocationConvert('A1').Convert()
    r2 = RemoveNonGames('.')
    r5 = board.CreateBoard([10, 10])
    r6 = board.DisplayBoard(r5)
    print(r1)
    print(r2)
    print(r5)
    print(r6)
    assert True
    return True


if __name__ == "__main__":
    # result = search('.', 'credentials.json').Locate()
    # print({'result': self.input})
    tests()
