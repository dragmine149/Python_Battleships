import time
import SaveSystem as save
import Functions


class create:
    def __init__(self):
        self.name = None
        self.users = None
        self.Placed = None
        self.twoPlayer = None

    @staticmethod
    def SizeRangeCheck(size):
        # replace with amount of ships in game.
        if size >= 5:  # got to be big enough to hold all ships
            return True
        return False

    # Function to process user inputs
    def _ProcessChoice(self, data=[True, None], infoData=None):
        # Creates a new game.
        # get the size
        x, y = None, None
        while x is None:
            x = Functions.check("Please enter X size (length): ", None, None, self.SizeRangeCheck).InputDigitCheck(data[0], data[1])  # noqa
        while y is None:
            y = Functions.check("Please enter Y size (length): ", None, None, self.SizeRangeCheck).InputDigitCheck(data[0], data[1])  # noqa
        GameBoard = save.board.CreateBoard([x, y])  # creates a board
        create = None
        name = False
        while not create:  # saves the board
            # uses default otherwise gets inputs
            if not name:
                self.name = infoData[0]
            else:
                self.name = input("Please enter a name for this game: ").replace(" ", "")  # noqa

            self.users = infoData[1]
            create = save.save(self.saveLocation).saveCreation(GameBoard, self.name, self.users, self.twoPlayer) # noqa
            if create == "E":
                create = None
                name = True

    def setup(self, data=[True, None], infoData=None):
        if infoData is None:
            infoData = [
                input("Please enter a name for this game: ").replace(" ", ""),
                [
                    str(input("Please enter player 1's name: ").replace(" ", "")),  # noqa
                    str(input("Please enter player 2's name: ").replace(" ", ""))  # noqa
                ]
            ]
            self.saveLocation = input("Custom Save Location (blank = default, Id = google drive folder id): ")  # noqa
            if self.saveLocation == "":
                self.saveLocation = "Saves"
            else:
                while not self.twoPlayer:
                    self.twoPlayer = input("Are you playing online? (y = yes, n = no): ")  # noqa
                    if self.twoPlayer[0].lower() == "y":
                        self.twoPlayer = infoData[1][0]

        Functions.clear()
        # Process choice
        self._ProcessChoice(data, infoData)
        time.sleep(1)
        return self.name, self.users, False, self.saveLocation, self.twoPlayer
