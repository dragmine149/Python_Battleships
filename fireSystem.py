import Save as save
import Functions
import ShipInfo as ship
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class fire:
    # Setup
    def __init__(self, game, fireUser, targetUser, Location):
        print(game, fireUser, targetUser, Location)
        self.game = game
        self.fireUser = fireUser
        self.targetUser = targetUser
        self.shotTaken = False
        print(fireUser, targetUser)
        self.fireUserInfo = Functions.boardRetrieve(fireUser,
                                                    Location,
                                                    game,
                                                    None,
                                                    save.save(Location, data={
                                                        'name': self.game,
                                                        'file': fireUser
                                                    }),
                                                    'grid')
        self.fireBoard = self.fireUserInfo.getBoard()
        self.fireUserDir = self.fireUserInfo.userDirectory
        self.targetBoard = Functions.boardRetrieve(targetUser,
                                                   Location,
                                                   game,
                                                   None,
                                                   save.save(Location, data={
                                                      'name': self.game,
                                                      'file': targetUser
                                                   }),
                                                   'ships').getBoard()
        self.saveLocation = Location

    # Does multiple checks and fires at the other user
    def Fire(self):
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
                Functions.board.DisplayBoard(self.fireBoard)

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
                print({'self.saveLocation': self.saveLocation})
                saveInfo = save.save(self.saveLocation, data={
                    'name': self.fireUser,
                    'file': self.fireUser
                })
                path = os.path.join(self.saveLocation, self.game, self.fireUser)  # noqa
                if saveInfo.api:
                    path = self.fireUserDir
                saveInfo.writeFile({
                    'data': self.fireBoard,
                    'folder': path
                })

                # Switch user when fired.
                saveInfo = save.save(self.saveLocation, data={
                    'name': 'turn',
                    'file': 'trun'
                })
                path = os.path.join(self.saveLocation, self.game)
                if saveInfo.api:
                    path = self.saveLocation

                saveInfo.writeFile({
                    'data': self.targetUser,
                    'folder': path
                })

                # Chek what is destroyed.
                return self._DestroyedCheck()

    # Compares both boards to check if any has been destroyed
    def _DestroyedCheck(self):
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

            print("GG!\n'{}' has beaten '{}'".format(self.fireUser, self.targetUser))  # noqa
            save.save(self.saveLocation, data={
                'name': 'win',
                'file': 'win'
            }).writeFile({
                'data': self.fireUser,
                'folder': os.path.join(self.saveLocation, self.game)
            })
            return True
        Functions.clear(2, destroyedList)
