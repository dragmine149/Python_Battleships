import copy

from PythonFunctions import Board
from PythonFunctions.Save import save
from PythonFunctions.Message import Message
from PythonFunctions.Check import Check
from PythonFunctions.Colours import Translate, Format
from PythonFunctions.Run import Timer
from colorama import Fore

from Files import ShipInfo


class Place:
    # setup the place system
    def __init__(self, gamePath: str, user: str):
        self.save = save()
        self.chk = Check()

        self.location = gamePath
        self.user = user
        self.ships = ShipInfo.shipInfo(ShipInfo.getShips()).Main()
        self.placedData = self.save.Read(
            f'{self.location}/{self.user}/placedData',
            encoding=self.save.encoding.BINARY)
        self.boardData = self.save.Read(
            f'{self.location}/{self.user}/ships',
            encoding=self.save.encoding.BINARY)

    # The display
    def ShowDisplay(self, board, showShips=True):
        print(f"{self.user}'s turn to place!", end='\n\n')
        Board.DisplayBoard(board, coords=True)

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
    def __rotationCheck(self):
        rotation = {
            "n": 0,
            "e": 90,
            "s": 180,
            "w": 270,
        }
        # Highlights important letters
        # shows you that you don't have to type whole word.
        north = f"{Translate('N', Format.UNDERLINE)}orth"
        east = f"{Translate('E', Format.UNDERLINE)}ast"
        south = f"{Translate('S', Format.UNDERLINE)}outh"
        west = f"{Translate('W', Format.UNDERLINE)}est"
        string = self.chk.getInput(
            f"Enter rotation of ship ({north}, {east}, {south}, {west}): ",
            self.chk.ModeEnum.yesno,
            info=('n', 'e', 's', 'w'))

        return rotation[string]

    def GetShipPlacementInfo(self):
        return self.chk.getInput('Please enter location to place ship:',
                                 self.chk.ModeEnum.location,
                                 x=len(self.boardData[0]),
                                 y=len(self.boardData)), self.__rotationCheck()

    def __ShipLocationCheck(self, placeId, index):
        if placeId + index < 0:
            raise IndexError("Ship goes off side of board!")
        return placeId + index

    # fLoatcation -> Curtestly of sophie
    def AttemptPlace(self, board, ship: ShipInfo.ShipTemplate):
        validShip = False
        tempShipValue = Translate(
            f'{Fore.YELLOW}{ship.getSymbol()}{Fore.RESET}', Format.BOLD)
        data = {
            0: (1, 1, -1),
            90: (0, 0, 1),
            180: (1, 1, 1),
            270: (0, 0, -1)
        }
        while not validShip:
            # Ability to get information in this loop
            fLoatcation, rotation = self.GetShipPlacementInfo()
            backupboard = copy.deepcopy(board)
            info = data.get(rotation)

            # board       -> copy of the current board.
            # ship        -> ship with data to place.
            # fLoatcation -> position to place ship.
            # rotation    -> rotation of ship.
            validShip = True
            for i in range(ship.getLength()):
                fLoatcation[info[0]] = self.__ShipLocationCheck(
                    info[1], i * info[2])

                if board[fLoatcation[1]][fLoatcation[0]] != "-":
                    board = backupboard
                    validShip = False
                    break

                board[fLoatcation[1]][fLoatcation[0]] = tempShipValue

            if validShip:
                return board

    @Timer
    def __ChangeColour(self, board, ship: ShipInfo.ShipTemplate):
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
        Message.clear()

        # Prints out a smaller, updated display
        self.ShowDisplay(self.boardData, False)
        shipPlacing = self.ships[place]
        print(f'\nPlacing Ship: {shipPlacing.getName()}')

        # Creates a copy just in case
        backupCopy = copy.deepcopy(self.boardData)

        # Attempts to place the ship on the map and show the board.
        board = self.AttemptPlace(backupCopy, shipPlacing)
        Message.clear()
        self.ShowDisplay(board, False)

        # Checks if the board and what has been placed is correct.
        cont, saved = self.chk.getInput("\nDoes this look correct?: ",
                                        self.chk.ModeEnum.yesno,
                                        y=lambda: (True, True),
                                        n=lambda: (self.boardData, False))
        if cont is True:
            cont = self.__ChangeColour(board, self.ships[place])

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
            Message.clear()
            if self.PlacedAll():
                return -2
            # Gets ship to place
            self.ShowDisplay(self.boardData)
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
                    Message.clear(
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
        Message.clear()
        data = self.Place()
        if data == -2:
            boardSize = self.save.Read(f"{self.location}/GameData",
                                       self.save.encoding.BINARY)
            self.save.Write(Board.CreateBoard(boardSize[0], boardSize[1]),
                            f'{self.location}/{self.user}/shots',
                            self.save.encoding.BINARY)
        return data == -2
