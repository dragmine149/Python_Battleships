import Functions
import os
import json


def save(data, name, users):
    if not os.path.exists("Saves"):
        os.mkdir("Saves")
    if os.path.exists(f"Saves/{name}"):
        print("Please enter a name that has not already been used.")
        Functions.clear(1)
        return None
    else:
        os.system(f"mkdir Saves/{name}")
        os.system(f"mkdir Saves/{name}/{users[0]}")
        if os.path.exists(f"Saves/{name}/{users[0]}"):
            UpdateFile(data, f"Saves/{name}/{users[0]}", "grid")
            os.system(f"mkdir Saves/{name}/{users[1]}")
            if os.path.exists(f"Saves/{name}/{users[1]}"):
                UpdateFile(data, f"Saves/{name}/{users[1]}", "grid")
                return True
            else:
                Functions.clear(1, "Error in path creation... (invalid characters?)")  # noqa
                os.system(f"rm -d -r Saves/{name}")
                return False
        else:
            Functions.clear(1, "Error in path creation... (invalid characters?)")  # noqa
            os.system(f"rm -d -r Saves/{name}")
            return False


def UpdateFile(data, path, o):
    with open(f'{path}/{o}.txt', 'w+') as file:
        file.write(str(json.dumps(data)))


def read(game, user, o="grid"):
    data = None
    with open(f'Saves/{game}/{user}/{o}.txt', 'r') as file:
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
