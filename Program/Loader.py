import Functions
import GameMenu as Menu
import newSave
import os
import ProcessInput as pi
import Settings


class Loader:
    def __init__(self):
        # loads
        print("Loading games...")
        self.game = None
        path = Settings.request("path")
        self.games = path
        self.path = path
        self.apiExternal = False
        self.gameList = None

    # deletes a game
    def deleteGame(self):
        delGame = None
        while not delGame:
            Functions.clear()
            delGame = Functions.check("Please enter game to delete (-1 to stop): ", self.LoadGames, self.path, self.GameRangeCheck, Functions.RemoveNonGames(self.path)).InputDigitCheck()  # noqa
            if delGame != -1:
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
                deletePath = os.path.join(self.path, Functions.RemoveNonGames(self.path)[delGame - 1])  # noqa
                newSave.save({
                            'name': '',
                            'path': self.path}).Delete(deletePath)
                delGame = None
        self.game = None

    # go back to previous menu
    def back(self):
        return "Returned"

    def changePath(self):
        data = Functions.changePath()
        self.game = None
        self.games, self.path, self.apiExternal = data
        return "Changed"

    def getGames(self):
        # sets the message so the user knows where it is better
        msg = "Local"
        if self.path != "Saves":
            msg = "External"
        if self.apiExternal:
            msg = "Google Drive"

        # banner information
        info = """--------------------------------------------------------------------
Games found in: {} ({})
--------------------------------------------------------------------
""".format(self.path, msg)

        # alvalible options
        options = ""
        self.gameList = Functions.RemoveNonGames(self.games)
        self.gameList.sort()

        for game in range(len(self.gameList)):
            options += "{}: {}\n".format(game + 1, self.gameList[game])

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
        return info, options, choices, external

    def loadMenu(self):
        # generates menu
        self.menu = Menu.menu(self.getGames, back="Back")
        inResult = self.menu.getInput(values=(-2, len(self.gameList)))
        return inResult

    # returns data from loading the games
    def selectGame(self):
        while not self.game:
            Functions.clear()
            self.game = self.loadMenu()

            if self.game == "Returned":
                return "back"

            if not Functions.IsDigit(self.game):
                self.game = None

            if self.game is not None:
                pathInfo = self.gameList[self.game - 1]
                return pi.Process(self.path, pathInfo).Inputs(self.apiExternal)
