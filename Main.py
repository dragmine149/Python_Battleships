import GameSetup as setup
import placeSystem as place
import fireSystem as fire
import Functions
setclass = setup.game()

while True:
    # Terminal setup ui
    gameName, users, Placed = setclass.setup()

    Functions.clear()

    # check to see if game has already been started
    # and there are ships on the board.
    if not Placed:
        # Placing ships on the borad
        place.placeShips(gameName, users[0])
        Functions.clear()
        place.placeShips(gameName, users[1])

    Functions.clear()

    game = False
    while not game:
        game = fire.FireShip(gameName, users[0], users[1])
        if not game:
            game = fire.FireShip(gameName, users[1], users[0])

    Functions.clear(10)
