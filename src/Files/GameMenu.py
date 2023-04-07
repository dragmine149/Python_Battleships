from colorama import Fore
from PythonFunctions.Message import Message
from PythonFunctions.CleanFolderData import Clean
from PythonFunctions.Check import Check
from PythonFunctions.TerminalDisplay import Display
from PythonFunctions.Save import save
from PythonFunctions import Run

from Files import ProcessInput as pi


class Menu:
    def __init__(self) -> None:
        self.msg = Message()
        self.chk = Check()
        self.dis = Display()
        self.save = save()
        self.cln = Clean()
        self.path = self.save.Read('Data/Settings',
                                   encoding=self.save.encoding.BINARY).get('path')
        self.header = None

    def GetGameInfo(self):
        Run.Mark("get game start")

        # sets the message so the user knows where it is better
        msg = "Local"
        if self.path != "Saves":
            msg = "External"

        # alvalible options
        options = {}
        self.gameList = self.cln.clean(self.save.ListFolder(self.path))
        self.gameList.sort()

        # Winner check

        Run.Mark("load game start")
        for gameIndex, game in enumerate(self.gameList):
            print(f"Checking: {game}")
            Run.Mark("win check")

            completed = ''
            winner = self.save.Read(f'{self.path}/{game}/win',
                                    encoding=self.save.encoding.BINARY)
            if winner != '' and winner is not False:
                completed = f'{Fore.GREEN}(Winner: {winner}){Fore.RESET}'

            Run.Mark("win check end")

            # The message showing the winner check time.
            timeDiff = Run.CompareMarkers("win check", "win check end", 2)
            loadtimeMsg = f'({timeDiff}s winner check time)'

            # the overall message of that row.
            options[gameIndex + 1] = (self.selectGame,
                                      f"{game} {completed} {loadtimeMsg}",
                                      gameIndex)

        Run.Mark("load game end")

        # Works out how long it took to load the files, mainly debug but
        Run.Mark("get game end")
        totalloadtime = Run.CompareMarkers("get game start", "get game end", 2)
        winloadtime = Run.CompareMarkers("load game start", "load game end",
                                         2)
        loadtimeMessage = f"{totalloadtime}s total ({winloadtime}s winner check)"

        self.header = f"Games found in: {self.path} ({msg}) (Load Time: {loadtimeMessage})"
        self.dis.SetOptions(options)

    def deleteGame(self, _):
        gameIndex = None
        while gameIndex != "":
            gameIndex = self.chk.getInput(
                "Please enter game number to delete (leave blank to stop): ",
                self.chk.ModeEnum.int,
                lower=0,
                higher=len(self.gameList))

            if gameIndex is None:
                return

            game = self.gameList[gameIndex - 1]
            self.save.RemoveFolder(f'{self.path}/{game}')

    def back(self, _):
        return "Returned"

    def changePath(self, _):
        self.path = input("Please enter the new path location: ")

    def selectGame(self, pos):
        return pi.Process(self.path, self.gameList[pos]).Inputs()

    def MakeDisplay(self):
        self.dis.AddOption((self.back, "Back"), index=0)
        self.dis.AddOption((self.changePath, "Change Path"), index=-1)
        self.dis.AddOption((self.deleteGame, "Delete Game"), index=-2)

    def main(self):
        self.GetGameInfo()
        self.MakeDisplay()
        self.msg.clear()
        result = None
        while result is None:
            self.dis.ShowHeader(text=self.header)
            result = self.dis.ShowOptions(useList=True)
            if result is not None:
                return result
