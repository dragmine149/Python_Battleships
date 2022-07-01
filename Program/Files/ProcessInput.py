import importlib
import os
Create = importlib.import_module('Files.CreateInfo')
newSave = importlib.import_module('Files.newSave')
Functions = importlib.import_module('Files.Functions')
readchar = importlib.import_module('Files.readchar.readchar')
Print = Functions.Print


class Process:
    def __init__(self, path, name=None):
        self.path = path
        self.name = name
        if name is not None:
            # Loads the save system
            self.saveSystem = newSave.save({
                'name': name,
                'path': path
            })

    def __create(self):
        Data = Create.CreateData(self.path, self.name).getOption()
        # checks if no data before trying to return chaos
        if Data is None:
            return
        [name, users, Location, online] = Data
        return name, users, [False, False], Location, online

    def viewBoards(self):
        print("----------------------------")
        for user in self.users:
            print({"User": user})
            boardSystem = newSave.save({
                'name': self.name,
                'path': os.path.join(self.path, self.name),
                'Json': True
            })
            ships = boardSystem.readFile(os.path.join(user, "ships"))
            shots = boardSystem.readFile(os.path.join(user, "shots"))

            Functions.board.MultiDisplay([ships, shots])
            print("----------------------------")

        print("\n\nPlease press any key when you are ready to move on")
        readchar.readchar()
        return True

    # Check if the game has been won, If so, print output
    def winView(self, winner):
        Functions.clear()

        Print("Game Over!!!", 'green')
        Print("Winner: {}".format(winner), "cyan")

        def noFunc():
            return None

        return Functions.check("Would you like to view the boards? (y or n): ",
                               returnFunc=(self.viewBoards, noFunc)).getInput("ynCheck")  # noqa E501

    # Gets the inputs and return the game result info thing
    def Inputs(self, create=False):
        if create:
            return self.__create()
        # get users
        self.users = self.saveSystem.ls(True, folder=self.name)

        # Convert google drive list into normal data
        if isinstance(self.users[0], dict):
            newUsers = []
            for user in self.users:
                newUsers.append(user['name'])
            self.users = newUsers

        self.users.sort()

        gameData = newSave.save({
            'name': self.name,
            'path': self.path
        }).readFile("GameData", joint=True)

        # checks if game already won
        if gameData["win"] != '':
            return self.winView(gameData["win"])

        # Checks if users have placed their ships
        placed = [False, False]
        for userIndex in range(len(self.users)):
            user = self.users[userIndex]
            print({"User": user})
            if self.saveSystem.CheckForFile("{}/{}/shots".format(self.name, user)):  # noqa E501
                placed[userIndex] = True
            print({"Placed": placed[userIndex]})

        return self.name, self.users, placed, self.path, gameData["multi"]
