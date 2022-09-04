import importlib
import sys
import argparse
Functions = importlib.import_module('Files.Functions')
Save = importlib.import_module('Files.Save')
Settings = importlib.import_module('Files.Settings')


def praser():
    """Setsup the command line arguments.

    Returns:
        args (list): the arguments inputted via command line
    """
    parser = argparse.ArgumentParser(description="Battleships, in python in a python terminal.")  # noqa E501
    parser.add_argument('menu', default=-.5,
                        help="The menu or game to load",
                        metavar="Menu / Game Name", nargs='?')
    parser.add_argument('--delete',
                        help="Delete old game data.",
                        action='store_true')
    parser.add_argument('--save',
                        nargs=1,
                        help="Overwrite the save location")
    args = vars(parser.parse_args())
    return args

def command_options():
    """Takes the command lines arguments and translates them into commands

    Returns:
        int: The choice that you choice
    """
    args = praser()
    if args['save']:
        # Force updates the save location.
        Settings.Settings().updateSave('path', args['save'][0])
    
    if args['delete']:
        def yes():
            Save.save.delete('Saves')
            Save.save.delete('Data')
            sys.exit('Deleted old data. Please rerun')

        def no():
            sys.exit('Aborted!')

        Functions.check('Are you sure you want to delete all data?: ',
                        returnFunc=(yes, no)).getInput('ynCheck')

    r = Functions.IsDigit(args['menu'])
    print(r, args['menu'])

    if not r:
        sys.exit("Comming soon (Probably in Update 3)")

    return int(args['menu'])

class Choices:
    """Stores information about what each option does
    """
    def __init__(self):
        Loader = importlib.import_module('Files.Loader')
        pi = importlib.import_module('Files.ProcessInput')
        self.Loader = Loader.Loader()
        self.path = self.Loader.path
        self.Process = pi.Process(self.path)

    # doesn't really generate, hard coded list
    def generate(self):
        return {
            1: self.selectGame,
            2: self.makeGame,
            3: self.settings,
            4: self.quit,
        }

    def quit(self):
        sys.exit("Thank you for playing")

    def selectGame(self):
        self.Loader.game = None
        result = self.Loader.selectGame()
        return result

    def makeGame(self):
        self.path = self.Loader.path
        return self.Process.Inputs(create=True)

    def settings(self):
        result = Settings.Settings().showDisplay()
        return result

def Main():
    # goes into menu
    result = command_options() or -0.5

    Display = importlib.import_module('Files.Display')

    # Delete temparary data stored in Saves/.Temp
    Save.save.delete('Saves/.Temp')

    # banner
    dashText = '-' * Functions.os.get_terminal_size().columns
    info = """\033[32m{}
Python Battleships

Creator: dragmine149
Github: https://www.github.com/dragmine149/Python_Battleships
{}
\033[0m""".format(dashText, dashText)

    while True:
        print("\x1b[2J\x1b[H", end='')
        
        if result == -0.5:
            dis = Display.Display(info)
            dis.Header()
            result = dis.Options(["Load Games", "Make New Game", "Settings"], ["Quit"]) + 1
            print("Returned Result: {}".format(result))
        
        Choices().generate()[result]()
        # print({'main temp result': result})
        # result = Game.Game(result).Main()
        # print({'Game result': result})
        result = -0.5 # reset choice so we don't go to that menu on back.


if __name__ == "__main__":
    Main()
