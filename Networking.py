import os
import time
import shutil
import random
import string
import json


class save:
    # path = saves dir on network
    def __init__(self, path):
        self.path = path.rstrip().replace("\\", "")
        self.newgame = None
        self.Test()

    def Test(self):
        os.system("clear")
        print("Loading network...")
        # Tries to write to server
        writeCheck = self._writeCheck()
        time.sleep(1)

        # Tries to read from server
        readCheck = self._readCheck()
        time.sleep(1)

        # Tries to remove excess files
        try:
            if self.newgame:
                shutil.rmtree(self.newgame)
            else:
                shutil.rmtree(os.path.join(self.path, "Test"))
        except FileNotFoundError:
            print("Failed to remove files created")
        time.sleep(1)
        print("\n\n")

        # Output results
        if writeCheck and readCheck:
            print("Client can access server files. Everything is ready.")
        elif writeCheck:
            print("Client can write to server but not read... how?")
            os.path.sys.exit("Required permission missing: Read.")
        elif readCheck:
            print("Client can read server data but not write.")
            os.path.sys.exit("Required permission missing: Write.")
        else:
            print("Client can not read or write to server.")
            os.path.sys.exit("""Required permissions missing: Read + Write.
            Is server down?""")

    def _writeCheck(self):
        print("Write Check 1 -> In Progress", end="\r")
        wc1 = self.makeFolder("Test")
        print("Write Check 1 -> {}         ".format(wc1))

        time.sleep(1)

        print("Write Check 2 -> In progress", end="\r")
        localFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "UploadFileTest.txt")  # noqa
        wc2 = self.copyFile("Test", localFile)
        print("Write Check 2 -> {}         ".format(wc2))

        time.sleep(1)

        print("Write Check 3 -> In Progress", end="\r")
        wc3 = self.writeFile("Test", "grid.txt", "H E L L O")
        print("Write Check 3 -> {}         ".format(wc3))

        complete = [
            wc1 == "Success",
            wc2 == "Success",
            wc3 == "Success"
        ]
        if complete[0] and complete[1] and complete[2]:
            return True
        else:
            print("Error whilst completing a task, Please try again")

    def makeFolder(self, game):
        path = os.path.join(self.path, game)
        if os.path.exists(path):
            self.newgame = game + '-' + ''.join(random.choice(string.ascii_letters) for _ in range(10))  # noqa
            path = os.path.join(self.path, self.newgame)
        try:
            os.mkdir(path)
            return "Success"
        except FileNotFoundError:
            return "Failed"

    def copyFile(self, game, file):
        if os.path.isfile(file):
            gameDir = None
            if not self.newgame:
                gameDir = os.path.join(self.path, game)
            else:
                gameDir = os.path.join(self.path, self.newgame)
            if os.path.isdir(gameDir):
                shutil.copy(file, gameDir)
                return "Success"
            else:
                return "specified game directory is not a path!"
        else:
            return "Game file given is not a file"

    def writeFile(self, game, file, data):
        try:
            if not self.newgame:
                with open(os.path.join(os.path.join(self.path, game), file), "w+") as gameData:  # noqa
                    gameData.write(json.dumps(data))
            else:
                with open(self.newgame + file, "w+") as file:
                    file.write(json.dumps(data))
        except FileNotFoundError:
            return "Folder to hold file was not found"
        return "Success"

    def _readCheck(self):
        print("Read Check 1 -> In Progress      ", end="\r")
        rc1 = self.readFile("Test", "grid.txt")
        print("Read Check 1 -> {}         ".format(rc1))

        complete = [
            rc1 == "Success"
        ]
        if complete[0]:
            return True
        else:
            print("Error whilst completing a task, Please try again")

    def readFile(self, game, file):
        try:
            if not self.newgame:
                with open(os.path.join(os.path.join(self.path, game), file), "r") as gameData:  # noqa
                    return json.loads(gameData.read())
            else:
                with open(self.newgame + file, "r") as file:
                    return json.loads(file.read())
        except FileNotFoundError:
            return "Failed -> Folder not found"

    def saveCreation(data, name, users):
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
                UpdateFile(data, "Saves/{}/{}".format(name, users[0]), "grid")
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

class board:
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
    n = save(input("Path of files: "))
