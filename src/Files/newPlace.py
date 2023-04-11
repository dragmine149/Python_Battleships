import copy

from PythonFunctions import Board, Convert
from PythonFunctions.Save import save
from PythonFunctions.Message import Message
from PythonFunctions.Check import Check
from PythonFunctions.Colours import FORMAT
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
        self.placedData = self.save.Read(
            f'{self.location}/{self.user}/placedData',
            encoding=self.save.encoding.BINARY)
        print("Loading board data")
        self.boardData = self.save.Read(
            f'{self.location}/{self.user}/ships',
            encoding=self.save.encoding.BINARY)
        print("Finished!")

    # The display
    def ShowDisplay(self, showShips=True, board=None):
        print("{}'s turn to place!\n".format(self.user))
        if board is None:
            board = self.boardData
        print("Your Board")
        Board.DisplayBoard(board)

        # Shows the alvalible ships to place etc
        if showShips:
            print("\nAlvalible Ships to place:")
            print("0: Back (all data will save)")
            for index, item in enumerate(self.placedData):
                msg = f"{index + 1}: {item}"
                if self.placedData[item]:
                    msg += " (move)"

                print(msg)

    # Custom check for the rotation
    def _rotationCheck(self):
        rotation = {
            "n": 0,
            "e": 90,
            "s": 180,
            "w": 270,
        }
        # Highlights important letters
        # shows you that you don't have to type whole word.
        north = f"{FORMAT.UNDERLINE}N{FORMAT.RESET}orth"
        east = f"{FORMAT.UNDERLINE}E{FORMAT.RESET}ast"
        south = f"{FORMAT.UNDERLINE}S{FORMAT.RESET}outh"
        west = f"{FORMAT.UNDERLINE}W{FORMAT.RESET}est"
        string = self.chk.getInput(
            f"Enter rotation of ship ({north}, {east}, {south}, {west}): ",
            self.chk.ModeEnum.yesno,
            info=('n', 'e', 's', 'w'))

        return rotation[string]
    
    def __ShipLocationCheck(self, placeId, index):
        if placeId + index < 0:
            raise IndexError("Ship goes off side of board!")
        return placeId + index

    # fLoatcation -> Curtestly of sophie
    def AttemptPlace(self, board, ship: ShipInfo.ShipTemplate):

        # Ability to get information in this loop
        fLoatcation = Convert.Location(
            input("Please enter location to place ship: "))
        rotation = self._rotationCheck()
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
                        placeId[1] = self.__ShipLocationCheck(placeId[1], -i)
                    if rotation == 90:
                        placeId[0] = self.__ShipLocationCheck(placeId[0], i)
                    if rotation == 180:
                        placeId[1] = self.__ShipLocationCheck(placeId[1], i)
                    if rotation == 270:
                        placeId[0] = self.__ShipLocationCheck(placeId[0], -i)

                    if board[placeId[1]][placeId[0]] != "-":
                        raise IndexError('Collides with another ship!')

                    board[placeId[1]][placeId[0]] = f"{Fore.YELLOW}{ship.getSymbol()}{Fore.RESET}"

                return board
            except IndexError as ie:
                # Report error, reget input
                print(f"Invalid ship placement -> {ie}")
                fLoatcation = Convert.Location(
                    input("Please enter location to place ship: "))
                rotation = self._rotationCheck()
                board = backupboard

    def _ChangeColour(self, board, ship: ShipInfo.ShipTemplate):
        symbol = ship.getSymbol()
        item = ship.getColour() + symbol + Fore.RESET
        for yIndex, yValue in enumerate(board):
            for xIndex, xValue in enumerate(yValue):
                if xValue != symbol:
                    # Skip other checks
                    continue
                board[yIndex][xIndex] = item
        return board

    def PlaceData(self, place):
        self.msg.clear()

        # Prints out a smaller, updated display
        self.ShowDisplay(False)
        shipPlacing = self.ships[place]
        print(f'\nPlacing Ship: {shipPlacing.getName()}')

        # Creates a copy just in case
        backupCopy = copy.deepcopy(self.boardData)

        # Attempts to place the ship on the map and show the board.
        board = self.AttemptPlace(backupCopy, shipPlacing)
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
    def PlacedAll(self) -> bool:
        print(self.placedData)
        for ship in self.placedData:
            if not self.placedData[ship]:
                return False
        return True

    # Main part of placing
    def Place(self):
        Finished = False
        while not Finished:
            self.msg.clear()
            if self.PlacedAll():
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
