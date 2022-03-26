# This file needs to be cleaned up a bit

import GameSetup as setup
import placeSystem as place
import fireSystem as fire
import SaveSystem as save
import Functions
import os
import time
import platform
print("Stored Path: {}".format(os.path.dirname(os.path.realpath(__file__))))
time.sleep(1)
os.chdir(os.path.dirname(os.path.realpath(__file__)))
gameName, users, Placed, Location, multi = None, None, None, None, None


def getLocation():
    return input("Enter location to place ship: ")


if os.path.exists('Tests/Path.txt'):
    os.remove('Tests/Path.txt')  # removes old data at start


def waitSim(iN, message):
    try:
        # Waiting message
        back = "(ctrl + c to go back)"
        print("{}       {}".format(message, back), end="\r")
        time.sleep(1)
        print("{}.      {}".format(message, back), end="\r")
        time.sleep(1)
        print("{}..     {}".format(message, back), end="\r")
        time.sleep(1)
        print("{}...    {}".format(message, back), end="\r")
        time.sleep(1)
        return iN
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
            pathLocation = Location.rstrip().replace('"', '')
            if platform.system() != "Windows":
                pathLocation = pathLocation.replace("\\", "")
            while not userSetup:
                if os.path.exists(os.path.join(pathLocation, gameName, other, "ships")):  # noqa
                    userSetup = True
                else:
                    v = waitSim(v, "Waiting for opponent to place their ships")
                    if v != 0:
                        userSetup = "Stop"

            if v == 0:
                # Actually playing the game
                game = False
                print("Current game: {}\nOpponent: {}".format(gameName, other))
                while not game:
                    try:
                        if save.save(Location).readFile(gameName, "turn") == name:  # noqa
                            game = fire.fire(gameName, name, other, Location).Fire(True)  # noqa
                            if not game:
                                print("Current game: {}\nOpponent: {}".format(gameName, other))  # noqa
                        else:
                            game = waitSim(game, "Waiting for opponent to take a shot")  # noqa
                    except KeyboardInterrupt:  # Probably shouldn't do this...
                        game = "Fake"
                        Functions.clear()
                        print("Current game: {}.\nOpponent: {}".format(gameName, other))  # noqa
                if game != "Fake":
                    print("\n")
                    if game:
                        winner = save.save(Location, True).readFile(gameName, "win")  # noqa
                        looser = name
                        if winner == name:
                            looser = other
                        print("GG!\n{} has beaten {}".format(winner, looser))
                    Functions.clear(10)
                gameName, users, Placed, multi = None, None, None, None
            else:
                Functions.clear()
        else:
            Functions.clear()
