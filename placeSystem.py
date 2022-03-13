import SaveSystem as save
import board
import ShipInfo as ship
import Functions
import os
import copy


# Get the board saved.
def LoadBoard(game, user):
    gameBoard = save.read(game, user)
    board.DisplayBoard(gameBoard)


def ShowShips(list):
    print("Alvalible Ships:")
    print("0: View Grid")
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


def Error(message, deep):
    Functions.clear(1, message)
    return False, deep

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
        print(f"{user}'s Turn to place ships\n")
        ShowShips(ships)
        place = Functions.InputDigitCheck("Enter ship you want to place: ", ShowShips, ships, rangeCheck, ships) - 1 # noqa
        deep = copy.deepcopy(cBoard)

        if place != -1:
            placed = False
            while not placed:
                # get ship position
                x = Functions.InputDigitCheck("Enter X position to place ship: ", board.DisplayBoard, cBoard, Functions.NumberRangeCheck, len(cBoard[0])) - 1  # noqa
                y = Functions.InputDigitCheck("Enter Y position to place ship: ", board.DisplayBoard, cBoard, Functions.NumberRangeCheck, len(cBoard)) - 1  # noqa
                rot = rotationCheck("Enter rotation of ship (North, East, South, West): ")  # noqa

                # Attempts to place the ship at the desiered location with rotation.
                try:
                    breaked = False
                    for i in range(ships[place].Length):
                        if rot == 0:  # up
                            if cBoard[y - i][x] == "-":
                                cBoard[y - i][x] = ships[place].Symbol
                            else:
                                placed, cBoard = Error("Ship collides with another ship!", deep)
                                breaked = True
                                break
                        elif rot == 90:  # right
                            if cBoard[y][x + i] == "-":
                                cBoard[y][x + i] = ships[place].Symbol
                            else:
                                placed, cBoard = Error("Ship collides with another ship!", deep)
                                breaked = True
                                break
                        elif rot == 180:  # down
                            if cBoard[y + i][x] == "-":
                                cBoard[y + i][x] = ships[place].Symbol
                            else:
                                placed, cBoard = Error("Ship collides with another ship!", deep)
                                breaked = True
                                break
                        elif rot == 270:  # left
                            if cBoard[y][x - i] == "-":
                                cBoard[y][x - i] = ships[place].Symbol
                            else:
                                placed, cBoard = Error("Ship collides with another ship!", deep)
                                breaked = True
                                break
                        else:  # Fail safe check.
                            Functions.clear(1, "Error in placing ship, Please try again")
                            placed = False
                    if not breaked:
                        placed = True
                    else:
                        board.DisplayBoard(cBoard)
                        print(f"{user}'s Turn to place ships\n")
                        print(f"Ship placing: {ships[place].Name}")
                except IndexError:  # reset if ship can't go there
                    placed, cBoard = Error("Ship does not fit on board", deep)

            ships.pop(place)  # removed placed ship
        Functions.clear(0)
        board.DisplayBoard(cBoard)

    save.UpdateFile(cBoard, f"Saves/{game}/{user}", "ships")


if __name__ == "__main__":
    os.system("clear")
    # LoadBoard("1", "me")
    placeShips("1", "me")
    os.system("clear")
    placeShips("1", "me2")
