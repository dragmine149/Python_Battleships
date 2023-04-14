import sys
import argparse
from PythonFunctions import Check
from PythonFunctions.IsDigit import IsDigit
from PythonFunctions.Save import save
from PythonFunctions.TerminalDisplay import Display
from PythonFunctions.Watermark import LINKCODE
from Files import Settings

sv = save()
# Pre load settings to make sure all the files are there etc...
settings = Settings.Settings()


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
        settings.updateSave('path', args['save'][0])

    if args['delete']:
        def yes():
            sv.RemoveFolder(['Saves', 'Data'])
            sys.exit('Deleted old data. Please rerun')

        def no():
            sys.exit('Aborted!')

        chk = Check.Check()
        chk.getInput("Are you sure you want to delete all data?: ",
                     chk.ModeEnum.yesno, y=yes, n=no)

    r = IsDigit(args['menu'])
    print(r, args['menu'])

    if not r:
        sys.exit("Comming soon (Probably in Update 3)")

    return int(args['menu'])


class Choices:
    """Stores information about what each option does
    """
    def activate(self, pos):
        pos = pos[1]
        options = {
            1: self.selectGame,
            2: self.makeGame,
            3: self.settings,
        }

        method = options.get(pos)
        if method:
            return method()
        raise ValueError("Unimplemented option!")

    def quit(self):
        sys.exit("Thank you for playing")

    def selectGame(self):
        from Files.GameMenu import Menu
        return Menu().main()

    def makeGame(self):
        from Files import CreateInfo
        path = sv.Read('Data/Settings',
                       encoding=[sv.encoding.JSON,
                                 sv.encoding.BINARY]).get('path')
        return CreateInfo.CreateData(path).main()

    def settings(self):
        result = settings.showDisplay()
        return result


def Main():
    # goes into menu
    result = command_options() or -0.5
    choice = Choices()

    # Delete temparary data stored in Saves/.Temp
    sv.RemoveFolder('Saves/.Temp')

    # Make setup files
    sv.MakeFolders('Saves')
    sv.MakeFolders('Data')

    # banner
    url = LINKCODE(
        'https://www.github.com/dragmine149/Python_Battleships', 'Github')
    info = f"""Python Battleships ({url})

Creator: dragmine149"""

    while True:
        print("\x1b[2J\x1b[H", end='')

        if result == -0.5:
            dis = Display()
            quitMsg = "Thank you for playing!"
            dis.SetQuitMessage(quitMsg)
            dis.ShowHeader(text=info)
            dis.SetOptions(
                {
                    0: (choice.activate, "Load Games", 1),
                    1: (choice.activate, "Make New Game", 2),
                    2: (choice.activate, "Settings", 3),
                }
            )
            result = dis.ShowOptions()
            print(result)
            if result == quitMsg:
                return

        result = -0.5  # reset choice so we don't go to that menu on back.


if __name__ == "__main__":
    Main()
