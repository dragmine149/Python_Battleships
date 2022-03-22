# This file needs to be cleaned up a bit

import GameSetup as setup
import placeSystem as place
import fireSystem as fire
import SaveSystem as save
import Functions
import os
import time
print("Stored Path: {}".format(os.path.dirname(os.path.realpath(__file__))))
os.chdir(os.path.dirname(os.path.realpath(__file__)))
gameName, users, Placed, Location, multi = None, None, None, None, None


def getLocation():
    return input("Enter location to place ship: ")


if os.path.exists('Tests/Path.txt'):
    os.remove('Tests/Path.txt')  # removes old data at start


def waitSim(in):
    try:
        # Waiting message
        print("Waiting for opponent to take their turn       (ctrl + c to go back)", end="\r")  # noqa
        time.sleep(1)
        print("Waiting for opponent to take their turn.      (ctrl + c to go back)", end="\r")  # noqa
        time.sleep(1)
        print("Waiting for opponent to take their turn..     (ctrl + c to go back)", end="\r")  # noqa
        time.sleep(1)
        print("Waiting for opponent to take their turn...    (ctrl + c to go back)", end="\r")  # noqa
        time.sleep(1)
        return in
    except KeyboardInterrupt:
        return "Fake"


while True:
    # Terminal setup ui
    gameName, users, Placed, Location, multi = setup.game().setup()
    Functions.clear()
    if not multi:
        # check to see if game has already been started
        # and there are ships on the board.
        v = 0
        if not Placed:
            # Placing ships on the borad
            v = place.place(gameName, users[0], Location).Place(getLocation)  # noqa
            Functions.clear()
            if v == 0 and not multi:
                v = place.place(gameName, users[1], Location).Place(getLocation) # noqa

        # Plays the game until stops or someone wins.
        if v == 0:
            Functions.clear()
            game = False
            while not game:
                game = fire.fire(gameName, users[0], users[1], Location).Fire()
                if not game:
                    game = fire.fire(gameName, users[1], users[0], Location).Fire()  # noqa
            if game != "Fake":
                Functions.clear(10)
            else:
                Functions.clear()
        else:
            Functions.clear()
        gameName, users, Placed = None, None, None
    else:
        # Different function for multiplayer as more checks.

        # get username.
        name = None
        other = None
        while not name:
            name = input("Please enter your username: ")
            if users[0] != name and users[1] != name:
                name = None
                print("Name not found in system (specate comming soon)")
            elif users[0] == name:
                other = users[1]
            elif users[1] == name:
                other = users[0]

        # Place check (and place)
        v = 0
        if not Placed:
            if not os.path.exists(os.path.join(Location, gameName, name, "ships")):  # noqa
                v = place.place(gameName, name, Location).Place(getLocation, save.save(Location).readFile(gameName, "multi"), users[0])  # noqa

        # Actual game
        if v == 0:
            # Waiting for other user to setup their ships
            userSetup = False
            while not userSetup:
                if os.path.exists(os.path.join(Location, gameName, other, "ships")):  # noqa
                    userSetup = True
                else:
                    v = waitSim(v)
                    if v != 0:
                        userSetup = "Stop"

            if v == 0:
                # Actually playing the game
                game = False
                while not game:
                    try:
                        if save.save(Location).readFile(gameName, "turn") == name:
                            game = fire.fire(gameName, name, other, Location).Fire()  # noqa
                        else:
                            game = waitSim(game)
                    except KeyboardInterrupt:  # Probably shouldn't do this...
                        game = "Fake"
                        Functions.clear()
                if game != "Fake":
                    Functions.clear(10)
                gameName, users, Placed, multi = None, None, None, None
            else:
                Functions.clear()
        else:
            Functions.clear()
