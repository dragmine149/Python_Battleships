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

    def LoadGames(self, path):
        message = "Games found on disk: "
        if isinstance(path, list):
            message = "Games found on external location: "
        print(message)

        newList = Functions.RemoveNonGames(path)
        for game in range(len(newList)):
            print("{}: {}".format(game + 1, newList[game]))
        # Cannot indent otherwise formating is broken
        print("""
Other Options:
-2: Remove Game (Deletes ALL files)
-1: Goes back to main screen
 0: Loads external game\n""")

    def GameRangeCheck(self, value, list):
        if value >= 0 and value <= len(list):
            return True
        elif value == -1:
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
                        delGame = Functions.check("Please enter game to delete (-1 to stop): ", self.LoadGames, self.path, self.GameRangeCheck, Functions.RemoveNonGames(self.path)).InputDigitCheck()
                        if delGame != -1:
                            save.save(self.path).Delete(os.path.join(self.path, Functions.RemoveNonGames(self.path)[delGame -1]))
                            delGame = None
                    self.game = None
                if self.game == -1:
                    self.choice = None
                    self.game = None
                    return
                if self.game == 0:
                    self.game = None
                    Functions.clear()
                    external = None
                    while not external:
                        external = input("Please enter location of storage: ").rstrip().replace('"', '')  # noqa
                        if external != "":
                            # Windows has different file structure AAA
                            if platform.system() != "Windows":
                                external = external.replace("\\", "")

                            # Normal file check
                            if external.find("\\") > -1 or external.find("/") > -1:  # noqa
                                # Directory check
                                if not os.path.isdir(external):
                                    external = None
                                    Functions.clear(2, "Provided directory is not a directory")  # noqa
                                else:
                                    self.path = external
                            else:
                                # Google api check
                                self.path = drive.Api(external).ListFolder()
                                apiExternal = True

                                # Reset if error in loading...
                                if self.path == "Error":
                                    self.path = "Saves"
                        else:
                            external = self.path
                            self.path = "Saves"
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
            if self.choice is not None:
                return result

    def OptionsRead(self):
        with open("Options.txt", "r") as options:
            lines = options.readlines()
            for line in lines:
                print(line, end="")


if __name__ == "__main__":
    game = game()
    gameInfo = game.GetInput()
    print(gameInfo)
