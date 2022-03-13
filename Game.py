import SaveSystem as save
import board
import ShipInfo as ship
import Functions


# Get the board saved.
def LoadBoard(game, user):
    gameBoard = save.read(game, user)
    board.DisplayBoard(gameBoard)


def ShowShips(list):
    print("Alvalible Ships:")
    for sHip in range(len(list)):
        print(f"{sHip + 1}: {list[sHip].Name}")


def rangeCheck(value, list):
    if value > 0 and value < len(list):
        return True
    else:
        return False


def placeShips(game, user):
    ships = [
        ship.Short(),
        ship.Medium(),
        ship.Medium(),
        ship.Long(),
        ship.ExtraLong()
    ]
    cBoard = save.read(game, user)
    while len(ships) > 0:
        ShowShips(ships)
        place = Functions.InputDigitCheck("Enter ship you want to place: ", ShowShips, ships, rangeCheck, ships)  # noqa
        print(place)


if __name__ == "__main__":
    # LoadBoard("1", "me")
    placeShips("1", "me")
