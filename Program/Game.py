import os
import sys
import Functions
import ProcessInput as pi
import platform
import Save as save
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class game:
    def __init__(self):
        Functions.clear()
        self.choice = None
        self.game = None
        self.path = "Saves"
        self.external = "Saves"

    def LoadGames(self, path):
        message = "Games found on disk: "
        if isinstance(path, list):
            message = "Games found on external location ({}): ".format(self.external)  # noqa
        print(message)

        newList = Functions.RemoveNonGames(path)
        for game in range(len(newList)):
            print("{}: {}".format(game + 1, newList[game]))
        # Cannot indent otherwise formating is broken
        print("""
Other Options:
-2: Remove Game (Deletes ALL files)
-1: Loads external game
 0: Goes back to main screen
""")

    def GameRangeCheck(self, value, list):
        if value >= 0 and value <= len(list):
            return True
        if value == -1:
            return True
        return False

    def ProcessChoice(self):
        if self.choice == 0:
            sys.exit("Thank you for playing")
        if self.choice == 1:
            apiExternal = False
            while not self.game:
                Functions.clear()
                self.game = Functions.check("Enter game number to load: ", self.LoadGames, self.path, self.GameRangeCheck, Functions.RemoveNonGames(self.path)).InputDigitCheck()  # noqa
                if self.game == -2:
                    delGame = None
                    while not delGame:
                        Functions.clear()
                        delGame = Functions.check("Please enter game to delete (-1 to stop): ", self.LoadGames, self.path, self.GameRangeCheck, Functions.RemoveNonGames(self.path)).InputDigitCheck()  # noqa
                        if delGame != -1:
                            deletePath = None
                            if apiExternal:
                                deletePath = Functions.RemoveNonGames(self.path)[delGame - 1]  # noqa
                                for item in self.path:
                                    if item['name'] == deletePath:
                                        result = save.save(self.external).Delete(item['id'])  # noqa

                                        # Reset ui to show new list instead of old  # noqa
                                        self.path = save.save(self.external).ListDirectory(dir=True)  # noqa
                                        break
                            else:
                                deletePath = os.path.join(self.path, Functions.RemoveNonGames(self.path)[delGame - 1])  # noqa
                                save.save(self.path).Delete(deletePath)  # noqa
                            delGame = None
                    self.game = None
                if self.game == 0:
                    self.choice = None
                    self.game = None
                    return
                if self.game == -1:
                    self.game = None
                    Functions.clear()
                    self.external = None
                    while not self.external:
                        try:
                            self.external = input("Please enter location of storage (leave blank to go back): ").rstrip().replace('"', '')  # noqa
                            if self.external != "":
                                # Windows has different file structure AAA
                                if platform.system() != "Windows":
                                    self.external = self.external.replace("\\", "")  # noqa

                                # Normal file check
                                if self.external.find("\\") > -1 or self.external.find("/") > -1:  # noqa
                                    # Directory check
                                    if not os.path.isdir(self.external):
                                        self.external = None
                                        Functions.clear(2, "Provided directory is not a directory")  # noqa
                                    else:
                                        self.path = self.external
                                else:
                                    # Google api check
                                    self.path = save.save(self.external).ListDirectory(dir=True)  # noqa
                                    apiExternal = True

                                    # Reset if error in loading...
                                    if self.path == "Error":
                                        self.path = "Saves"
                                        Functions.clear(2)
                            else:
                                self.external = self.path
                                self.path = "Saves"
                                self.external = "Saves"
                        # Easy way to redo just in case mess up.
                        except KeyboardInterrupt:
                            self.external = None
                            Functions.clear()
            return pi.Process().Inputs(self.path, name=Functions.RemoveNonGames(self.path)[self.game - 1], external=apiExternal)  # noqa
        if self.choice == 2:
            return pi.Process().Inputs(self.game, create=True)
        if self.choice == 3:
            print("Comming soon...")

    def GetInput(self):
        while not self.choice:
            Functions.clear()
            self.choice = Functions.check("Your Choice (number): ", self.OptionsRead, None, Functions.NumberRangeCheck, 3).InputDigitCheck()  # noqa
            result = self.ProcessChoice()
            if result is None:
                self.choice = None
                continue
            return result

    def OptionsRead(self):
        print("""0. Quit
1. Load Games
2. Make New Game
3. Settings""")


if __name__ == "__main__":
    game = game()
    gameInfo = game.GetInput()
    print(gameInfo)
