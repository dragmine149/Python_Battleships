import importlib
import sys
import argparse
Functions = importlib.import_module('Files.Functions')
Save = importlib.import_module('Files.Save')
Settings = importlib.import_module('Files.Settings')


def praser():
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


def Main():
    # goes into menu
    choice = command_options() or -0.5

    GameMenu = importlib.import_module('Files.GameMenu')
    Choices = importlib.import_module('Files.Choices')
    Game = importlib.import_module('Files.Game')

    # loads info
    c = Choices.Choices()
    menu = GameMenu.menu

    # Delete temparary data stored in Saves/.Temp
    Save.save.delete('Saves/.Temp')

    # banner
    dashText = '-' * Functions.os.get_terminal_size().columns
    info = """\033[32m{}
Python Battleships by drag

Github: https://www.github.com/dragmine149/Python_Battleships
{}
\033[0m""".format(dashText, dashText)

    options = """01: Load Games
02: Make New Game
03: Settings"""

    while True:
        main = menu(info, options, c.generate("main"))

        result = main.getInput(choice, values=(0, 3))
        if result is True:
            continue

        # print({'main temp result': result})
        result = Game.Game(result).Main()
        print({'Game result': result})


if __name__ == "__main__":
    Main()
