# Imports
import Game
import placeSystem as place
import fireSystem as fire
import Save as save
import Functions
import os
import time
import platform

# Prints where stored
filePath = os.path.dirname(os.path.realpath(__file__))
print("Stored Path: {}".format(filePath))
os.chdir(filePath)
Functions.clear(.5)


class Main:
    def __init__(self):
        # Setup class info
        self.gameName = None
        self.users = None
        self.Placed = None
        self.Location = None
        self.multi = None
        self.cont = 0

    def __reset(self):
        self.gameName = None
        self.users = None
        self.Placed = None

    def LocInput(self):
        return input("Enter location to place ship: ")

    # Whilst waiting for other person to do stuff.
    def waitSim(self, message):
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
        except KeyboardInterrupt:
            return "Fake"

    def Place(self, user, other):
        return place.place(self.gameName,
                           user,
                           self.Location).Place(
                           self.LocInput,
                           other
                           )

    def Fire(self):
        game = False
        while not game:
            game = fire.fire(self.gameName,
                             self.users[0],
                             self.users[1],
                             self.Location).Fire()
            if not game:
                game = fire.fire(self.gameName,
                                 self.users[0],
                                 self.users[1],
                                 self.Location).Fire()
        # Win check
        # "Fake means returned"
        if game == "Fake":
            Functions.clear()
        else:
            Functions.clear(10)
        return

    # Loop of the program
    def MainLoop(self):
        # Get game information
        gameInfo = Game.game().GetInput()
        self.gameName = gameInfo[0]
        self.users = gameInfo[1]
        self.Placed = gameInfo[2]
        self.Location = gameInfo[3]
        self.multi = gameInfo[4]
        Functions.clear(2)

        # If not multiplayer.
        if not self.multi:
            # Value to see if the user didn't back out
            self.cont = 0
            # Checks if placed
            if not self.Placed:
                # Place otherwise
                self.cont = self.Place(self.users[0], self.users[1])
                Functions.clear()
                if self.cont == 0:
                    self.cont = self.Place(self.users[1], self.users[0])

            Functions.clear()
            # Plays game until win or return
            if self.cont == 0:
                self.Fire()
            self.__reset()
        else:
            # Gets players username
            username, opponent = None, None
            while username is None:
                username = input("Please enter your name: ")
                if self.users[0] == username:
                    opponent = self.users[1]
                elif self.users[1] == username:
                    opponent = self.users[0]
                else:
                    username = None
                    print("Name not found in the game! (spectate comming soon)")  # noqa

            # Place check
            self.count = 0
            if not self.Placed:
                self.count = self.Place(username, opponent)

            o_Placed = False
            while not o_Placed:
                print(self.users)
                opponentData = save.save(self.Location, data={
                    'name': self.gameName,
                    'file': opponent
                })


if __name__ == "__main__":
    main = Main()
    main.MainLoop()
