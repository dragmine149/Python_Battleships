import newSave
import Functions
import copy
import ShipInfo
import os


class Place:
    # setup the place system
    def __init__(self, name, location, user):
        self.name = name
        self.location = location
        self.user = user
        self.ships = ShipInfo.shipInfo(ShipInfo.getShips()).Main()
        self.LoadInfo()

    # Load more information, Mainly save information.
    def LoadInfo(self):
        self.info = newSave.save({
            'name': os.path.join(self.name, self.user),
            'path': self.location,
            'Json': True
        })
        self.placedData = self.info.readFile("placedData", True)
        self.boardData = self.info.readFile("ships", True)

    # The display
    def ShowDisplay(self):
        print("{}'s turn to place!\n".format(self.user))
        Functions.board.DisplayBoard(self.boardData)
        print("\nAlvalible Ships to place:")

        index = 1
        for item in self.placedData:
            if not self.placedData[item]:
                print("{}: {}".format(index, item))
            else:
                print("{}: {} (move)".format(index, item))
            index += 1

    # Custom check for the rotation
    def _rotationCheck(self):
        string = None
        rotation = {
            "n": 0,
            "e": 90,
            "s": 180,
            "w": 270
        }
        while not string:
            string = input("Enter rotation of ship (\033[04mN\033[0morth, \033[04mE\033[0mast, \033[04mS\033[0mouth, \033[04mW\033[0mest): ")  # noqa E501
            if len(string) == 0:
                Functions.clear(1, "Please enter a valid direction!")
                string = None

            if string is not None:
                string = string[0].lower()
                try:
                    self.rot = rotation[string]
                except KeyError:
                    string = None
                    Functions.clear(1, "Please enter a valid direction (North, East, South, West)")  # noqa

    def AttemptPlace(self, ships, place, y, x, rot):
        try:
            breaked = False
            for i in range(ships[place].Length):
                squareId = [0, 0]
                if rot == 0:
                    if y - i >= 0:
                        squareId = [y - i, x]
                    else:
                        # Error, doesn't fit on board
                        self._ShipError()
                elif rot == 90:
                    if x + i >= 0:
                        squareId = [y, x + i]
                    else:
                        self._ShipError()
                elif rot == 180:
                    if y + i >= 0:
                        squareId = [y + i, x]
                    else:
                        self._ShipError()
                elif rot == 270:
                    if x - i >= 0:
                        squareId = [y, x - i]
                    else:
                        self._ShipError()
                else:  # Fail safe check.
                    Functions.clear(1, "Error in placing ship, Please try again")  # noqa
                    self.placed = False
                    break
                if self.gameBoard[squareId[0]][squareId[1]] == "-":
                    self.gameBoard[squareId[0]][squareId[1]] = str(ships[place].Symbol)  # noqa
                else:
                    self._Error("Ship collides with another ship!")
                    self.gameBoard = deep
                    break

            if not self.breaked:
                self.placed = True
            else:
                Functions.board.DisplayBoard(self.gameBoard)
                print("{}'s Turn to place ships\n\nShip placing: {}".format(self.user, ships[place].Name))  # noqa
        except IndexError:  # reset if ship can't go there
            self._Error("Ship does not fit on board")
            self.gameBoard = deep
            self.placed = False

    # Main part of placing
    def Place(self):
        while len(self.ships) > 1:
            # Gets ship to place
            place = Functions.check("Enter ship number you want to place (-1 to stop, data will save): ",
                                    (self.ShowDisplay),
                                    (-1, len(self.ships))).getInput()
            if place == -1:
                return -1
            if place is not None:
                place -= 1

            # Creates a copy just in case
            backupCopy = copy.deepcopy(self.boardData)

            # gets the location to place ship
            Location = Functions.LocationConvert(input("Please enter location to place ship: ")).Convert()  # noqa E501
            roatation = self._rotationCheck()

    def Main(self):
        Functions.clear()
        self.Place()
        return False
