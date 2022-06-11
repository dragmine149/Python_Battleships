import CreateInfo as Create
import newSave
import Functions
from Functions import Print
import os


class Process:
    def __init__(self, path, name=None):
        self.path = path
        self.name = name
        if name is not None:
            # Loads the save system
            self.saveSystem = newSave.save({
                'name': name,
                'path': os.path.join(path, name)
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

            print("Grid:")
            Functions.board.DisplayBoard(ships)
            print("\nShots:")
            Functions.board.DisplayBoard(shots)
            print("----------------------------")

        print("\n\n")
        input("Please press enter when you are ready to continue")
        return True

    # Check if the game has been won, If so, print output
    def winView(self, path, name=None, external=False):
        Functions.clear()
        winner = self.saveSystem.readFile("win")

        Print("Game Over!!!", 'green')
        Print("Winner: {}".format(winner), "cyan")

        def noFunc():
            return None

        return Functions.check("Would you like to view the boards? (y or n): ",
                               returnFunc=(self.viewBoards, noFunc)).getInput("ynCheck")  # noqa E501

    # Gets the inputs and return the game result info thing
    def Inputs(self, external=False, create=False):
        if create:
            return self.__create()
        # if not external:

        # get users
        self.users = self.saveSystem.ls(True)

        # checks if game already won
        if self.saveSystem.CheckForFile("win"):
            return self.winView(self.path, self.name, external)

        # Checks if users have placed their ships
        placed = [False, False]
        for userIndex in range(len(self.users)):
            user = self.users[userIndex]
            print({"User": user})
            if self.saveSystem.CheckForFile("{}/shots".format(user)):
                placed[userIndex] = True

        # Checks for multiplayer support
        multi = self.saveSystem.readFile("multi")

        return self.name, self.users, placed, self.path, multi
        # # Path, name (id, name)
        # # Path usless
        # for item in path:
        #     # Errors... why?
        #     if item['name'] == name:
        #         saveLoc = item['id']
        #         name = item
        #         break
        #
        # usersInfo = save.save(name['id']).ListDirectory()
        # multiPlayerId = None
        # newUsers = []
        # for user in usersInfo:
        #     if user['name'] == "multi":
        #         multiPlayerId = user['id']
        #     elif user['name'] != "turn":
        #         newUsers.append(user)
        # print({'1. usersInfo': newUsers})
        # users = Functions.RemoveNonGames(usersInfo)
        #
        # print({'users': users})
        # print({'usersInfo': usersInfo})
        # print({'multiPlayerId': multiPlayerId})
        # placed = [False, False]
        #
        # for user in range(len(newUsers)):
        #     Files = save.save(newUsers[user]['id']).ListDirectory()
        #     for file in Files:
        #         if file['name'] == "ships":
        #             placed[user] = True
        #             break
        #
        # print({'placed': placed})
        #
        # multi = False
        # if multiPlayerId is not None:
        #     if not os.path.exists("Saves/.Temp/{}".format(name['id'])):
        #         os.mkdir("Saves/.Temp/{}".format(name['id']))
        #
        #     multi = save.save(name['id'], data={
        #         'name': 'Saves',
        #         'file': 'multi'
        #     }).readFile({
        #         'name': multiPlayerId
        #     })
        #     print({'multi': multi})
        #     if multi:
        #         save.save("Saves").Delete("Saves/.Temp/{}".format(name['id']))  # noqa
        #
        # return name['name'], newUsers, placed, saveLoc, multi  # noqa
