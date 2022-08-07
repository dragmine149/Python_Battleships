import os
import importlib
import time

Functions = importlib.import_module('Files.Functions')
Menu = importlib.import_module('Files.GameMenu')
Save = importlib.import_module('Files.Save')
pi = importlib.import_module('Files.ProcessInput')
Settings = importlib.import_module('Files.Settings')
colours = importlib.import_module('Files.colours')

c = colours.c


class Loader:
    def __init__(self):
        # loads
        print("Loading games...")
        self.game = None
        path = Settings.request("path")
        self.games = path
        self.path = path
        saveInfo = Save.save({
            'path': path
        })
        self.apiExternal = saveInfo._api
        self.gameList = None

    # deletes a game
    def deleteGame(self):
        delGameIndex = None
        while delGameIndex is None:
            Functions.clear()
            info, options, choices, external = self.getGames()
            ui = info + "\n" + options
            delGameIndex = Functions.check("Please enter game number to delete (-1 to stop): ", ui, (-1, len(self.gameList))).getInput()  # noqa E501
            if delGameIndex != -1:
                deletePath = None
                # if apiExternal:
                #     deletePath = Functions.RemoveNonGames(self.path)[delGame - 1]  # noqa
                #     for item in self.path:
                #         if item['name'] == deletePath:
                #             result = save.save(self.external).Delete(item['id'])  # noqa
                #
                #             # Reset ui to show new list instead of old  # noqa
                #             self.path = save.save(self.external).ListDirectory(dir=True)  # noqa
                #             break
                #     continue
                deletePath = self.gameList[delGameIndex - 1]
                Save.save({
                            'path': self.path}).Delete(os.path.join(self.path, deletePath))  # noqa E501
                delGameIndex = None
        self.game = None

    # go back to previous menu
    def back(self):
        return "Returned"

    def changePath(self):
        data = Functions.changePath()
        self.game = None
        self.games, self.path, self.apiExternal = data
        return "Changed"

    def gameMenuInfo(self, options):
        if options == "":
            options = c('r') + """No games found!
Please reload by giving no input, Choose a different location or make a game.
""" + c()

        def all(choice):
            Functions.Print('ALL OBJECT CALLED', 'green', 'bold')
            return choice

        choices = {
            "All": all,
            0: self.back,
            -1: self.deleteGame,
            -2: self.changePath
        }
        external = {
            -1: 'Delete Game',
            -2: 'Change Path'
        }
        return [options, choices, external]

    def getGames(self):
        print('loadinG Games')
        self.games = Settings.request("path")
        self.path = Settings.request("path")
        loadtimeStart = time.time()

        # sets the message so the user knows where it is better
        msg = "Local"
        if self.path != "Saves":
            msg = "External"
        if self.apiExternal:  # TODO: Fix
            msg = self.apiExternal.msg

        # banner information
        dashText = '-' * os.get_terminal_size().columns
        info = """{}
Games found in: {} ({}) (Load Time: +)
{}
""".format(dashText, self.path, msg, dashText)

        # alvalible options
        options = ""
        self.gameList = Functions.RemoveNonGames(self.games)
        self.gameList.sort()
        # print(self.gameList)

        LTS2 = time.time()
        # Adds (Winner: {winner}) to the list if the game has been completed.
        for game in range(len(self.gameList)):
            gTime = time.time()
            completed = ''
            try:
                # Checks if there is a winner
                winnerData = newSave.save({
                    'name': self.gameList[game],
                    'path': self.path
                })
                winner = winnerData.CheckForFile('win')
                if winner:

                    # reads winner if found
                    winner = winnerData.readFile("win", joint=True)["win"]

                if winner != '' and winner is not False:
                    completed = '(Winner: {})'.format(winner)
            except KeyError:
                completed = ''

            gTEnd = time.time()

            # Sorts out the individal load times            
            loadtimeMsg = ''
            if Settings.request('loadTimes'):
                loadtimeMsg = '({}s winner check time)'.format(round(gTEnd - gTime, 2))

            options += "{}: {} {} {}\n".format(game + 1, self.gameList[game],
                                               completed, loadtimeMsg)
        
        LTS2E = time.time()

        # Works out how long it took to load the files, mainly debug but
        loadtimeEnd = time.time()
        loadtime = round(loadtimeEnd - loadtimeStart, 2)
        lts = round(LTS2E - LTS2, 2)
        loadtimeMessage = "{}s total ({}s winner check)".format(loadtime, lts)

        info = info.replace('+', loadtimeMessage)
        options, choices, external = self.gameMenuInfo(options)
        return info, options, choices, external

    def loadMenu(self):
        # generates menu
        self.menu = Menu.menu(self.getGames, back="Back")
        inResult = self.menu.getInput(values=(-2, len(self.gameList)))
        return inResult

    # returns data from loading the games
    def selectGame(self):
        while not self.game:
            self.game = self.loadMenu()

            if self.game == "Returned":
                return "back"

            if not Functions.IsDigit(self.game):
                self.game = None

            if self.game is not None:
                pathInfo = self.gameList[self.game - 1]
                return pi.Process(self.path, pathInfo).Inputs()
