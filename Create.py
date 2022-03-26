import SaveSystem as save
import Functions


class create:
    def __init__(self):
        self.info = []
        self.save = None

    def strCheck(self, msg, info, check=None):
        name = None
        while not name:
            name = input(msg)
            if name == '':
                name = None
                Functions.clear(1, "Please enter a {}!".format(info))
            elif name == check:
                name = None
                Functions.clear(1, "Player 2's name cannot be the same as player 1!")  # noqa
            elif name.startswith('.'):
                name = None
                Functions.clear(1, "{} cannot start with '.'!".format(info))
            elif name.find(' ') > -1:
                print("Detected spaces in {}".format(info))
                reset = None
                while not reset:
                    reset = input("New {}: {} (y = yes, n = no): ".format(info, name.replace(' ', '')))  # noqa
                    if reset.lower()[0] == "n":
                        name = None
                        Functions.clear(1, "Please enter a new {}".format(info))  # noqa
                    elif reset.lower()[0] == "y":
                        return name.replace(' ', '')
                    else:
                        reset = None
                        Functions.clear(1, "Please enter 'y' or 'n'")
            else:
                return name

    def _SizeRangeCheck(self, size):
        # replace with amount of ships in game.
        if size >= 5:  # got to be big enough to hold all ships
            return True
        return False

    def intCheck(self, msg):
        iNT = None
        while not iNT:
            iNT = Functions.check(msg, None, None, self._SizeRangeCheck).InputDigitCheck()  # noqa
        return iNT

    def inputs(self):
        name = self.strCheck("Please enter a name for this game: ", "Game Name")  # noqa
        u1 = self.strCheck("Please enter player 1's name: ", "Player 1 Name")  # noqa
        u2 = self.strCheck("Please enter player 2's name: ", "Player 2 Name", u1)  # noqa
        users = [u1, u2]
        size = [
            self.intCheck("Please enter X size (length): "),
            self.intCheck("Please enter Y size (height): ")
        ]
        Location = None
        while not Location:
            Location = input("Custom save location (blank = default, Supports google drive files): ")  # noqa
            if Location == "":
                Location = "Saves"
            else:
                self.save = save.save(Location)

        online = None
        if Location != "Saves":
            while online is not None:
                online = input("Are you playing online? (y = yes, n = no): ")
                if online.lower()[0] == "y":
                    online = True
                elif online.lower()[0] != "n":
                    online = None
                    Functions.clear(1, "Please enter 'y' or 'n'")
                else:
                    online = False

        gameBoard = save.board.CreateBoard(size)
        game = None
        while game is None:
            game = self.save.saveCreation(gameBoard, name, users, online)  # noqa
            if game == "E":
                name = self.strCheck("Please enter a name for this game: ", "Game Name")  # noqa
                game = None
        return [name, users, Location, online]
