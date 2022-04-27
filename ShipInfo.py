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
        print('waiting...')
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
        for ship in self.ships:
            # Length check
            try:
                ship.Length
            except AttributeError:
                self.ships.remove(ship)
            # Height check
            try:
                ship.Height
            except AttributeError:
                self.ships.remove(ship)

            # Set name
            if ship.Name is None:
                ship.Name = "({} long)".format(self.calculate(ship))

            # set health
            ship.Health = self.calculate(ship)

    def setSymbol(self):
        noSymbol = []
        for ship in self.ships:
            if ship.Symbol in self.symbols:
                self.symbols.remove(ship.Symbol)
            else:
                noSymbol.append(ship)

        for noShip in noSymbol:
            if self.symbols.Length > 0:
                noShip.Symbol = self.symbols[0]
                self.symbols.pop(0)
            else:
                self.ships.remove(noShip)
                break

    def Main(self):
        self.valid_Check()
        self.setSymbol()
        return self.ships


if __name__ == "__main__":
    s = shipInfo(getShips())
