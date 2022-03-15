import board
import os
import sys
import time
import SaveSystem as save
import Functions
import Message


def loadGames():
    Message.sendMessage("Games found on disk:")
    games = os.listdir("Saves")
    Message.Load(games)


def LoadRangeCheck(value):
    amount = len(os.listdir("Saves"))
    if value > 0 and value <= amount:
        return True
    elif value == -1:
        return True
    else:
        return False


def SizeRangeCheck(size):
    if size >= 5:  # got to be big enough to hold all ships
        return True
    return False


def ProcessChoice(choice):
    if choice == 1 and not os.path.exists("Saves"):
        Message.sendMessage("There is no game to load!!")
        return None, None, None, None
    elif choice == 1 and len(os.listdir("Saves")) == 0:
        Message.sendMessage("There is no game to load!!")
        return None, None, None, None
    elif choice == 1:
        # load game
        Functions.clear()
        loadGames()
        game = Functions.InputDigitCheck("Enter number of game to load (-1 to go back): ", loadGames, None, LoadRangeCheck)  # noqa
        if game == -1:
            return None, None, None, None
        else:
            gameName = os.listdir('Saves')[game - 1]
            users = os.listdir(f"Saves/{gameName}")
            if os.path.exists(f"Saves/{gameName}/win.txt"):
                os.system("clear")
                for i in range(2):
                    Message.sendMessage(f"{users[i]} data")
                    Message.sendMessage("grid (where they shot)")
                    board.DisplayBoard(save.read(gameName, users[i]))
                    Message.sendMessage(f"{users[i]} data")
                    Message.sendMessage("ships (The ship layout they had)")
                    board.DisplayBoard(save.read(gameName, users[i], "ships"))
                input("Press enter when you are ready to continue.")
                return None, None, None, None
            else:
                placed = False
                if os.path.exists(f"Saves/{gameName}/{users[0]}/ships.txt") and os.path.exists(f"Saves/{gameName}/{users[1]}/ships.txt"):  # noqa
                    placed = True
                return True, gameName, users, placed
    elif choice == 2:
        # get the size
        x = Functions.InputDigitCheck("Please enter X size (length): ", None, None, SizeRangeCheck)  # noqa
        y = Functions.InputDigitCheck("Please enter Y size (length): ", None, None, SizeRangeCheck)  # noqa
        size = [x, y]
        GameBoard = board.CreateBoard(size)  # creates a board
        create = None
        while not create:  # saves the board
            name = input("Please enter a name for this game: ").replace(" ", "")  # noqa
            users = [
                str(input("Please enter player 1's name: ").replace(" ", "")),
                str(input("Please enter player 2's name: ").replace(" ", ""))
            ]
            create = save.save(GameBoard, name, users)
        return True, name, users, False
    elif choice == 0:
        sys.exit("Thank you for playing")
        return True, None, None, None


def fileRead():
    # convert over to the new Message System
    with open("Options.txt", "r") as options:
        lines = options.readlines()
        for line in range(len(lines)):
            if line == 1:
                if os.path.exists("Saves"):
                    if len(os.listdir("Saves")) == 0:
                        print(f"{lines[line].strip()} (disabled)")
                    else:
                        print(f"{lines[line].strip()}")
                else:
                    print(f"{lines[line].strip()} (disabled)")
            else:
                print(f"{lines[line].strip()}")


def setup():
    choice = None
    while not choice:
        Functions.clear()
        # Load interface thing...
        fileRead()
        # get the user choice
        choice = Functions.InputDigitCheck("Your Choice (number): ", fileRead)

        # Process choice
        choice, name, users, Placed = ProcessChoice(choice)
        time.sleep(1)
    return name, users, Placed


if __name__ == "__main__":
    setup()
