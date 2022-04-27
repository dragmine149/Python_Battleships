"""
ShipInfo.py
Where all ship data is stored

How to add new ship:
- Add a new class at the bottom with the requirements below
- Add the class to the list at the very bottom with the other ships

Example:
class Short:
    def __init__(self):
        self.Length = 2
        self.Height = 1
        self.Name = "Destroyer (2 long)"
        self.Symbol = "{"
        self.Health = 2

Arguments:
- Length
    - Required: Yes
    - Value: Interger
- Height
    - Required: Yes
    - Value: Interger
- Name
    - Required: No
    - Value: String
    - Default: Ship size
- Symbol
    - Required: No
    - Value: String
    - Default: Unclaimed symbol
"""


class Short:
    def __init__(self):
        self.Length = 2
        self.Height = 1
        self.Name = "Destroyer (2 long)"
        self.Symbol = "{"


class Medium1:
    def __init__(self):
        self.Length = 3
        self.Height = 1
        self.Name = "Submarine (3 long)"
        self.Symbol = "}"


class Medium2:
    def __init__(self):
        self.Length = 3
        self.Height = 1
        self.Name = "Cruiser (3 long)"
        self.Symbol = "="


class Long:
    def __init__(self):
        self.Length = 4
        self.Height = 1
        self.Name = "Battleship (4 long)"
        self.Symbol = "("


class ExtraLong:
    def __init__(self):
        self.Length = 5
        self.Height = 1
        self.Name = "Aircraft Carrier (5 long)"
        self.Symbol = ")"


def getShips():
    return [
        Short(),
        Medium1(),
        Medium2(),
        Long(),
        ExtraLong()
    ]


"""
CODE
Here is stuff to controll the ship data and get accruate inputs.
Please do not touch
"""


class shipInfo:
    def __init__(self, ships):
        self.ships = ships
        self.symbols = [
            "{",
            "}",
            "(",
            ")",
            "=",
            "[",
            "]",
            "<",
            ">"
        ]

    def calculate(self, ship):
        return ship.Length * ship.Height

    def valid_Check(self):
        goodShips = []
        for shipNum in range(len(self.ships)):
            if shipNum == len(self.ships):
                print("Reached limit!")
                break
            ship = self.ships[shipNum]
            # Length check
            try:
                if ship.Length == 0:
                    continue
            except AttributeError:
                continue
            # Height check
            try:
                if ship.Height == 0:
                    continue
            except AttributeError:
                continue

            # Set name
            try:
                ship.Name
            except AttributeError:
                ship.Name = "({} long)".format(self.calculate(ship))

            # set health
            ship.Health = self.calculate(ship)
            goodShips.append(ship)

        return goodShips

    def setSymbol(self):
        noSymbol = []
        for ship in self.ships:
            try:
                if ship.Symbol in self.symbols:
                    self.symbols.remove(ship.Symbol)
                else:
                    noSymbol.append(ship)
            except AttributeError:
                pass

        for noShip in range(len(noSymbol)):
            if self.symbols.Length > 0:
                noSymbol[noShip].Symbol = self.symbols[0]
                self.symbols.pop(0)
            else:
                self.ships.remove(noShip)

    def Main(self):
        self.ships = self.valid_Check()
        self.setSymbol()
        return self.ships


if __name__ == "__main__":
    s = shipInfo(getShips())
