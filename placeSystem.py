import save
import ShipInfo as ship
import Functions
import copy


class place:
    def __init__(self, game, user):
        self.game = game
        self.user = user
        self.rot = 0
        self.breaked = False
        self.placed = False
        self.gameBoard = save.read(self.game, self.user)

    # Get the board saved.
    def _LoadBoard(self):
        self.gameBoard = save.read(self.game, self.user)
        save.DisplayBoard(self.gameBoard)

    def _ShowShips(self, list):
        print("Alvalible Ships:\n-1:Return (data will not be saved untill all ships palced)\n0: View Grid")  # noqa
        for sHip in range(len(list)):
            print("{}: {}".format(sHip + 1, list[sHip].Name))

    def _rangeCheck(self, value, list):
        if value >= 0 and value <= len(list):
            return True
        return False

    def _rotationCheck(self, request):
        string = None
        rotation = {
            "n": 0,
            "e": 90,
            "s": 180,
            "w": 270
        }
        while not string:
            string = input(request)[0].lower()
            try:
                self.rot = rotation[string]
            except KeyError:
                string = None
                Functions.clear(1, "Please enter a valid direction (North, East, South, West)")  # noqa

    def _Error(self, message, deep):
        Functions.clear(1, message)
        self.breaked = True
        self.placed = False

    def _Reset(self):
        self.rot = 0
        self.breaked = False
        self.placed = False

    def Place(self):
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
            self._ShowShips(ships)
            place = None
            while place is None:
                place = Functions.check("Enter ship you want to place: ", self._ShowShips, ships, self._rangeCheck, ships).InputDigitCheck() # noqa
                if place == -1:
                    return -1
                if place is not None:
                    place -= 1
            deep = copy.deepcopy(self.gameBoard)

            if place != -1:
                while not self.placed:
                    # get ship position
                    x, y = None, None
                    while x is None and y is None:
                        x, y = Functions.LocationConvert(input("Enter location to place ship: ")).Convert()  # noqa
                    self._rotationCheck("Enter rotation of ship (North, East, South, West): ")  # noqa

                    # Attempts to place the ship at the desiered location
                    # with rotation.
                    try:
                        self.breaked = False
                        for i in range(ships[place].Length):
                            squareId = [0, 0]
                            if self.rot == 0:
                                squareId = [y - i, x]
                            elif self.rot == 90:
                                squareId = [y, x + i]
                            elif self.rot == 180:
                                squareId = [y + i, x]
                            elif self.rot == 270:
                                squareId = [y, x - i]
                            else:  # Fail safe check.
                                Functions.clear(1, "Error in placing ship, Please try again")  # noqa
                                self.placed = False
                                break
                            if self.gameBoard[squareId[0]][squareId[1]] == "-":
                                self.gameBoard[squareId[0]][squareId[1]] = ships[place].Symbol  # noqa
                            else:
                                self._Error("Ship collides with another ship!")
                                self.gameBoard = deep
                                break

                        if not self.breaked:
                            self.placed = True
                        else:
                            save.DisplayBoard(self.gameBoard)
                            print("{}'s Turn to place ships\n\nShip placing: {ships[place].Name}".format(self.user))  # noqa
                    except IndexError:  # reset if ship can't go there
                        self._Error("Ship does not fit on board",)
                        self.gameBoard = deep

                ships.pop(place)  # removed placed ship
            else:
                print("This has not been implement yet!")
            Functions.clear(0)
            save.DisplayBoard(self.gameBoard)

        save.UpdateFile(self.gameBoard, "Saves/{}/{}".format(self.game, self.user), "ships")  # noqa
