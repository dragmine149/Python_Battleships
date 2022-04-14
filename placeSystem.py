import Save as save
import ShipInfo as ship
import Functions
import copy
import os
import sys


"""
TODO:
- Replace google drive parts
- Fix with new save system
"""


class place:
    def __init__(self, game, user, Location):
        self.game = game
        self.user = user
        self.rot = 0
        self.breaked = False
        self.placed = False
        self.saveLocation = Location
        self.userDirectory = None
        self.saveInfo = save.save(self.saveLocation, data={
            'name': self.game,
            'file': self.user
        })
        self.boardRetrieve = Functions.boardRetrieve(user,
                                                     self.saveLocation,
                                                     self.game,
                                                     self.userDirectory,
                                                     self.saveInfo,
                                                     'grid')
        self.gameBoard = self.boardRetrieve.getBoard()
        self.userDirectory = self.boardRetrieve.userDirectory
        if not isinstance(self.gameBoard, list):
            sys.exit('Failed to find game, please check')

    # Get the board saved.
    def _LoadBoard(self):
        self.gameBoard = self.boardRetrieve.getBoard()
        self.userDirectory = self.boardRetrieve.userDirectory
        if self.gameBoard == "Failed -> Folder not found":
            sys.exit('Failed to find folder, please check')
        save.board.DisplayBoard(self.gameBoard)

    # List ships that the user can places
    def _ShowShips(self, list):
        print("Alvalible Ships:\n-1:Return (data will not be saved untill all ships palced)\n0: View Grid")  # noqa
        for sHip in range(len(list)):
            print("{}: {}".format(sHip + 1, list[sHip].Name))

    # Range check for input (in length of list)
    def _rangeCheck(self, value, list):
        if value >= 0 and value <= len(list):
            return True
        return False

    # Custom check for the rotation
    def _rotationCheck(self, request):
        string = None
        rotation = {
            "n": 0,
            "e": 90,
            "s": 180,
            "w": 270
        }
        while not string:
            string = input(request)
            if len(string) == 0:
                Functions.clear(1, "Please enter a valid direction!")
                string = None
            else:
                string = string[0].lower()
            try:
                self.rot = rotation[string]
            except KeyError:
                string = None
                Functions.clear(1, "Please enter a valid direction (North, East, South, West)")  # noqa

    # Reset error function
    def _Error(self, message):
        Functions.clear(1, message)
        self.breaked = True
        self.placed = False

    def _Reset(self):
        self.rot = 0
        self.breaked = False
        self.placed = False

    def _ShipError(self):
        self.gameBoard[len(self.gameBoard) + 1][len(self.gameBoard[0]) + 1] = "+++"  # noqa

    # Function to palce ship
    def Place(self, locInput, owner=None):
        Functions.clear()
        # TODO: change to allow mod support
        ships = [
            ship.Short(),
            ship.Medium1(),
            ship.Medium2(),
            ship.Long(),
            ship.ExtraLong()
        ]
        while len(ships) > 0:
            self._Reset()
            print("{}'s Turn to place ships\n".format(self.user))
            place = None
            testTemp = 0
            while place is None:
                place = Functions.check("Enter ship you want to place: ", self._ShowShips, ships, self._rangeCheck, ships).InputDigitCheck() # noqa
                if place == -1:
                    return -1
                if place is not None:
                    place -= 1
                testTemp += 1
            deep = copy.deepcopy(self.gameBoard)

            if place != -1:
                while not self.placed:
                    # get ship position
                    x, y = None, None
                    while x is None and y is None:
                        # Change to make sure locInput is function
                        x, y = Functions.LocationConvert(locInput()).Convert()  # noqa
                        self._rotationCheck("Enter rotation of ship (North, East, South, West): ")  # noqa

                    # Attempts to place the ship at the desiered location
                    # with rotation.
                    try:
                        self.breaked = False
                        for i in range(ships[place].Length):
                            squareId = [0, 0]
                            if self.rot == 0:
                                if y - i >= 0:
                                    squareId = [y - i, x]
                                else:
                                    # Error, doesn't fit on board
                                    self._ShipError()
                            elif self.rot == 90:
                                if x + i >= 0:
                                    squareId = [y, x + i]
                                else:
                                    self._ShipError()
                            elif self.rot == 180:
                                if y + i >= 0:
                                    squareId = [y + i, x]
                                else:
                                    self._ShipError()
                            elif self.rot == 270:
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

                ships.pop(place)  # removed placed ship
            else:
                print("This has not been implement yet!")
            Functions.clear(0)
            Functions.board.DisplayBoard(self.gameBoard)

        print({'user': self.user,
               'folder': self.saveLocation})
        save.save(self.saveLocation, data={
            'name': 'ships',
            'file': self.user
        }).writeFile({
            'data': self.gameBoard,
            'folder': self.userDirectory
        })
        save.save(self.saveLocation, data={
            'name': 'turn',
            'file': 'trun'
        }).writeFile({
            'data': owner,
            'folder': self.saveLocation
        })
        Functions.clear(2)
        return 0  # pass check
