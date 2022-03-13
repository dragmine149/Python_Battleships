import SaveSystem as save
import board
import Functions


def FireShip(game, fireUser, targetUser):
    # load data
    fireBoard = save.read(game, fireUser)
    targetUser = save.read(game, targetUser, "ships")
    shotTaken = False
    while not shotTaken:
        board.DisplayBoard(fireBoard)

        # get shooting cooridnates
        x = Functions.InputDigitCheck("Enter X position to fire at: ", board.DisplayBoard, fireBoard, Functions.NumberRangeCheck, len(fireBoard)) - 1  # noqa
        y = Functions.InputDigitCheck("Enter Y position to fire at: ", board.DisplayBoard, fireBoard, Functions.NumberRangeCheck, len(fireBoard)) - 1  # noqa

        # check if haven't already shot there
        if fireBoard[y][x] != "-":
            Functions.clear(1, "You have already shot there")
        else:
            # Find enemy and place icon depending on hit or miss. (X = hit, + = miss)

            # Do we save it in there account as well? or just compare?
            if targetUser[y][x] != "-":  # has ship, no matter the symbol
                fireBoard[y][x] = "X"
                print("HIT!")
            else:
                fireBoard[y][x] = "+"
                print("Miss")
            shotTaken = True


if __name__ == "__main__":
    Functions.clear()
    FireShip("1", "me", "me2")
    Functions.clear(1)
    FireShip("1", "me2", "me")
