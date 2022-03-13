import SaveSystem as save
import board
import ShipInfo as ship
import Functions
import os


# Get the board saved.
def LoadBoard(game, user):
    gameBoard = save.read(game, user)
    board.DisplayBoard(gameBoard)


def ShowShips(list):
    print("Alvalible Ships:")
    for sHip in range(len(list)):
        print(f"{sHip + 1}: {list[sHip].Name}")


def rangeCheck(value, list):
    if value >= 0 and value <= len(list):
        return True
    else:
        return False


def rotationCheck(request):
    string = None
    while not string:
        string = input(request)[0].lower()
        if string == "n":
            return 0
        if string == "e":
            return 90
        if string == "s":
            return 180
        if string == "w":
            return 270
        string = None
        Functions.clear(1, "Please enter a valid direction (North, East, South, West)")  # noqa


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
        place = Functions.InputDigitCheck("Enter ship you want to place: ", ShowShips, ships, rangeCheck, ships) - 1 # noqa
        board.DisplayBoard(cBoard)

        # get ship position
        x = Functions.InputDigitCheck("Enter X position to place ship: ", board.DisplayBoard, cBoard, Functions.NumberRangeCheck, len(cBoard[0]))  # noqa
        y = Functions.InputDigitCheck("Enter Y position to place ship: ", board.DisplayBoard, cBoard, Functions.NumberRangeCheck, len(cBoard))  # noqa
        rot = rotationCheck("Enter rotation of ship (North, East, South, West): ")  # noqa
        input = [x, y, rot]
        print(input)


if __name__ == "__main__":
    os.system("clear")
    # LoadBoard("1", "me")
    placeShips("1", "me")
