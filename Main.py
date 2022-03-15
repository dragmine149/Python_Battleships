import GameSetup as setup
import placeSystem as place
import fireSystem as fire
import Functions
setClass = setup.game()

while True:
    # Terminal setup ui
    gameName, users, Placed = setClass.setup()
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
        game = fire.fire(gameName, users[0], users[1]).Fire()
        if not game:
            game = fire.fire(gameName, users[1], users[0]).Fire()
    Functions.clear(10)
