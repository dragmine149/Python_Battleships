import os
import importlib
import time
import colorama

from PythonFunctions.Save import save
from PythonFunctions.Message import Message
from PythonFunctions.Check import Check

Menu = importlib.import_module('Files.GameMenu')
pi = importlib.import_module('Files.ProcessInput')
Settings = importlib.import_module('Files.Settings')


class Loader:
    def __init__(self):
        # loads
        print("Loading games...")
        self.save = save()
        self.msg = Message()
        self.chk = Check()

        self.game = None
        path = Settings.request(["path"])[0]
        self.games = path
        self.path = path
        self.gameList = None

    # deletes a game
    def deleteGame(self):
        delGameIndex = None
        while delGameIndex is None:
            self.msg.clear()
            info, options, choices, external = self.getGames()
            ui = info + "\n" + options
            print(ui)
            delGameIndex = self.chk.getInput(
                "Please enter game number to delete (leave blank to stop): ",
                self.chk.ModeEnum.int, lower=0, higher=self.gameList)
            if delGameIndex is not None:
                deletePath = self.gameList[delGameIndex - 1]
                # Difference from api and normal
                pathToDelete = os.path.join(self.path, deletePath)
                if self.apiExternal:
                    pathToDelete = deletePath

                self.save.RemoveFolder(pathToDelete)
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

    def gameMenuInfo(self, optionsText):
        if optionsText == "":
            optionsText = f"""{colorama.Fore.RED}No games found!
Please reload by giving no input, Choose a different location or make a game.
{colorama.Fore.RESET}"""

        options = {
            -2: (self.changePath, "Change Path"),
            -1: (self.deleteGame, "Delete Game"),
            0: (self.back, "Back")
        }
        return optionsText, options

    def getGames(self):
        print('loading Games')
        self.games, self.path, LoadTimeMsg = Settings.request(
            ['path', 'path', 'loadTimes'])
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

        # Winner check
        gameData = Save.save({
            'name': '',
            'path': self.path
        })

        LoadTime = time.time()
        for gameIndex in range(len(self.gameList)):
            game = self.gameList[gameIndex]  # load the current game name
            print(f"Checking: {game}")
            winnerLoadTime = time.time()  # start of winner check time

            completed = ''
            # change to the game directory.
            result = gameData.ChangeDirectory(game)
            if result:
                # check if winner file is there
                winner = gameData.CheckForFile('win', False)
                if winner:
                    # reads winner if found
                    winner = gameData.readFile("win")["win"]  # reads winner
                    if winner != '' and winner is not False:
                        completed = '{}(Winner: {}){}'.format(c('green'),
                                                              winner,
                                                              c())  # adds winner to list

                winnerEndLoadTime = time.time()  # end of winner check time
                loadtimeMsg = ''
                if LoadTimeMsg:
                    # The message showing the winner check time.
                    loadtimeMsg = '({}s winner check time)'.format(
                        round(winnerEndLoadTime - winnerLoadTime, 2))

                # the overall message of that row.
                options += "{}: {} {} {}\n".format(gameIndex + 1, game,
                                                   completed, loadtimeMsg)
                gameData.ChangeDirectory('..')
            else:
                Functions.Print(
                    "Failed to switch to directory: {}!".format(game), "red", "bold")

        LoadEndTime = time.time()

        # Works out how long it took to load the files, mainly debug but
        loadtimeEnd = time.time()
        loadtime = round(loadtimeEnd - loadtimeStart, 2)
        lts = round(LoadEndTime - LoadTime, 2)
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
