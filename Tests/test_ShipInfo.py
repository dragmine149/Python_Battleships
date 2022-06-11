import sys
# We assume the user is in the main directory.
# TODO find Program folder and change to that.
sys.path.insert(0, './Program')
import ShipInfo as ships
from colours import *


# Test classes
class TB4:
    def __init__(self):
        self.Height = 4
        self.Length = 2


class Invalid:
    def __init__(self):
        self.Length = 0
        self.Height = 0


class Missing:
    def __init__(self):
        pass

class InvalidColour:
    def __init__(self):
        self.Length = 3
        self.Height = 1
        self.Colour = 'red'
        self.Name = 'IC'

class ValidColour:
    def __init__(self):
        self.Length = 3
        self.Height = 1
        self.Colour = c('r')
        self.Name = 'VC'

def Creation():
    customShips = [
        TB4(),
        Invalid(),
        Missing(),
        InvalidColour(),
        ValidColour()
    ]

    for ship in ships.getShips():
        customShips.append(ship)
    return customShips


# The actually test itself
def test_Test():
    customShips = Creation()
    """
    Excepted Results:
    - TB4 getting health, name, symbol
    - Invalid being deleted from table
    - Missing being deleted from table
    - InvalidColour Colour being set to None
    - ValidColour not having anything
    """
    # Where the data comes from
    shipData = ships.shipInfo(customShips)
    customShips = shipData.Main()

    # Checks to make sure data is Correct
    Passed = [[False, False, False], False, [False, False]]
    print({'Remaning': customShips})
    foundShip = None
    for ship in customShips:
        if ship.Name == "(2 by 4)":  # 2B4 check
            print("Found ship! (TB4)")
            foundShip = ship
            if ship.Health == 8:
                print("Correct Health (TB4)")
                try:
                    print(vars(ship))
                    print(ship.Symbol)
                    Passed[0] = True
                except AttributeError:
                    Passed[0][0] = True
                    Passed[0][1] = True
                    Passed[0][2] = False
                    break
            else:
                Passed[0][0] = True
        if ship.Name == 'IC':
            print(vars(ship))
            if ship.Colour == None:
                Passed[2][0] = True
        if ship.Name == 'VC':
            print(vars(ship))
            if ship.Colour == c('r'):
                Passed[2][1] = True
                
    if isinstance(Passed[0], list):
        if not Passed[0][0]:
            print("Failed to find ship! Excepted: TB4. Found:None")
        if not Passed[0][1]:
            print("Failed to get ship health! Excepted: 8, Found:{}".format(foundShip.Health))  # noqa E501
        if not Passed[0][2]:
            print("Failed to get ship symbol!")
        Passed[0] = False

    if isinstance(Passed[2], list):
        if not Passed[2][0]:
            print("(IC) Failed to reset ship colour to None!")
        if not Passed[2][1]:
            print("Ship (VC) doesn't have correct colour!")
        if Passed[2][0] and Passed[2][1]:
            Passed[2] = True
        else:
            Passed[2] = False

    if len(customShips) == 8:  # In theory, no other added in testing
        Passed[1] = True
        print("customShips length is 8 (removed two bad ships)")
    if not Passed[1]:
        print("customShips length is {}! Excepted: {}".format(len(customShips), 8))  # noqa

    print(Passed[0], Passed[1], Passed[2])
    assert Passed[0] and Passed[1] and Passed[2]
    return Passed[0] and Passed[1] and Passed[2]


assert test_Test()
