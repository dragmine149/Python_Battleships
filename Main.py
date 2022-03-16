import GameSetup as setup
import placeSystem as place
import fireSystem as fire
import Functions
import os
print("Stored Path: {}".format(os.path.dirname(os.path.realpath(__file__))))
os.chdir(os.path.dirname(os.path.realpath(__file__)))
gameName, users, Placed = None, None, None

while True:
    # Terminal setup ui
    gameName, users, Placed = setup.game().setup()
    Functions.clear()
    # check to see if game has already been started
    # and there are ships on the board.
    if not Placed:
        # Placing ships on the borad
        place.place(gameName, users[0]).Place()
        Functions.clear()
        place.place(gameName, users[1]).Place()
    Functions.clear()
    game = False
    while not game:
        game = fire.fire(gameName, users[0], users[1]).Fire()
        if not game:
            game = fire.fire(gameName, users[1], users[0]).Fire()
    Functions.clear(10)
    gameName, users, Placed = None, None, None
