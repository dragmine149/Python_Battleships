import sys
import argparse
import getpass
from PythonFunctions import Check
from PythonFunctions.IsDigit import IsDigit
from PythonFunctions.Save import save
from PythonFunctions.TerminalDisplay import Display
from PythonFunctions.Watermark import LINKCODE
from Files import Settings, CreateInfo
from Files.GameMenu import Menu

sv = save()
# Pre load settings to make sure all the files are there etc...
settings = Settings.Settings()


def praser():
    """Setsup the command line arguments.

    Returns:
        args (list): the arguments inputted via command line
    """
    parser = argparse.ArgumentParser(
        description="Battleships, in python in a python terminal.")
    parser.add_argument('menu', default=-.5,
                        help="The menu or game to load",
                        metavar="Menu / Game Name", nargs='?')
    createGroup = parser.add_argument_group(
        'Create', 'Arguments for creating a game')
    createGroup.add_argument('-c', '--create',
                             help='Create a game.',
                             action='store_true')
    createGroup.add_argument('-cn',
                             help='Name of the game',
                             nargs=1,
                             default=['None'],
                             metavar='Name')
    createGroup.add_argument('-cu1',
                             help='Name of user 1',
                             nargs=1,
                             default=[getpass.getuser()],
                             metavar='User')
    createGroup.add_argument('-cu2',
                             help='Name of user 2',
                             nargs=1,
                             default=['None'],
                             metavar='User')
    createGroup.add_argument('-cX',
                             help='X size of the board',
                             nargs=1,
                             default=[10],
                             metavar='Size')
    createGroup.add_argument('-cY',
                             help='Y size of the board',
                             nargs=1,
                             default=[10],
                             metavar='Size')
    createGroup.add_argument('-cM',
                             help='If multiplayer is enabled',
                             nargs=1,
                             default=['no'],
                             metavar='Multiplayer')
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
    print(args)
    if args.get('create'):
        path = sv.Read('Data/Settings',
                       encoding=[sv.encoding.JSON,
                                 sv.encoding.BINARY]).get('path')
        c = CreateInfo.CreateData(path)
        c.SetDefaults(args.get('cn')[0], args.get('cu1')[0], args.get(
            'cu2')[0], args.get('cX')[0], args.get('cY')[0], args.get('cM')[0])
        c.main()

    if args.get('save'):
        # Force updates the save location.
        settings.saveSettings('path', args.get('save')[0])

    if args.get('delete'):
        def yes():
            sv.RemoveFolder(['Saves', 'Data'])
            sys.exit('Deleted old data. Please rerun')

        chk = Check.Check()
        chk.getInput("Are you sure you want to delete all data?: ",
                     chk.ModeEnum.yesno, y=yes, n=sys.exit, nA='Aborted!')

    if args.get('menu') != -0.5:
        if IsDigit(args.get('menu')):
            Menu().main(args.get('menu'))
            return

        sys.exit('Invalid game argument')


# pylint: disable=C0415
class Choices:
    """Stores information about what each option does
    """

    def activate(self, pos):
        pos = pos[1]
        options = {
            1: self.selectGame,
            2: self.makeGame,
            3: settings.showDisplay,
        }

        method = options.get(pos)
        if method:
            return method()
        raise ValueError("Unimplemented option!")

    def quit(self):
        sys.exit("Thank you for playing")

    def selectGame(self):
        return Menu().main()

    def makeGame(self):
        path = sv.Read('Data/Settings',
                       encoding=[sv.encoding.JSON,
                                 sv.encoding.BINARY]).get('path')
        return CreateInfo.CreateData(path).main()

# pylint: enable=C0415


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
