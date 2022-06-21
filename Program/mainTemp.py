import importlib
import sys
import argparse
Functions = importlib.import_module('Functions')


def praser():
    parser = argparse.ArgumentParser(description="Battleships, in python in a python terminal.")  # noqa E501
    parser.add_argument('menu', default=-.5, type=int,
                        help="The menu to load into.", choices=[-.5, 1, 2, 3],
                        metavar="MENU", nargs='?')
    parser.add_argument('--delete',
                        help="Delete old game data.",
                        action='store_true')
    parser.add_argument("game name", default="", type=str,
                        help="Load into that game, comming in U3",
                        metavar="GAME_NAME", nargs='?')
    args = vars(parser.parse_args())
    return args


def command_options():
    args = praser()
    if args['delete']:
        def yes():
            import newSave
            newSave.save.Delete('Saves')
            newSave.save.Delete('Data')
            sys.exit('Deleted old data. Please rerun')

        def no():
            sys.exit('Aborted!')

        Functions.check('Are you sure you want to delete all data?: ',
                        returnFunc=(yes, no)).getInput('ynCheck')

    if args['game name'] != '':
        sys.exit("Comming soon (Probably in Update 3)")

    return args['menu']


def Main():
    # goes into menu
    choice = command_options() or -0.5

    GameMenu = importlib.import_module('GameMenu')
    Choices = importlib.import_module('Choices')
    Game = importlib.import_module('Game')

    # loads info
    c = Choices.Choices()
    menu = GameMenu.menu

    # banner
    info = """\033[32m--------------------------------------------------------------------
Python Battleships by drag

Github: https://www.github.com/dragmine149/Python_Battleships
--------------------------------------------------------------------
\033[0m"""

    options = """01: Load Games
02: Make New Game
03: Settings"""
    main = menu(info, options, c.generate("main"))

    result = main.getInput(choice, values=(0, 3))
    print({'main temp result': result})
    result = Game.Game(result).Main()
    print({'Game result': result})


if __name__ == "__main__":
    Main()
