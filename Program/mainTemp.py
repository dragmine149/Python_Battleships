import Functions
import sys
import GameMenu
import Choices

# loads info
c = Choices.Choices()
menu = GameMenu.menu

if __name__ == "__main__":
    # banner
    info = """--------------------------------------------------------------------
Python Battleships by drag

Github: https://www.github.com/dragmine149/Python_Battleships
--------------------------------------------------------------------
"""

    options = """01: Load Games
02: Make New Game
03: Settings"""

    main = menu(info, options, c.generate("main"))

    # goes into menu
    choice = -.5
    if len(sys.argv) > 1:
        if Functions.IsDigit(sys.argv[1]):
            choice = int(sys.argv[1])  # fix

    result = main.getInput(choice, values=(0, 3))
    print({'main temp result': result})
