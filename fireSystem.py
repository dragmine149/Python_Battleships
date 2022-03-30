# import SaveSystem as save
import Functions
import ShipInfo as ship
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class fire:
    # Setup
    def __init__(self, game, fireUser, targetUser, Location):
        self.game = game
        self.fireUser = fireUser
        self.targetUser = targetUser
        self.shotTaken = False
        self.fireBoard = save.save(Location).readFile(os.path.join(game, fireUser), "grid")  # noqa
        self.targetBoard = save.save(Location).readFile(os.path.join(game, targetUser), "ships")  # noqa
        self.saveLocation = Location

    # Does multiple checks and fires at the other user
    def Fire(self, Multi=False):
        # Just in case another check fails.
        if os.path.exists("{}/{}/win".format(self.saveLocation, self.game)):
            return True

        # Keep shooting until shot is know to be completed.
        while not self.shotTaken:
            # get shooting cooridnates
            x, y = None, None
            while x is None and y is None:
            	# Output
                print("{}'s Turn to shoot\n".format(self.fireUser))
                save.board.DisplayBoard(self.fireBoard)
                
                shotPos = input("Enter position to shoot at (-1 to quit game for now): ")  # noqa
                if shotPos != "-1":
                    x, y = Functions.LocationConvert(shotPos).Convert()  # noqa
                else:
                    return "Fake"  # fake win

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

                # Update files.
                self.shotTaken = True
                save.save(self.saveLocation).writeFile("{}/{}".format(self.game, self.fireUser), "grid", self.fireBoard)  # noqa

                # Switch user when fired.
                if Multi:
                    save.save(self.saveLocation).writeFile(self.game, "turn", self.targetUser)  # noqa
                return self._DestroyedCheck(Multi)

    # Compares both boards to check if any has been destroyed
    def _DestroyedCheck(self, Multi):
        # Change ships to take the ammount from file instead of in list.
        # Mod support bascially.
        ships = [
            ship.Short(),
            ship.Medium1(),
            ship.Medium2(),
            ship.Long(),
            ship.ExtraLong()
        ]
        destroyedList = "Destroyed Ships:\n"  # makes a list
        destroyedAmount = 0

        # Could this be better?
        for pShip in ships:
            for y in range(len(self.fireBoard)):
                for x in range(len(self.fireBoard[y])):
                    if self.fireBoard[y][x] == "X" and self.targetBoard[y][x] == pShip.Symbol:  # check if hit   # noqa
                        pShip.Health -= 1  # remove
            if pShip.Health == 0:  # add
                destroyedList += "{}\n".format(pShip.Name)
                destroyedAmount += 1

        # game over check
        if destroyedAmount == len(ships):
            Functions.clear()
            if not Multi:
                print("GG!\n'{}' has beaten '{}'".format(self.fireUser, self.targetUser))  # noqa
            save.save(self.saveLocation, True).writeFile(self.game, "win", self.fireUser)  # noqa
            return True
        Functions.clear(2, destroyedList)
