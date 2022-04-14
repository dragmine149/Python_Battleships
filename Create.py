import Save as save
import Functions


class create:
    def __init__(self):
        self.info = []
        self.save = None

    def strCheck(self, msg, info, check=None):
        name = None
        while not name:
            name = input(msg)
            if name == '':
                name = None
                Functions.clear(1, "Please enter a {}!".format(info))
            elif name == check:
                name = None
                Functions.clear(1, "Player 2's name cannot be the same as player 1!")  # noqa
            elif name.startswith('.'):
                name = None
                Functions.clear(1, "{} cannot start with '.'!".format(info))
            elif name.find(' ') > -1:
                print("Detected spaces in {}".format(info))
                reset = None
                while not reset:
                    reset = input("New {}: {} (y = yes, n = no): ".format(info, name.replace(' ', '')))  # noqa
                    if reset.lower()[0] == "n":
                        name = None
                        Functions.clear(1, "Please enter a new {}".format(info))  # noqa
                    elif reset.lower()[0] == "y":
                        return name.replace(' ', '')
                    else:
                        reset = None
                        Functions.clear(1, "Please enter 'y' or 'n'")
            else:
                return name

    def _SizeRangeCheck(self, size):
        # replace with amount of ships in game.
        if size >= 5:  # got to be big enough to hold all ships
            return True
        return False

    def intCheck(self, msg):
        iNT = None
        while not iNT:
            iNT = Functions.check(msg, None, None, self._SizeRangeCheck).InputDigitCheck()  # noqa
        return iNT

    def inputs(self):
        name = self.strCheck("Please enter a name for this game: ", "Game Name")  # noqa
        u1 = self.strCheck("Please enter player 1's name: ", "Player 1 Name")  # noqa
        u2 = self.strCheck("Please enter player 2's name: ", "Player 2 Name", u1)  # noqa
        users = [u1, u2]
        size = [
            self.intCheck("Please enter X size (length): "),
            self.intCheck("Please enter Y size (height): ")
        ]
        Location = None
        while not Location:
            Location = input("Custom save location (blank = default, Supports google drive files): ")  # noqa
            if Location == "":
                Location = "Saves"
            # Check for HttpError without putting google files into this file..
            self.userSave = []
            self.userFolder = []
            self.parent = save.save(Location, data={
                'name': name,
                'file': ''
            }).makeFolder()
            if isinstance(self.parent, dict):
                self.parent = self.parent['id']

            for user in users:
                saveItem = False
                while not saveItem:
                    saveItem = save.save(Location, data={
                        'name': name,
                        'file': user
                    })
                    if isinstance(saveItem, str):
                        if saveItem.startswith('GD'):
                            Functions.clear(2, "Google Drive not installed. Please rerun this program with it installed or user a different directory.")  # noqa
                            Location = None
                            saveItem = True
                            break

                        if saveItem.startswith('No'):
                            Location = None
                            saveItem = True
                            Functions.clear(2, "Client doesn't have access to that folder id. Please make sure you have internet connect and can read and write into the folder specified!")  # noqa
                            break
                    self.userFolder.append(saveItem.makeFolder(user))

                self.userSave.append(saveItem)

        online = None
        if Location != "Saves":
            while online is None:
                online = input("Are you playing online? (y = yes, n = no): ")
                if online.lower()[0] == "y":
                    online = True
                elif online.lower()[0] != "n":
                    online = None
                    Functions.clear(1, "Please enter 'y' or 'n'")
                else:
                    online = False

        gameBoard = Functions.board.CreateBoard(size)
        print("---------------INFO---------------")
        print(self.userSave)
        print(self.userFolder)
        print("-------------END INFO-------------")
        for user in range(len(self.userSave)):
            self.userSave[user].writeFile({
                'data': gameBoard,
                'folder': self.userFolder[user]
            }, 'grid')
        if online:
            result = save.save(Location, data={
                'name': 'multi',
                'file': 'multi'
            }).writeFile({
                'data': online,
                'folder': self.parent
            })
            print({'result': result})
            Functions.clear(20)
        return [name, users, self.parent, online]
