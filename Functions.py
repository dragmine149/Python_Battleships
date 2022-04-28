import time
import os
import platform
import Save as save
os.chdir(os.path.dirname(os.path.realpath(__file__)))


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
        else:
            clear(1, "Must be at least two digits, a letter (x) and a number (y)")  # noqa
            return None, None


# Remove games that begin with '.' or '__' or are not directoies at all.
# TODO: Better hidden folder check
def RemoveNonGames(path="Saves"):
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


# Checks if a number is within 0 and another value.
def NumberRangeCheck(value, x):
    if value >= 0 and value <= x:
        return True
    return False


# Clears the console with a message before clear.
def clear(timeS=0, message=None):
    if message:
        print(message)
    time.sleep(timeS)
    # Windows doesn't have 'clear' so having to use the other option.
    # Mac / Linux doesn't have 'cls' same issue as windows
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


# Check if the input is a valid input using a whole bunch of data
class check:
    """
    request -> String
        - What you want to ask the user
    extra -> String / function
        - Any extra information you want to display to the user
    extraValue -> value
        - Information that the function needs
    rangeCheck -> function
        - A callable function that checks if the input is within 2 digits
    rangeCheckValue -> Interager
        - The other digit for the range check
    """

    def __init__(self, request, extra=None, extraValue=None, rangeCheck=None, rangeCheckValue=None):  # noqa
        self.request = request
        self.extra = extra
        self.extraValue = extraValue
        self.rangeCheck = rangeCheck
        self.rangeCheckValue = rangeCheckValue
        self.Id = None
        self.check = None

    def _PassCheck(self):
        # Checks to see if the value is okay
        self.Id = int(self.Id)
        if self.rangeCheck is not None:  # checks if in certain range
            # A lot of checks to call a function or not
            if callable(self.rangeCheck):
                if self.rangeCheckValue is None:
                    self.check = self.rangeCheck(self.Id)
                else:
                    if callable(self.rangeCheckValue):
                        self.check = self.rangeCheck(self.Id, self.rangeCheckValue())  # noqa
                    else:
                        self.check = self.rangeCheck(self.Id, self.rangeCheckValue)  # noqa

                if self.check:
                    return self.Id
                else:
                    if self.Id == -1 or self.Id == -2:
                        return self.Id
                    clear(1, "Out of range.")
                    self.Id = None
                    return None
            else:
                print("ERROR, range check is not a function!")
                return self.Id
        else:
            return self.Id

    def _FailCheck(self):
        # user notification
        clear(1, "Please enter a valid input")
        self.Id = None

    def _CallExtra(self):  # repeats any information the user needs to know
        if self.extra is not None:
            if callable(self.extra):
                if self.extraValue is None:
                    self.extra()  # call function
                else:
                    self.extra(self.extraValue)
            else:
                print(self.extra)

    def InputDigitCheck(self):  # noqa
        while not self.Id:
            self._CallExtra()
            self.Id = input("{}".format(self.request))  # get input
            try:
                int(self.Id)
                return self._PassCheck()
            except ValueError:
                self._FailCheck()


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
                return data

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


if __name__ == "__main__":
    data = userData("Saves", "Test", "me")
    data.getBoard()
