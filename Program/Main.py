# Imports
import Game
import placeSystem as place
import fireSystem as fire
import Save as save
import Functions
import os
import time
import sys

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
        self.opponent = None

    def __reset(self):
        # Resets for infinite loop
        self.gameName = None
        self.users = None
        self.Placed = None
        self.opponent = None

    def LocInput(self):
        # This is so we can send it into a function
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

    # Place ship
    def Place(self, user, other):
        return place.place(self.gameName,
                           user,
                           self.Location).Place(
                           self.LocInput,
                           other
                           )

    def getTurn(self):
        # Using the 'turn' file, finds the users turn
        turn = None
        while not isinstance(turn, str):
            turn = save.save(self.Location, False, {
                'name': self.gameName,
                'file': 'turn',
            }).readFile({
                # don't want to do this (on windows at time of writing)  # noqa E501
                # but it fixies it for now...
                'name': None
            })
        return turn.replace('"', '')

    def Fire(self, username=None):
        self.printStatus()
        # Fire function
        game = False
        while not game:
            turn = self.getTurn()
            print({'username': username,
                   'self.opponent': self.opponent,
                   'turn': turn,
                   'opponent turn?': self.opponent == turn,
                   'Your turn?': username == turn})
            if username == turn:
                game = fire.fire(self.gameName,
                                 username,
                                 self.opponent,
                                 self.Location).Fire()
            elif turn == self.opponent:
                game = self.waitSim("Waiting for opponent to shoot")
                Functions.clear()
            else:
                for user in range(len(self.users)):
                    # Get the other user (target user)
                    other = 0
                    if user == 0:
                        other = 1

                    if turn == self.users[user]:
                        game = fire.fire(self.gameName,
                                         self.users[user],
                                         self.users[other],
                                         self.Location).Fire()
        # Win check
        # "Fake" means returned
        if game == "Fake":
            Functions.clear()
        else:
            Functions.clear(10)
        return

    def printStatus(self):
        print({
            'self.gameName': self.gameName,
            'self.users': self.users,
            'self.Placed': self.Placed,
            'self.Location': self.Location,
            'self.multi': self.multi
        })

    # Loop of the program
    def MainLoop(self, argv):
        # Get game information
        gameInfo = Game.game().GetInput()
        print({'gameInfo': gameInfo})
        self.gameName = gameInfo[0]
        # Users start
        users = gameInfo[1]
        self.users = []
        for usr in users:
            if isinstance(usr, dict):
                self.users.append(usr['name'])
            else:
                self.users.append(usr)
        # users end
        self.Placed = gameInfo[2]
        Placed = self.Placed[0] and self.Placed[1]
        self.Location = gameInfo[3]
        self.multi = gameInfo[4]
        Functions.clear(2)

        self.printStatus()
        # If not multiplayer.
        if not self.multi:
            # Value to see if the user didn't back out
            self.cont = 0
            # Checks if placed
            if not Placed:
                # Place otherwise
                self.cont = self.Place(self.users[0], self.users[1])  # noqa
                Functions.clear()
                if self.cont == 0:
                    self.cont = self.Place(self.users[1], self.users[0])  # noqa

            Functions.clear()
            # Plays game until win or return
            if self.cont == 0:
                self.Fire()
            self.__reset()
        else:
            # Gets players username
            username, self.opponent = None, None
            playerPos = 0  # To check if local player placed.
            while username is None:
                username = input("Please enter your name: ")
                if self.users[0] == username:
                    playerPos = 0
                    self.opponent = self.users[1]
                elif self.users[1] == username:
                    playerPos = 1
                    self.opponent = self.users[0]
                else:
                    username = None
                    print("Name not found in the game! (spectate comming soon)")  # noqa

            # Place check
            self.count = 0
            if not self.Placed[playerPos]:
                self.count = self.Place(username, self.opponent)

            Functions.clear()

            if self.count == 0:
                o_Placed = False
                if not (self.Placed[0] and self.Placed[1]):
                    while not o_Placed:
                        loc = 0
                        if playerPos == 0:
                            loc = 1
                        if isinstance(users[loc], dict):
                            location = users[loc]['id']
                        else:
                            location = os.path.join(self.Location, self.gameName, users[loc])  # noqa
                        o_Placed = save.save(location).CheckForFile('ships')
                        if not o_Placed:
                            o_Placed = self.waitSim("Waiting for opponent to place their ships")  # noqa

                if o_Placed != "Fake":
                    self.Fire(username)
            self.__reset()
        self.MainLoop()


def help():
    print("""USAGE:
--------------------------------------------------------------------------------------
python Main.py [Option]

Option can be one of the following:
- String
  - Attempts to load game name of string, If not found will make game name of string
- Number
  - Does that action (1 = load, 2 = make, 3 = settings). Quick form

Other possible options:
- help
  - Shows this menu
---------------------------------------------------------------------------------------
""")  # noqa E501

    return 1


if __name__ == "__main__":
    # Checks if help before doing anything
    arguments = sys.argv
    if len(arguments) > 1:
        if arguments[1].lower()[0] == 'h':
            sys.exit(help())
    else:
        # Do rest of program
        main = Main()
        main.MainLoop(sys.argv)