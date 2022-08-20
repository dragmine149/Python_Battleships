import importlib
import time
import os
import traceback
import glob

Settings = importlib.import_module('Files.Settings')
Save = importlib.import_module('Files.Save')
colours = importlib.import_module('Files.colours')
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# set import from colours (from colours import Print)
Print = colours.Print


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
    saveLocation = Save.save({
        'path': path
    })
    api = saveLocation._api

    try:
        games = saveLocation.ls()
    except FileNotFoundError:
        return []

    # skips loop if empty
    if len(games) == 0:
        return []

    newlist = []
    BannedList = ['.Temp', 'multi',' turn', 'win']
    for folder in games:
        # Removes non directories
        if isinstance(folder, dict):
            folder = folder['name']
        
        if not folder.startswith(".") and not folder.startswith("__") and folder not in BannedList:
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
        if Settings.request(['clear'])[0]:
            # This clears the terminal without deleting the logs.
            print("\x1b[2J\x1b[H", end='')
        else:
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
            # inclusive of 2 end values
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

        # TODO: Find a way to update the values if the list of options
        #     : has changed.

        # check if any extra information to show
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
        if self.__input == '':
            clear(2, "Invalid input, please enter y or n!", "red")
            return "Invalid"
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

        try:
            # unknown check
            if callable(self._returnFunc[2]):
                return self._returnFunc[2]()
            return self._returnFunc[2]
        except (KeyError, IndexError):  # if we only supply 2 arguments
            warn(2, "Invalid input, please enter y or n!", "red")
            return "Invalid"

    def getInput(self, check="Int"):
        while not self.__input:
            # gets inputs
            self._CallExtra()  # show information as needed
            self.__input = input(str(self._request)).strip()

            # sorts out inputs
            if check == "Int":
                self.__input = self._IntCheck()
                if self.__input is not None:
                    return self.__input

            if check == "ynCheck":
                result = self._ynCheck()
                if result == "Invalid":
                    self.__input = None
                    continue
                return result


# Everything to do with the board. Prints it and creates it.
class board:
    @staticmethod
    def CreateBoard(size):
        board = []
        for _ in range(size[1]):  # Y size (height)
            x = []
            for _ in range(size[0]):  # X size (width)
                x.append('-')
            board.append(x)
        return board

    @staticmethod
    def DisplayBoard(board, text):
        print("  {}{}{}".format(colours.c('funderline'),
                                text[0:10],
                                colours.c()))
        print("  ABCDEFGHIJ")  # Easy to know where the square is
        for y in range(len(board)):

            yIndex = str(y + 1)
            if len(yIndex) == 1:
                yIndex = "0" + yIndex
            print(yIndex, end="")

            for x in board[y]:
                print(x, end="")
            print()

    @staticmethod
    def MultiDisplay(boards=[], text=[]):
        if len(boards) < 2 or len(boards) > 3:
            return

        msg = "  {}{}{}\t\t\t  {}{}{}\n".format(colours.c('funderline'),
                                                text[0][0:10],
                                                colours.c(),
                                                colours.c('funderline'),
                                                text[1][0:10],
                                                colours.c())
        msg += "  ABCDEFGHIJ\t\t\t  ABCDEFGHIJ"
        msg += "\t\t\t{}Opponent shots{}".format(colours.c('funderline'), colours.c()) if len(boards) == 3 else ""
        print(msg)
        lines = []
        for _ in range(len(boards[0])):
            lines.append("")

        maxRange = len(boards)

        for i in range(maxRange):
            for y in range(len(boards[i])):

                yIndex = str(y + 1)
                if len(yIndex) == 1:
                    yIndex = "0" + yIndex
                lines[y] += yIndex

                for x in boards[i][y]:
                    lines[y] += x

            for line in range(len(lines)):
                lines[line] += "\t\t\t"

        for line in lines:
            print(line)


class search:
    """
    directory -> where to start search
    target -> what to search for (Supports '()' arrays (tuples))
    layers -> How many directories above the current directory to search.
              Default 2: '../../../'
    sti -> how long to wait between messages and stuff, just for fun.
           Recommendation don't add if you want speed.
    """
    def __init__(self, directory, target, layers=2, sti=0):
        self.directory = directory
        self.target = target
        self.searched = ''
        self.layers = layers
        self.sti = sti
        self.__FoundList = []

    def Locate(self):
        self.__searchDirectory(self.directory)
        return self.__FoundList

    def __FindFile(self, directory, file):
        # Using glob, finds files with `directory/file`
        files = glob.glob(os.path.join(directory, file))
        self.__FoundList.extend(files)

    """
    __searchDirectory(self, directory, sub)
    - Searches for a file in directory
    Loops though pretty much the whole fs until the file is found.
    Goes up directories, down into directories and more!
    """
    def __searchDirectory(self, directory, sub=False):
        if self.layers > 0:
            fileText = "file"
            if isinstance(self.target, tuple) and len(self.target) > 1:
                fileText = "files"
            Print('Searching Dir: "{}". Target {}: "{}"'.format(directory, fileText, self.target), "green") # noqa E501
            time.sleep(self.sti)  # makes it look cool

            # checks if in current directory, returns if it is.
            if isinstance(self.target, tuple):
                for file in self.target:
                    self.__FindFile(directory, file)

            # get files in current directory and remove the folder the user
            # just came out of (doesn't search the folder again)
            try:
                files = os.listdir(directory)
            except PermissionError:
                Print('Missing permissions for for {}'.format(directory), "red", "bold")  # noqa E501
                return

            # Skip over directory we just came out of
            if self.searched in files:
                files.remove(self.searched)

            # loops though all the files
            for file in files:
                time.sleep(self.sti)
                Print('Looking at {}'.format(file), "yellow")
                # Skips the folder if it's a well know not going to have files.
                if file == ".git":
                    print(".git, no just no.")
                    continue
                
                if file == self.target:
                    self.__FoundList.append(os.path.join(directory, file))

                # checks if the folder is a directory
                newFile = os.path.join(directory, file)
                if os.path.isdir(newFile):
                    self.__searchDirectory(newFile, True)  # noqa E501

            # if sub directory, don't go back up 1 directory.
            if not sub:
                self.searched = os.path.basename(os.path.abspath(directory))
                self.layers -= 1
                self.__searchDirectory(os.path.abspath(os.path.join(directory, '../')))  # noqa


def LocationTest(Location):
    try:
        saveInfo = Save.save({
            'name': 'Test',
            'path': Location,
        })
        print({'saveInfo vars': vars(saveInfo)})

        # Creates test folder
        folder = saveInfo.makeFolder()
        print({'folder': folder})
        
        saveInfo.ChangeDirectory(folder)

        # creates file
        savedLocation = saveInfo.writeFile("This is a test file", "Test")
        print({'savedLocation': savedLocation})

        # reads file from same place
        data = saveInfo.readFile("Test")
        print({'data': data})

        if data != "This is a test file":
            # Oh oh, doesn't work... Return error
            clear(3, "Please make sure that this program has read and write ability to {}".format(Location))  # noqa
            Location = None

        print("Folder to delete: {}".format(folder))
        print(saveInfo.GetPath())
        deletion = saveInfo.Delete(folder)
        # deletion2 = saveInfo.delete('Saves/.Temp/Test')
        print({'deletion': deletion})
        # print({'deletion2': deletion2})

        return True, saveInfo._api
    except Exception:
        PrintTraceback()
        return False, False


def IsDigit(var):
    """
    Better version of .isdigit but works with negatives.
    """

    # Skips the check if None is inputted
    if var is None:
        raise AttributeError("'NoneType' object has no attribute 'isdigit'")

    # returns true if interger
    if isinstance(var, int):
        return True

    var = str(var)  # make sure it's a string if the int check failed

    # Checks to see if negative or not
    try:
        # Removes negative
        var = var.replace("-", "")

        # gets where the decimal is
        decimalLocation = False

        # 2 items on split
        if len(var.split('.')) == 2:
            decimalLocation = var.index('.')

        # 1 item on split
        if len(var.split('.')) == 1:
            return var.isdigit()

        # Too many items on split (not 1 or 2)
        if decimalLocation is False:
            print('Too many decimals found!')
            return False

        # Final thing to return (if contains decimal)
        var1 = var[:decimalLocation].isdigit()
        var2 = var[decimalLocation + 1:].isdigit()
        return var1 and var2
    except IndexError as ie:  # if error, return false
        print("IndexError: {}".format(ie))
        return False


def tests():
    # Run a series of tests for all things
    r1 = LocationConvert('A1').Convert()
    r2 = RemoveNonGames('.')
    r5 = board.CreateBoard([10, 10])
    print(r1)
    print(r2)
    print(r5)
    assert True
    return True


# lets the user select the path of where to view the games
def changePath():
    games = None
    path = None
    external = None
    apiExternal = None
    clear()
    while not external:
        try:
            external = input("Please enter location of storage (leave blank to reset, Keyboard Interrupt to reset input): ").rstrip().replace('"', '')  # noqa
            if external != "" and external != "Saves":  # external being equal to saves in annoying.
                # Windows has different file structure AAA
                if os.name != "nt":
                    external = external.replace("\\", "")  # noqa

                # test and tells us
                result = LocationTest(external)
                print(result)
                print(result[0])
                print(result[1])
                if result[0]:
                    print("Success!")
                    # set the path to the new external location
                    path = external

                    # tells the code to use different location
                    if result[1]:
                        apiExternal = True

                        # get the files
                        games = Save.save({
                            'path': external
                        }).ls()
                        games = games

                        # checks if there is game data
                        if games is None:
                            external = None
                            path = "Saves"
                            clear(2, "No games found in desired location!")  # noqa E501
                            continue
                        return games, path, apiExternal
                
                    apiExternal = False
                    games = path
                    return games, path, apiExternal
                
                print("Error!")
                # break if error in stuff
                external = None
                games = None
                path = None
                apiExternal = None
                clear(1, "Failed to find folder!", "red")
                break
                
            path = "Saves"
            games = "Saves"
            apiExternal = False
            return games, path, apiExternal

        # Easy way to redo just in case mess up.
        except KeyboardInterrupt:
            external = None
            clear()


def PrintTraceback():
    print('\033[41m----')
    traceback.print_exc()
    print('----\033[0m')


# Prints a message out with a timer whilst waiting
def waiting(message):
    time = Settings.request(["CheckTimeout"])[0]
    # Waits for the opponent.
    try:
        back = "(ctrl + c to go back)"
        dots = ''
        for _ in range(0, time + 1):
            print("{}{} {}".format(message, dots, back), end="\r")
            dots += '.'
            time.sleep(1)
    except KeyboardInterrupt:
        return "Back"


if __name__ == "__main__":
    # result = search('.', 'credentials.json').Locate()
    # print({'result': self.input})
    tests()
