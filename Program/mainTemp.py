import Functions
import sys
import GameMenu
import Choices

# loads info
c = Choices.Choices()
menu = GameMenu.menu


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


if __name__ == "__main__":
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

    # goes into menu
    choice = -.5
    if len(sys.argv) > 1:
        if Functions.IsDigit(sys.argv[1]):
            choice = int(sys.argv[1])  # fix
        if sys.argv[1].lower()[0] == "h":
            sys.exit(help())

    result = main.getInput(choice, values=(0, 3))
    print({'main temp result': result})
