import importlib
import sys
Functions = importlib.import_module('Functions')


def help():
    print("""USAGE:
--------------------------------------------------------------------------------------
\033[90mpython \033[32mMain.py \033[33m[Option]\033[0m

Option can be one of the following:
- String
  - Attempts to load game name of string, If not found will make game name of string
- Number
  - Does that action (1 = load, 2 = make, 3 = settings). Quick form

Other possible options:
- help
  - Shows this menu
---------------------------------------------------------------------------------------
""")  # noqa E501

    return 1


def options():
    if len(sys.argv) > 1:
        if Functions.IsDigit(sys.argv[1]):
            return int(sys.argv[1])  # fix?

        if sys.argv[1].lower()[0] == "h":
            sys.exit(help())

        if sys.argv[1] == '+-delete':
            def yes():
                import newSave
                newSave.save.Delete('Saves')
                newSave.save.Delete('Data')
                sys.exit('Deleted old data. Please rerun')

            def no():
                sys.exit('Aborted!')

            Functions.check('Are you sure you want to delete all data?: ',
                            returnFunc=(yes, no)).getInput('ynCheck')

        if isinstance(sys.argv[1], str):
            sys.exit("Comming soon (Probably in Update 3)")


if __name__ == "__main__":
    # goes into menu
    choice = options() or -0.5

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
