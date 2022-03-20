# This file needs to be cleaned up a bit

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
    v = 0
    if not Placed:
        # Placing ships on the borad
        v = place.place(gameName, users[0]).Place(input("Enter location to place ship: "))  # noqa
        Functions.clear()
        if v == 0:
            v = place.place(gameName, users[1]).Place(input("Enter location to place ship: ")) # noqa

    # Plays the game until stops or someone wins.
    if v == 0:
        Functions.clear()
        game = False
        while not game:
            game = fire.fire(gameName, users[0], users[1]).Fire()
            if not game:
                game = fire.fire(gameName, users[1], users[0]).Fire()
        if game != "Fake":
            Functions.clear(10)
        else:
            Functions.clear()
    else:
        Functions.clear()
    gameName, users, Placed = None, None, None
