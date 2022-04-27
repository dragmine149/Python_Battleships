"""
ShipInfo.py
Where all ship data is stored

How to add new ship:
- In the class, add a new class with the required information

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
- Health
    - Required: No
    - Value: String
    - Default: Length * Height
"""


class Ships:
    class Short:
        def __init__(self):
            self.Length = 2
            self.Height = 1
            self.Name = "Destroyer (2 long)"
            self.Symbol = "{"
            self.Health = 2

    class Medium1:
        def __init__(self):
            self.Length = 3
            self.Height = 1
            self.Name = "Submarine (3 long)"
            self.Symbol = "}"
            self.Health = 3

    class Medium2:
        def __init__(self):
            self.Length = 3
            self.Height = 1
            self.Name = "Cruiser (3 long)"
            self.Symbol = "="
            self.Health = 3

    class Long:
        def __init__(self):
            self.Length = 4
            self.Height = 1
            self.Name = "Battleship (4 long)"
            self.Symbol = "("
            self.Health = 4

    class ExtraLong:
        def __init__(self):
            self.Length = 5
            self.Height = 1
            self.Name = "Aircraft Carrier (5 long)"
            self.Symbol = ")"
            self.Health = Ships.calculateHealth(self)

    # Changed to something better
    @staticmethod
    def calculateHealth(ship):
        return ship.Length * ship.Height

    def getShips(self):
        return [
            self.Short(),
            self.Medium1(),
            self.Medium2(),
            self.Long(),
            self.ExtraLong()
        ]


def getShips():
    return Ships().getShips()


if __name__ == "__main__":
    print(getShips())
