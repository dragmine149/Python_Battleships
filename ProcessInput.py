import Create as Create
import SaveSystem as save
import Functions
import os
import DriveApi as Drive


class Process:
    def __init__(self):
        print("Loading")

    # def winView(self, Path, external=False):
    #     Functions.clear()
    #     # change to a different layout
    #     aPath = Path
    #     name = Path
    #     if external:
    #         aPath = Path['id']
    #         name = Path['name']
    #     for i in range(len(users)):
    #         if users[i] != "win":
    #             print("{} data\ngrid (where they shot)".format(users[i]))  # noqa
    #             save.board.DisplayBoard(save.save(aPath, external).readFile(name, "grid"))  # noqa
    #             print("{} data\nships (The ship layout they had)".format(users[i]))  # noqa
    #             save.board.DisplayBoard(save.save(aPath, external).readFile(name, "ships"))  # noqa
    #     input("Press enter when you are ready to continue.")

    def Inputs(self, path, name=None, external=False, create=False):
        if create:
            [name, users, Location, online] = Create.create().inputs()
            return name, users, False, Location, online
        if not external:
            # Path Name
            err_Msg = "Failed -> Folder not found"
            win = save.save(path, False).readFile(name, "win")
            if win != err_Msg:  # change msg
                self.winView()
            else:
                users = save.save(path, False).ListDirectory(os.path.join(path, name))  # noqa
                placed = False
                if save.save(path, False).readFile(os.path.join(name, users[0]), "ships") != err_Msg:  # noqa
                    if save.save(path, False).readFile(os.path.join(name, users[1]), "ships") != err_Msg:  # noqa
                        placed = True

                multi = False
                if save.save(path, False).readFile(name, "multi") != err_Msg:
                    multi = True

                return name, users, placed, path, multi
        else:
            # Path, name (id, name)
            # Path usless
            users = Drive.Api(name['id']).ListFolder()
            print(users)
