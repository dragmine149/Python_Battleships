import os

from PythonFunctions.Save import save
from Files import CreateInfo as Create
from Files import Settings


class Process:
    def __init__(self, path, name=None):
        print("Processing...")
        self.path = path
        self.name = name
        self.sv = save()

    def __create(self):
        self.path = Settings.request(["path"])[0]
        Data = Create.CreateData(self.path, self.name).getOption()
        # checks if no data before trying to return chaos
        if Data is None:
            return
        [name, users, Location, online] = Data
        return name, users, [False, False], Location, online

    def viewBoards(self):
        data = []
        gameInfo = Save.save({
            'path': self.path
        })
        gameInfo.ChangeDirectory(self.name)
        
        for user in self.users:
            print({"User": user})
            gameInfo.ChangeDirectory(user)

            ships = gameInfo.readFile("ships")
            shots = gameInfo.readFile("shots")
            data.append([ships, shots])
            
            gameInfo.ChangeDirectory('..')

        print('-' * Functions.os.get_terminal_size().columns)
        for user in data:
            Functions.board.MultiDisplay([user[0], user[1]],
                                         ["ships", "shots"])
            print('-' * Functions.os.get_terminal_size().columns)

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
        self.saveSystem.ChangeDirectory(self.name)
        # get users
        self.users = self.saveSystem.ls()

        # Convert google drive list into normal data
        if isinstance(self.users[0], dict):
            newUsers = []
            for user in self.users:
                newUsers.append(user['name'])
            self.users = newUsers

        self.users.sort()
        
        blackList = ['GameData', 'win']
        newList = []
        print({'original': self.users})
        for i in range(len(self.users)):
            if self.users[i] not in blackList:
                newList.append(self.users[i])
        
        self.users = newList
        
        print({'new': self.users})
        
        gameInfo = Save.save({
            'path': self.path
        })
        gameInfo.ChangeDirectory(self.name)
        gameData = gameInfo.readFile("GameData")

        # checks if game already won
        if gameInfo.CheckForFile('win'):
            return self.winView(gameInfo.readFile('win')["win"])

        # Checks if users have placed their ships
        placed = [True, True]
        for userIndex in range(len(self.users)):
            user = self.users[userIndex]
            print({"User": user})
            placeData = Save.save({
                'path': self.path
            }).readFile('{}/placedData'.format(os.path.join(self.name, user)))

            for ship in placeData:
                if not placeData[ship]:
                    placed[userIndex] = False

        return self.name, self.users, placed, gameInfo.GetPath(), gameData["multi"]
