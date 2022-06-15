import newSave
import Functions
import copy
import ShipInfo
import os
import colours


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
    def ShowDisplay(self, showShips=True, board=None):
        print("{}'s turn to place!\n".format(self.user))
        if board is None:
            board = self.boardData
        Functions.board.DisplayBoard(board)

        if showShips:
            print("\nAlvalible Ships to place:")

            print("0: Back (all data will save)")
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
            "n": 90,
            "e": 180,
            "s": 270,
            "w": 0,
        }
        while not string:
            # Highlights important letters
            # shows you that you don't have to type whole word.
            string = input("Enter rotation of ship (\033[04mN\033[0morth, \033[04mE\033[0mast, \033[04mS\033[0mouth, \033[04mW\033[0mest): ")  # noqa E501
            if len(string) == 0:
                Functions.clear(1, "Please enter a valid direction!")
                string = None

            if string is not None:
                string = string[0].lower()
                try:
                    return rotation[string]
                except KeyError:
                    string = None
                    Functions.clear(1, "Please enter a valid direction (North, East, South, West)")  # noqa

    # fLoatcation -> Curtestly of sophie
    def AttemptPlace(self, board, ship, fLoatcationFunc, rotationFunc):

        # Ability to get information in this loop
        fLoatcation = fLoatcationFunc()
        rotation = rotationFunc()

        # board       -> copy of the current board.
        # ship        -> ship with data to place.
        # fLoatcation -> position to place ship.
        # rotation    -> rotation of ship.
        while True:
            try:
                empty = copy.deepcopy(board)
                for i in range(ship.Length):
                    placeId = [fLoatcation[0], fLoatcation[1]]

                    # A Bunch of checks, Personally don't like these but if we
                    # don't want ships to rotate off the board, these have to
                    # be included.
                    if rotation == 0:
                        if placeId[0] - i < 0:
                            raise IndexError("Ship goes off side of board!")

                        placeId = [placeId[0] - i, placeId[1]]
                    if rotation == 90:
                        if placeId[1] + i < 0:
                            raise IndexError("Ship goes off side of board!")

                        placeId = [placeId[0], placeId[1] + i]
                    if rotation == 180:
                        if placeId[0] + i < 0:
                            raise IndexError("Ship goes off side of board!")

                        placeId = [placeId[0] + i, placeId[1]]
                    if rotation == 270:
                        if placeId[1] - i < 0:
                            raise IndexError("Ship goes off side of board!")

                        placeId = [placeId[0], placeId[1] - i]

                    # Place ship, Change?
                    if board[placeId[1]][placeId[0]] == "-":
                        board[placeId[1]][placeId[0]] = "\033[33m{}\033[0m".format(str(ship.Symbol))  # noqa E501
                    if empty[placeId[1]][placeId[0]] == "-":
                        empty[placeId[1]][placeId[0]] = ship.Colour + str(ship.Symbol) + colours.c()  # noqa E501

                return board, empty
            except IndexError as ie:
                # Report error, reget input
                print("Invalid ship placement -> {}".format(ie))
                fLoatcation = fLoatcationFunc()
                rotation = rotationFunc()

    def __GetLocation(self):
        # Better location check to get the location easier.
        # And fixes an incorrect issue
        Location = [None, None]
        while Location[0] is None or Location[1] is None:
            Location = Functions.LocationConvert(input("Please enter location to place ship: "))  # noqa E501
            Location = Location.Convert()
        return Location

    def PlaceData(self, place):
        Functions.clear()

        # Prints out a smaller, updated display
        self.ShowDisplay(False)
        print('\nPlacing Ship: {}\n'.format(self.ships[place].Name))

        # Creates a copy just in case
        backupCopy = copy.deepcopy(self.boardData)

        # Attempts to place the ship on the map and show the board.
        board, empty = self.AttemptPlace(backupCopy, self.ships[place], self.__GetLocation, self._rotationCheck)  # noqa E501
        Functions.clear()
        self.ShowDisplay(False, board)

        # Checks if the board and what has been placed is correct.
        def yes():
            return True

        def no():
            return self.boardData

        cont = Functions.check("\nDoes this look correct? (y or n): ",
                               returnFunc=(yes, no)).getInput('ynCheck')

        # Translate and use inputs
        if cont is True:
            return empty
        return cont

    # Checks if all ships have been placed
    def PlacedAll(self):
        for ship in self.placedData:
            if not self.placedData[ship]:
                return True
        return False

    # Main part of placing
    def Place(self):
        while self.PlacedAll:
            Functions.clear()
            # Gets ship to place
            place = Functions.check("Enter ship number you want to place: ",
                                    (self.ShowDisplay),
                                    (0, len(self.ships))).getInput()
            if place == 0:
                return 0
            if place is not None:
                if self.placedData[self.ships[place].Name]:
                    Functions.clear(2, "Moving ships comming in Update 3 (Sorry, big task to do atm.)")  # noqa E501
                    continue

                place -= 1

                self.boardData = self.PlaceData(place)
                self.placedData[self.ships[place].Name] = True

    def Main(self):
        Functions.clear()
        self.Place()
        return False
