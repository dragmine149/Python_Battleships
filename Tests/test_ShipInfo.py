import ShipInfo as ships


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


def Creation():
    customShips = [
        TB4(),
        Invalid(),
        Missing(),
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
    """
    # Where the data comes from
    shipData = ships.shipInfo(customShips)
    customShips = shipData.Main()

    # Checks to make sure data is Correct
    Passed = [[False, False], False]
    print({'Remaning': customShips})
    foundShip = None
    for ship in customShips:
        if ship.Name == "(8 long)":  # 2B4 check
            print("Found ship! (TB4)")
            foundShip = ship
            if ship.Health == 8:
                print("Correct Health (TB4)")
                try:
                    print(ship.Symbol)
                    Passed[0] = True
                except AttributeError:
                    Passed[0][0] = True
                    Passed[0][1] = True
                    break
            else:
                Passed[0][0] = True
            break
    if isinstance(Passed[0], list):
        if not Passed[0][0]:
            print("Failed to find ship! Excepted: TB4. Found:None")
        if not Passed[0][1]:
            print("Failed to get ship health! Excepted: 8, Found:{}".format(foundShip.Health))  # noqa E501
        Passed[0] = False

    if len(customShips) == 6:  # In theory, no other added in testing
        Passed[1] = True
        print("customShips length is 6 (removed two bad ships)")
    if not Passed[1]:
        print("customShips length is {}! Excepted: {}".format(len(customShips), 6))  # noqa

    return Passed[0] and Passed[1]


assert test_Test()
