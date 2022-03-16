import Functions
import os
import json
import shutil
os.chdir(os.path.dirname(os.path.realpath(__file__)))


def save(data, name, users):
    if not os.path.exists("Saves"):
        os.mkdir("Saves")
    if os.path.exists("Saves/{}".format(name)):
        print("Please enter a name that has not already been used.")
        Functions.clear(1)
        return None
    else:
        os.mkdir("Saves/{}".format(name))
        os.mkdir("Saves/{}/{}".format(name, users[0]))
        if os.path.exists("Saves/{}/{}".format(name, users[0])):
            UpdateFile(data, "Saves/{}/{}".format(name, users[0], "grid"))
            os.mkdir("Saves/{}/{}".format(name, users[1]))
            if os.path.exists("Saves/{}/{}".format(name, users[1])):
                UpdateFile(data, "Saves/{}/{}".format(name, users[1]), "grid")
                return True
            else:
                Functions.clear(1, "(2) Error in path creation... (invalid characters?)")  # noqa
                shutil.rmtree("rm -d -r Saves/{}".format(name))
                return False
        else:
            Functions.clear(1, "(1) Error in path creation... (invalid characters?)")  # noqa
            shutil.rmtree("rm -d -r Saves/{}".format(name))
            return False


def UpdateFile(data, path, o="grid"):
    with open('{}/{}.txt'.format(path, o), 'w+') as file:
        file.write(str(json.dumps(data)))


def read(game, user, o="grid"):
    data = None
    with open('Saves/{}/{}/{}.txt'.format(game, user, o), 'r') as file:
        data = file.read()
        data = json.loads(data)
    return data


# Create the board in a 2d array.
def CreateBoard(size):
    board = []
    for _ in range(size[1]):  # _ = assaign it to nothing.
        x = []
        for _ in range(size[0]):  # x grid
            x.append('-')
        board.append(x)

    return board


# Loops through the board and prints it out.
def DisplayBoard(board):
    for y in board:
        for x in y:
            print(x, end="")
        print()


if __name__ == "__main__":
    board = CreateBoard([10, 10])
    DisplayBoard(board)
