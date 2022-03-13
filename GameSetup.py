import board
import os
import sys
import time
import SaveSystem as save
import Functions


def loadGames():
    print("Games found on disk:")
    games = os.listdir("Saves")
    for file in range(len(games)):
        print(f"{file + 1}: {games[file]}")


def LoadRangeCheck(value):
    amount = len(os.listdir("Saves"))
    if value > 0 and value <= amount:
        return True
    elif value == -1:
        return True
    else:
        return False


def ProcessChoice(choice):
    if choice == 1 and not os.path.exists("Saves"):
        print("There is no game to load!!")
        return None
    elif choice == 1:
        # load game
        Functions.clear()
        loadGames()
        game = Functions.InputDigitCheck("Enter number of game to load (-1 to go back): ", loadGames, None, LoadRangeCheck)  # noqa
        if game == -1:
            return None
        else:
            print("Loading (NOT IMPLEMENT YET)")
        return True
    elif choice == 2:
        # get the size
        size = [
            Functions.InputDigitCheck("Please enter X size (length): "),
            Functions.InputDigitCheck("Please enter Y size (length): ")
        ]
        GameBoard = board.CreateBoard(size)  # creates a board
        create = None
        while not create:  # saves the board
            name = input("Please enter a name for this game: ")
            users = [
                input("Please enter player 1's name: "),
                input("Please enter player 2's name: ")
            ]
            create = save.save(GameBoard, name, users)
        return True
    elif choice == 3:
        sys.exit("Thank you for playing")
        return True


def fileRead():
    with open("Options.txt", "r") as options:
        lines = options.readlines()
        for line in range(len(lines)):
            if line == 0 and not os.path.exists("Saves"):
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
        choice = ProcessChoice(choice)
        time.sleep(1)


if __name__ == "__main__":
    setup()
