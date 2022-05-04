import Save as save
import Functions


class create:
    def __init__(self):
        self.info = []
        self.save = None

    @staticmethod
    def yesFunc():
        name = self.strCheck("Please enter a name for this game: ", "Game Name")  # noqa
        return name

    def gameCheck(self, name, Location):
        gameInfo = save.save(Location)
        if gameInfo.CheckForFile(name):
            overwrite = None
            while overwrite is None:
                overwrite = Functions.ynCheck(input("Are you sure you want to overwrite this game? (y = yes, n = no): "),  # noqa E501
                                              True)
                if overwrite:
                    # If they don't want to overwrite, Makes the same game but with a random string attacked on to the end  # noqa
                    # This is so they can use the same name yet not interfer with the old game # noqa
                    newName = None
                    while newName is None:
                        newName = Functions.ynCheck(input("Do you want to choose a new name?: "),  # noqa E501
                                                    self.yesFunc, "n")
                    if newName == "n":
                        newName = path + '-' + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))  # noqa E501
                    return newName

    # Checks if the inputted string is valid
    # TODO: better check
    def strCheck(self, msg, info, check=None):
        name = None
        while not name:
            name = input(msg)
            if name == '':
                Functions.clear(1, "Please enter a {}!".format(info))
            elif name == check:
                Functions.clear(1, "Player 2's name cannot be the same as player 1!")  # noqa
            elif name.startswith('.') or name.startswith('_'):
                Functions.clear(1, "{} cannot start with '.' or '_'!".format(info))  # noqa E501
            elif name.find(' ') > -1:
                print("Detected spaces in {}".format(info))
                reset = None
                while not reset:
                    def resetNo():
                        Functions.clear(1, "Please enter a new {}".format(info))  # noqa
                        return "Skip"


                    reset = Functions.ynCheck(input("New {}: {} (y = yes, n = no): ".format(info, name.replace(' ', '_'))),  # noqa E501
                                              name.replace(' ', '_'),
                                              resetNo)
                    if reset is not None and reset != "Skip":
                        return reset
            else:
                return name
            name = None  # this would only run if it hasn't been returned yet

    def _SizeRangeCheck(self, size):
        # replace with amount of ships in game.
        if size >= 5:  # got to be big enough to hold all ships
            return True
        return False

    # Checks if int
    def intCheck(self, msg):
        iNT = None
        while not iNT:
            iNT = Functions.check(msg, None, None, self._SizeRangeCheck).InputDigitCheck()  # noqa
        return iNT

    # Gets inputs for the game
    def inputs(self):
        # get information about the game
        name = self.strCheck("Please enter a name for this game: ", "Game Name")  # noqa
        u1 = self.strCheck("Please enter player 1's name: ", "Player 1's Name")  # noqa
        u2 = self.strCheck("Please enter player 2's name: ", "Player 2's Name", u1)  # noqa
        users = [u1, u2]
        size = [
            self.intCheck("Please enter X size (length): "),
            self.intCheck("Please enter Y size (height): ")
        ]

        Location = None
        while Location is None:
            Location = input("Custom save location (blank = default, supports google drive folder id): ")  # noqa
            if Location == "":
                Location = "Saves"

            # If default, don't need to do much
            # If drive, run test
            # If external, run test

            # skip doing stuff to saves
            if Location != "Saves":
                # attmepts to write file and read file from dir specified
                # creates save obj
                saveInfo = save.save(Location, False, {
                    'name': 'Test',
                    'file': 'test'
                })

                # creates file
                saveInfo.writeFile("This is a test file")

                # reads file from same place
                data = saveInfo.readFile({
                    'name': 'Test'
                })

                print(data)
                if data != "This is a test file":
                    # Oh oh, doesn't work... Return error
                    Functions.clear(3, "Please make sure that this program has read and write ability to {}".format(Location))  # noqa
                    Location = None

        print({"Loc": Location})
        # # Location get, i do not like it too much.
        # # TODO: rewrite... and shrink
        # Location = None
        # while not Location:
        #     Location = input("Custom save location (blank = default, Supports google drive files): ")  # noqa
        #     if Location == "":
        #         Location = "Saves"
        #     # Check for HttpError without putting google files into this file..
        #     self.userSave = []
        #     self.userFolder = []
        #     name = self.gameCheck(name, Location)
        #     self.parentSave = save.save(Location, data={
        #         'name': name,
        #         'file': ''
        #     })
        #     result = self.parentSave.makeFolder()
        #     if len(result) > 0:
        #         self.parent = result[0]
        #         if result[1] is not None:  # something got returned as well!
        #             # This gets the name from the folder created
        #             start = self.parent.find(Location)
        #             length = len(Location)
        #             end = start + length + 1
        #             name = self.parent[end:]
        #
        #     if isinstance(self.parent, dict):
        #         self.parent = self.parent['id']
        #     else:
        #         print(self.parent)  # curios of what it returns...
        #
        #     # Makes save file for every user
        #     for user in users:
        #         saveItem = False
        #         while not saveItem:
        #             # TODO: use new folder.
        #             saveItem = save.save(self.parent, data={
        #                 'name': '',
        #                 'file': user
        #             })
        #             if isinstance(saveItem, str):
        #                 if saveItem.startswith('GD'):
        #                     Functions.clear(2, "Google Drive not installed. Please rerun this program with it installed or user a different directory.")  # noqa
        #                     Location = None
        #                     saveItem = True
        #                     break
        #
        #                 if saveItem.startswith('No'):
        #                     Location = None
        #                     saveItem = True
        #                     Functions.clear(2, "Client doesn't have access to that folder id. Please make sure you have internet connect and can read and write into the folder specified!")  # noqa
        #                     break
        #             self.userFolder.append(saveItem.makeFolder(user))
        #
        #         self.userSave.append(saveItem)

        # Deals with online stuff
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
            Functions.clear(2)
        return [name, users, Location, online]
