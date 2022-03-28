import os
import time
import shutil
import random
import string
import json
import Functions
import sys
import platform
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class save:
    # path = saves dir on network
    def __init__(self, path, json=True):
        self.path = path.rstrip().replace('"', '')
        if platform.system() != "Windows":
            self.path = self.path.replace("\\", "")
        self.Api = None
        if self.path.find('/') == -1 and self.path.find("\\") == -1 and not self.path == "Saves":  # noqa
            # Load google api
            try:
                import DriveApi
                if not os.path.exists("Saves/Google"):
                    os.mkdir("Saves/Google")

                self.Api = DriveApi.Api(self.path)
                if not self.Api.Test():
                    sys.exit("Something failed in the google drive api test...")  # noqa
                self.Folder = None
            except ModuleNotFoundError:
                sys.exit("Google drive api not installed. Please install...")
        self.newgame = None
        self.last = None
        # Json is not always needed to decode files
        # and can break files somethimes
        self.json = json
        # Bypasses testing if local file.
        time.sleep(1)
        if self.path != "Saves":
            self.Test()

    def _writeTestFile(self):
        with open('Tests/Path.txt', 'w+') as f:
            f.write(self.path)

    def Test(self):
        if self.Api:
            self.TestDriverFiles = []
        try:
            with open('Tests/Path.txt', 'r+') as f:
                if self.path == f.read():
                    return True  # skip the test if that path has been tested recently  # noqa
                else:
                    self._writeTestFile()
        except FileNotFoundError:
            self._writeTestFile()

        if platform.system() != "Windows":
            os.system("clear")
        else:
            os.system("cls")
        print("Loading network...")
        # Tries to write to server
        writeCheck = self._writeCheck()

        # Tries to read from server
        readCheck = self._readCheck()

        # Tries to remove excess files
        print("Removing files")
        try:
            if not self.Api:
                if self.newgame:
                    shutil.rmtree(os.path.join(self.path, self.newgame))
                else:
                    shutil.rmtree(os.path.join(self.path, "Test"))
            else:

                shutil.rmtree("Saves/Google/Test")
                print(self.TestDriverFiles)
                for file in self.TestDriverFiles:
                    self.Api.DeleteData(file)
                # Delete Data.

            print(os.path.exists('Test'))
            if os.path.exists('Test'):
                os.system('rm Test')

        except FileNotFoundError:
            print("Failed to remove files created")
        self.newgame = None
        print("\n\n")

        # Output results
        if writeCheck and readCheck:
            print("Client can access server files. Everything is ready.")
        elif writeCheck:
            print("Client can write to server but not read... how?")
            sys.exit("Required permission missing: Read.")
        elif readCheck:
            print("Client can read server data but not write.")
            sys.exit("Required permission missing: Write.")
        else:
            print("Client can not read or write to server.")
            sys.exit("""Required permissions missing: Read + Write.
            Is server down?""")

    def _writeCheck(self):
        print("Write Check 1 -> In Progress", end="\r")
        wc1 = self.makeFolder("Test")
        print("Write Check 1 -> {}         ".format(wc1))

        if self.Api is None:
            print("Write Check 2 -> In progress", end="\r")
            localFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "UploadFileTest.txt")  # noqa
            wc2 = self.copyFile("Test", localFile)
            print("Write Check 2 -> {}         ".format(wc2))

        print("Write Check 3 -> In Progress", end="\r")
        wc3 = self.writeFile("Test", "grid", "H E L L O")
        print("Write Check 3 -> {}         ".format(wc3))

        if self.Api is None:
            complete = [
                wc1 == "Success",
                wc2 == "Success",
                wc3 == "Success"
            ]
            if complete[0] and complete[1] and complete[2]:
                return True
            else:
                print("Error whilst completing a task, Please try again")
        else:
            complete = [
                wc1 == "Success",
                wc3 == "Success"
            ]
            if complete[0] and complete[1]:
                return True
            else:
                print("Error whilst completing a task, Please try again")

    def makeFolder(self, game):
        if self.Api:
            self.Folder = self.Api.UploadData({
                "name": game,
            }, True)['id']
            if isinstance(self.TestDriverFiles, list):
                self.TestDriverFiles.append(self.Folder)
            if self.Folder:
                return "Success"
            else:
                return "Failed to create folder"
        else:
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
        if self.Api:
            with open(game, "w+") as f:  # noqa
                f.write(data)
            id = self.Api.UploadData({
                'name': file,
                'path': game,
                'folder': self.Folder
            })['id']
            if isinstance(self.TestDriverFiles, list):
                self.TestDriverFiles.append(id)
            self.last = id
            if not os.path.exists("ApiFiles/Google"):
                os.mkdir("ApiFiles/Google")
            if not os.path.exists("ApiFiles/Google/{}".format(game)):
                os.mkdir("ApiFiles/Google/{}".format(game))
            with open("ApiFiles/Google/{}".format(os.path.join(game, file)), "w+") as write:  # noqa
                write.write(str(id))
        else:
            try:
                if not self.newgame:
                    newPath = os.path.join(os.path.join(self.path, game), file)
                    with open(newPath, "w+") as gameData:  # noqa
                        if self.json:
                            gameData.write(json.dumps(data))
                        else:
                            gameData.write(data)
                else:
                    newPath = os.path.join(self.path, os.path.join(self.newgame, file))  # noqa
                    with open(newPath, "w+") as file:
                        if self.json:
                            file.write(json.dumps(data))
                        else:
                            file.write(data)
            except FileNotFoundError:
                return "Folder to hold file was not found"
        return "Success"

    def _readCheck(self):
        print("Read Check 1 -> In Progress      ", end="\r")
        rc1 = self.readFile("Test", "grid", self.last)
        print("Read Check 1 -> {}         ".format(rc1))

        complete = [
            rc1 != "Failed -> Folder not found"
        ]
        if complete[0]:
            return True
        else:
            print("Error whilst completing a task, Please try again")

    def readFile(self, game=None, file=None, id=None):
        if self.Api:
            with open("ApiFiles/Google/{}".format(os.path.join(game, file)), "r") as downlaoded:  # noqa
                return downlaoded.read()

            print(game)
            splitGame = game.split("/")
            print(splitGame)
            for split in range(len(splitGame)):
                print(split)
                if split != len(splitGame):
                    path = None
                    if split > 0:
                        path = splitGame[:split-1] + splitGame[split]

                    if os.path.exists("Saves/Google/{}".format(path)):
                        os.mkdir(path)
            if not os.path.exists("Saves/Google/{}".format(game)):
                os.mkdir("Saves/Google/{}".format(game))
            result = self.Api.DownloadData({
                'name': id,
                'path': "Saves/Google/{}".format(os.path.join(game, file))
            }, False)
            if result:
                with open("Saves/Google/{}".format(os.path.join(game, file)), "r") as downlaoded:  # noqa
                    return downlaoded.read()
            else:
                return "Failed -> Folder not found"

        try:
            if not self.newgame:
                with open(os.path.join(os.path.join(self.path, game), file), "r") as gameData:  # noqa
                    if self.json:
                        return json.loads(gameData.read())
                    else:
                        return gameData.read()
            else:
                newPath = os.path.join(self.path, os.path.join(self.newgame, file))  # noqa
                with open(newPath, "r") as file:
                    if self.json:
                        return json.loads(file.read())
                    else:
                        return file.read()
        except FileNotFoundError:
            return "Failed -> Folder not found"

    def saveCreation(self, data, name, users, twoPlayer=None):
        Functions.clear(1)
        if not self.Api:
            print("Saving data")
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            if os.path.exists("{}/{}".format(self.path, name)):
                print("Please enter a name that has not already been used.")
                Functions.clear(1)
                return "E"
            else:
                os.mkdir("{}/{}".format(self.path, name))
                os.mkdir("{}/{}/{}".format(self.path, name, users[0]))
                print("Made dir -> {}/{}/{}".format(self.path, name, users[0]))
                if os.path.exists("{}/{}/{}".format(self.path, name, users[0])):  # noqa
                    print(self.writeFile("{}/{}".format(name, users[0]), "grid", data)) # noqa
                    os.mkdir("{}/{}/{}".format(self.path, name, users[1]))
                    print("Made dir -> {}/{}/{}".format(self.path, name, users[1]))  # noqa
                    if os.path.exists("{}/{}/{}".format(self.path, name, users[1])):  # noqa
                        print(self.writeFile("{}/{}".format(name, users[1]), "grid", data))  # noqa
                        if twoPlayer:  # whose turn it is.
                            print(self.writeFile("{}".format(name), "multi", users[0]))  # noqa
                        return True
                    else:
                        Functions.clear(1, "(2) Error in path creation... (invalid characters?)")  # noqa
                        shutil.rmtree("{}/{}".format(self.path, name))
                        return False
                else:
                    Functions.clear(1, "(1) Error in path creation... (invalid characters?)")  # noqa
                    shutil.rmtree("{}/{}".format(self.path, name))
                    return False
        else:
            with open("Temp-txt", "w+") as f:
                f.write(json.dumps(data))
            with open("Temp-multi-txt", "w+") as f:
                f.write(users[0])
            mainFolder = self.Api.UploadData({'name': name, 'path':'', 'folder': self.path}, True)  # noqa
            user1 = self.Api.UploadData({'name': users[0], 'path': '', 'folder': mainFolder['id']}, True)  # noqa
            user2 = self.Api.UploadData({'name': users[1], 'path': '', 'folder': mainFolder['id']}, True)  # noqa
            if twoPlayer:
                self.Api.UploadData({'name': 'multi', 'path': 'Temp-multi-txt', 'folder': mainFolder['id']}, False)  # noqa
            self.Api.UploadData({'name': 'grid', 'path': 'Temp-txt', 'folder': user1['id']}, False)  # noqa
            self.Api.UploadData({'name': 'grid', 'path': 'Temp-txt', 'folder': user2['id']}, False)  # noqa
            os.system('rm Temp-txt')
            os.system('rm Temp-multi-txt')
            return True

    def ListDirectory(self, path=None):
        if self.Api:
            return self.Api.ListFolder()
        else:
            if path:
                return os.listdir(path)
            else:
                return os.listdir(self.path)


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
    os.system('rm Tests/Path.txt')
    n = save("1jgyfEG0R76adWlnyzqDU030ps-mk4M20")
    n.ListDirectory()
