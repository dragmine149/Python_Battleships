import os
import sys
import Functions
import ProcessInput as pi
import platform
import Save as save
import GameMenu
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class game:
    def __init__(self):
        # Functions.clear()
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
            return self.SelectGame()
        if self.choice == 2:
            return pi.Process().Inputs(self.game, create=True)
        if self.choice == 3:
            print("Comming soon...")

    def GetInput(self):
        while not self.choice:
            Functions.clear()
            self.choice = Functions.check("Your Choice (number): ", self.Options, None, Functions.NumberRangeCheck, 3).InputDigitCheck()  # noqa
            result = self.ProcessChoice()
            if result is None:
                self.choice = None
                continue
            return result

    def Options(self):
        print("""0. Quit
1. Load Games
2. Make New Game
3. Settings""")


if __name__ == "__main__":
    Game = game()
    gameInfo = Game.GetInput()
    print(gameInfo)
