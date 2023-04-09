import copy

from PythonFunctions import Board, Convert
from PythonFunctions.Save import save
from PythonFunctions.Message import Message
from PythonFunctions.Check import Check
from colorama import Fore

from Files import ShipInfo


class Place:
    # setup the place system
    def __init__(self, location, user):
        self.save = save()
        self.msg = Message()
        self.chk = Check()

        self.location = location
        self.user = user
        self.ships = ShipInfo.shipInfo(ShipInfo.getShips()).Main()
        self.LoadInfo()

    # Load more information, Mainly save information.
    def LoadInfo(self):
        print("Loading user placed data")
        print("Loading placed Data")
        self.placedData = self.save.Read(f'{self.location}/{self.user}/placedData',
                                         encoding=self.save.encoding.BINARY)
        print("Loading board data")
        self.boardData = self.save.Read(f'{self.location}/{self.user}/ships',
                                        encoding=self.save.encoding.BINARY)
        print("Finished!")

    # The display
    def ShowDisplay(self, showShips=True, board=None):
        # Multiplayer check?
        print("{}'s turn to place!\n".format(self.user))
        if board is None:
            board = self.boardData
        print("Your Board")
        Board.DisplayBoard(board)

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
                self.msg.clear("Please enter a valid direction!", timeS=1)
                string = None

            if string is not None:
                string = string[0].lower()
                try:
                    return rotation[string]
                except KeyError:
                    string = None
                    self.msg.clear(
                        "Please enter a valid direction (North, East, South, West)",
                        timeS=1)

    # fLoatcation -> Curtestly of sophie
    def AttemptPlace(self, board, ship:ShipInfo.ShipTemplate, fLoatcationFunc, rotationFunc):

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
                for i in range(ship.getLength()):
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
                        board[placeId[1]][placeId[0]] = "\033[33m{}\033[0m".format(ship.getSymbol())  # noqa E501
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
            Location = Convert.Location(
                input("Please enter location to place ship: "))
        return Location

    def _ChangeColour(self, board, ship: ShipInfo.ShipTemplate):
        for y in range(len(board)):
            for x in range(len(board[y])):
                sy = ship.getSymbol()
                rSt = ship.getColour() + sy + Fore.RESET
                board[y][x] = rSt if board[y][x].find(sy) > -1 else board[y][x]
        return board

    def PlaceData(self, place):
        self.msg.clear()

        # Prints out a smaller, updated display
        self.ShowDisplay(False)
        print('\nPlacing Ship: {}\n'.format(self.ships[place].getName()))

        # Creates a copy just in case
        backupCopy = copy.deepcopy(self.boardData)

        # Attempts to place the ship on the map and show the board.
        board = self.AttemptPlace(backupCopy, self.ships[place], self.__GetLocation, self._rotationCheck)  # noqa E501
        self.msg.clear()
        self.ShowDisplay(False, board)

        # Checks if the board and what has been placed is correct.
        cont, saved = self.chk.getInput("\nDoes this look correct?: ",
                                        self.chk.ModeEnum.yesno,
                                        y=lambda: (True, True),
                                        n=lambda: (self.boardData, False))
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
            self.msg.clear()
            if not self.PlacedAll():
                return -2
            # Gets ship to place
            self.ShowDisplay()
            place = self.chk.getInput("Enter ship number you want to place: ",
                                      self.chk.ModeEnum.int,
                                      lower=0, higher=len(self.ships))
            if place == 0:
                # self.info.writeFile(Settings.request(['colour'])[0], "UserColour")
                print("User colour is disabled at the moment. Sorry")
                return 0
            if place is not None:
                place -= 1

                if self.placedData[self.ships[place].getName()]:
                    self.msg.clear(
                        "Moving ships comming in Update 3 (Sorry, big task to do atm.)",
                        timeS=2
                    )
                    continue

                self.boardData, saved = self.PlaceData(place)
                if saved:
                    print("Saved")
                    self.placedData[self.ships[place].getName()] = True

                    self.save.Write(self.boardData,
                                    f'{self.location}/{self.user}/ships',
                                    encoding=self.save.encoding.BINARY)
                    
                    self.save.Write(self.placedData,
                                    f'{self.location}/{self.user}/placedData',
                                    encoding=self.save.encoding.BINARY)

    def Main(self):
        self.msg.clear()
        data = self.Place()
        if data == -2:
            boardSize = self.save.Read(f"{self.location}/GameData",
                                       self.save.encoding.BINARY)
            self.save.Write(Board.CreateBoard(boardSize[0], boardSize[1]),
                            f'{self.location}/{self.user}/shots',
                            self.save.encoding.BINARY)
        return data == -2
