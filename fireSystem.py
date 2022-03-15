import save
import Functions
import ShipInfo as ship


def FireShip(game, fireUser, targetUser):
    # load data
    fireBoard = save.read(game, fireUser)
    targetBoard = save.read(game, targetUser, "ships")
    shotTaken = False
    while not shotTaken:
        print(f"{fireUser}'s Turn to shoot\n")
        save.DisplayBoard(fireBoard)

        # get shooting cooridnates
        x, y = Functions.LocationInput(input("Enter position to shoot at: "))

        # check if haven't already shot there
        if fireBoard[y][x] != "-":
            Functions.clear(1, "You have already shot there")
        else:
            # Find enemy and place icon depending on hit or miss.
            # (X = hit, + = miss)

            # Do we save it in there account as well? or just compare?
            if targetBoard[y][x] != "-":  # has ship, no matter the symbol
                fireBoard[y][x] = "X"
                print("HIT!")
            else:
                fireBoard[y][x] = "+"
                print("Miss")
            shotTaken = True
            save.UpdateFile(fireBoard, f"Saves/{game}/{fireUser}", "grid")
            return DestroyedCheck(fireBoard, targetBoard, fireUser, targetUser, game)  # noqa


# Compares both boards to check if any has been destroyed
def DestroyedCheck(fireBoard, targetBoard, fireUser, targetUser, game):
    ships = [
        ship.Short(),
        ship.Medium1(),
        ship.Medium2(),
        ship.Long(),
        ship.ExtraLong()
    ]
    destroyedList = "Destroyed Ships:\n"  # makes a list
    destroyedAmmount = 0

    # This could be made better
    for pShip in ships:
        for y in range(len(fireBoard)):
            for x in range(len(fireBoard[y])):
                if fireBoard[y][x] == "X":  # check if hit
                    if targetBoard[y][x] == pShip.Symbol:  # find ship
                        pShip.Health -= 1  # remove
        if pShip.Health == 0:  # add
            destroyedList += f"{pShip.Name}\n"
            destroyedAmmount += 1

    # game over check
    if destroyedAmmount == len(ships):
        Functions.clear()
        print("GG!")
        print(f"{fireUser} has beaten {targetUser}")
        save.UpdateFile(fireUser, f"Saves/{game}", "win")
        return True
    Functions.clear(2, destroyedList)


if __name__ == "__main__":
    Functions.clear()
    for _ in range(2):
        FireShip("1", "me", "me2")
        Functions.clear(1)
        FireShip("1", "me2", "me")
