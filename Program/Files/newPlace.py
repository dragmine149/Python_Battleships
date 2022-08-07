import importlib
import copy
import os
Save = importlib.import_module('Files.Save')
Functions = importlib.import_module('Files.Functions')
ShipInfo = importlib.import_module('Files.ShipInfo')
colours = importlib.import_module('Files.colours')
Settings = importlib.import_module('Files.Settings')


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
        self.info = Save.save({
            'path': self.location[0],
        })
        loc = self.location[1]
        self.placedData = self.info.readFile(
            "{}/placedData".format(loc), True)
        self.boardData = self.info.readFile(
            "{}/ships".format(loc), True)

    # The display
    def ShowDisplay(self, showShips=True, board=None):
        # Multiplayer check?
        print("{}'s turn to place!\n".format(self.user))
        if board is None:
            board = self.boardData
        Functions.board.DisplayBoard(board, "Your Board")

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
            "n": 0,
            "e": 90,
            "s": 180,
            "w": 270,
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
        backupboard = copy.deepcopy(board)

        # board       -> copy of the current board.
        # ship        -> ship with data to place.
        # fLoatcation -> position to place ship.
        # rotation    -> rotation of ship.
        while True:
            try:
                for i in range(ship.Length):
                    placeId = [fLoatcation[0], fLoatcation[1]]

                    # A Bunch of checks, Personally don't like these but if we
                    # don't want ships to rotate off the board, these have to
                    # be included.
                    if rotation == 0:
                        if placeId[1] - i < 0:
                            raise IndexError("Ship goes off side of board!")

                        placeId = [placeId[0], placeId[1] - i]
                    if rotation == 90:
                        if placeId[0] + i < 0:
                            raise IndexError("Ship goes off side of board!")

                        placeId = [placeId[0] + i, placeId[1]]
                    if rotation == 180:
                        if placeId[1] + i < 0:
                            raise IndexError("Ship goes off side of board!")

                        placeId = [placeId[0], placeId[1] + i]
                    if rotation == 270:
                        if placeId[0] - i < 0:
                            raise IndexError("Ship goes off side of board!")

                        placeId = [placeId[0] - i, placeId[1]]

                    if board[placeId[1]][placeId[0]] == "-":
                        board[placeId[1]][placeId[0]] = "\033[33m{}\033[0m".format(str(ship.Symbol))  # noqa E501
                    else:
                        raise IndexError('Collides with another ship!')

                return board
            except IndexError as ie:
                # Report error, reget input
                print("Invalid ship placement -> {}".format(ie))
                fLoatcation = fLoatcationFunc()
                rotation = rotationFunc()
                board = backupboard

    def __GetLocation(self):
        # Better location check to get the location easier.
        # And fixes an incorrect issue
        Location = [None, None]
        while Location[0] is None or Location[1] is None:
            Location = Functions.LocationConvert(input("Please enter location to place ship: "))  # noqa E501
            Location = Location.Convert()
        return Location

    def _ChangeColour(self, board, ship):
        for y in range(len(board)):
            for x in range(len(board[y])):
                sy = str(ship.Symbol)
                rSt = ship.Colour + sy + colours.c()
                board[y][x] = rSt if board[y][x].find(sy) > -1 else board[y][x]
        return board

    def PlaceData(self, place):
        Functions.clear()

        # Prints out a smaller, updated display
        self.ShowDisplay(False)
        print('\nPlacing Ship: {}\n'.format(self.ships[place].Name))

        # Creates a copy just in case
        backupCopy = copy.deepcopy(self.boardData)

        # Attempts to place the ship on the map and show the board.
        board = self.AttemptPlace(backupCopy, self.ships[place], self.__GetLocation, self._rotationCheck)  # noqa E501
        Functions.clear()
        self.ShowDisplay(False, board)

        # Checks if the board and what has been placed is correct.
        def yes():
            return True, True

        def no():
            return self.boardData, False

        cont, saved = Functions.check("\nDoes this look correct? (y or n): ",
                                      returnFunc=(yes, no)).getInput('ynCheck')
        if cont is True:
            cont = self._ChangeColour(board, self.ships[place])

        return cont, saved

    # Checks if all ships have been placed
    def PlacedAll(self):
        for ship in self.placedData:
            if not self.placedData[ship]:
                return True
        return False

    # Main part of placing
    def Place(self):
        Finished = False
        while not Finished:
            Functions.clear()
            if not self.PlacedAll():
                return -2
            # Gets ship to place
            place = Functions.check("Enter ship number you want to place: ",
                                    (self.ShowDisplay),
                                    (0, len(self.ships))).getInput()
            if place == 0:
                self.info.writeFile(Settings.request('colour'),
                                    True, "UserColour", True)
                return 0
            if place is not None:
                place -= 1

                if self.placedData[self.ships[place].Name]:
                    Functions.clear(2, "Moving ships comming in Update 3 (Sorry, big task to do atm.)")  # noqa E501
                    continue

                self.boardData, saved = self.PlaceData(place)
                if saved:
                    print("Saved")
                    self.placedData[self.ships[place].Name] = True
                    loc = self.location[1]
                    self.info.writeFile(self.boardData,
                                        True,
                                        "{}/ships".format(loc),
                                        True,
                                        True)
                    self.info.writeFile(self.placedData,
                                        True,
                                        "{}/placedData".format(loc),
                                        True,
                                        True)

    def Main(self):
        Functions.clear()
        data = self.Place()
        if data == -2:
            boardSize = Save.save({
                'path': self.location[0]
            }).readFile(
                '{}/GameData'.format(os.path.split(self.location[1])[0]),
                True)
            self.info.writeFile(Functions.board.CreateBoard(boardSize['size']),
                                True,
                                "{}/shots".format(self.location[1]),
                                True,
                                True)  # noqa E501
        return data == -2
