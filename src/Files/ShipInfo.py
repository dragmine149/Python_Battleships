"""
ShipInfo.py
Where all ship data is stored

How to add new ship:
- Add a new class at the bottom with the requirements below
- Add the class to the list at the very bottom with the other ships

Example:
class Short(ShipTemplate):
    def __init__(self) -> None:
        super().__init__(2, 1, "Destroyer (2 long)", "{", Fore.RED)

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
    - Default: 'Length' by 'Height'
- Symbol
    - Required: No
    - Value: String
    - Default: Unclaimed symbol
- Colour
    - Required: No
    - Value: String (colorama.Fore)
"""
import typing
from colorama import Fore


class ShipTemplate:
    def __init__(self, Length: int, Height: int,
                 Name: str = None, Symbol: str = None, Colour: str = ""):
        self.__Length = Length
        self.__Height = Height
        self.__Name = Name
        self.__Symbol = Symbol
        self.__Colour = Colour

        if self.__Name is None:
            self.setName()

    def getLength(self):
        return self.__Length

    def getHeight(self):
        return self.__Height

    def getTotalArea(self):
        return self.__Length * self.__Height

    def getName(self):
        return self.__Name

    def setName(self, name: str):
        if name is None:
            self.__Name = f'{self.__Length} by {self.__Height}'
            return

        self.__Name = name

    def getSymbol(self):
        return self.__Symbol

    def setSymbol(self, symbol: str):
        self.__Symbol = symbol

    def getColour(self):
        return self.__Colour


class Short(ShipTemplate):
    def __init__(self) -> None:
        super().__init__(2, 1, "Destroyer (2 long)", "{", Fore.RED)


class Medium1(ShipTemplate):
    def __init__(self):
        super().__init__(3, 1, "Submarine (3 long)", "}", Fore.YELLOW)


class Medium2(ShipTemplate):
    def __init__(self):
        super().__init__(3, 1, "Cruiser (3 long)",
                         "=", Fore.LIGHTYELLOW_EX)


class Long(ShipTemplate):
    def __init__(self):
        super().__init__(4, 1, "Battleship (4 long)",
                         "(", Fore.GREEN)


class ExtraLong(ShipTemplate):
    def __init__(self):
        super().__init__(5, 1, "Aircraft Carrier (5 long)",
                         ")", Fore.CYAN)


def getShips():
    return [
        Short(),
        Medium1(),
        Medium2(),
        Long(),
        ExtraLong()
    ]


def getDefaultPlaced():
    data = {}
    for ship in getShips():
        data[ship.getName()] = False

    return data


def getShipFromSymbol(symbol: str) -> ShipTemplate | None:
    for ship in getShips():
        ship: ShipTemplate
        if ship.getSymbol() == symbol:
            return ship

    return None


"""
CODE
Here is stuff to controll the ship data and get accruate inputs.
Please do not touch
"""


class shipInfo:
    def __init__(self, ships):
        self.ships: typing.List[ShipTemplate] = ships
        # Symbol set defined, These are symbols that the text will work without
        # having the grid be messed up
        self.symbols = [
            "{", "}", "(", ")", "=",  # Default
            # Custom set
            "[", "]", "<", ">", "!",
            "@", "£", "#", '$', "%",
            "^", "&", "*", "±", "§"
        ]

    # Checks if all values of the class are correct
    def valid_Check(self):
        goodShips = []  # good, meet the rules
        for shipNum in range(len(self.ships)):
            ship = self.ships[shipNum]
            # Length check
            if ship.getLength() <= 0:
                print("Invalid ship length! (must be positive)")
                continue
            # Height check
            if ship.getHeight() <= 0:
                print("Invalid ship height! (must be positive)")
                continue

            # set health
            ship.Health = ship.getTotalArea()
            goodShips.append(ship)  # If reach, then good ship

        return goodShips

    # This is called after to make sure symbols don't get taken out if the ship
    # is bad and could be used for something else.
    def setSymbol(self):
        noSymbol: typing.List[ShipTemplate] = []
        # Removes all symbols already assigned
        # Adds ships without symbols to array
        for ship in self.ships:
            if ship.getSymbol() in self.symbols:
                self.symbols.remove(ship.getSymbol())
                continue
            noSymbol.append(ship)

        # For ships without symbols, Add a symbol from the global array
        # If run out of symbols, then erm... Just remove the ship (need to add result other than remove for this case)  # noqa E501
        for index, noShip in enumerate(noSymbol):
            if len(self.symbols) <= 0:
                break

            noShip.setSymbol(self.symbols[0])
            self.symbols.pop(0)

    # Groups everything up into one funciton
    def Main(self):
        self.ships = self.valid_Check()
        self.setSymbol()
        return self.ships


if __name__ == "__main__":
    s = shipInfo(getShips())
