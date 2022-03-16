import save
import Functions
import ShipInfo as ship


class fire:
    def __init__(self, game, fireUser, targetUser):
        self.game = game
        self.fireUser = fireUser
        self.targetUser = targetUser
        self.shotTaken = False
        self.fireBoard = save.read(game, fireUser)
        self.targetBoard = save.read(game, targetUser, "ships")

    def Fire(self):
        # load data
        while not self.shotTaken:
            print(f"{self.fireUser}'s Turn to shoot\n")
            save.DisplayBoard(self.fireBoard)
            # get shooting cooridnates
            x, y = None, None
            while x is None and y is None:
                x, y = Functions.LocationConvert(input("Enter position to shoot at: ")).Convert()  # noqa
            # check if haven't already shot there
            if self.fireBoard[y][x] != "-":
                Functions.clear(1, "You have already shot there")
            else:
                # Find enemy and place icon depending on hit or miss.
                # (X = hit, + = miss)
                # has ship, no matter the symbol
                if self.targetBoard[y][x] != "-":
                    self.fireBoard[y][x] = "X"
                    print("HIT!")
                else:
                    self.fireBoard[y][x] = "+"
                    print("Miss")
                self.shotTaken = True
                save.UpdateFile(self.fireBoard, f"Saves/{self.game}/{self.fireUser}", "grid")  # noqa
                return self._DestroyedCheck()

    # Compares both boards to check if any has been destroyed
    def _DestroyedCheck(self):
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
            for y in range(len(self.fireBoard)):
                for x in range(len(self.fireBoard[y])):
                    if self.fireBoard[y][x] == "X" and self.targetBoard[y][x] == pShip.Symbol:  # check if hit   # noqa
                        pShip.Health -= 1  # remove
            if pShip.Health == 0:  # add
                destroyedList += f"{pShip.Name}\n"
                destroyedAmmount += 1

        # game over check
        if destroyedAmmount == len(ships):
            Functions.clear()
            print(f"GG!\n'{self.fireUser}'' has beaten ''{self.targetUser}''")
            save.UpdateFile(self.fireUser, f"Saves/{self.game}", "win")
            return True
        Functions.clear(2, destroyedList)
