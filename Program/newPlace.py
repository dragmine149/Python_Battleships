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
        print("\nAlvalible Options:")

        index = 1
        for item in self.placedData:
            if not self.placedData[item]:
                print("{}: {}".format(index, item))
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
