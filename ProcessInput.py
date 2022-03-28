import Create as Create
import SaveSystem as save
import Functions
import os
import DriveApi as Drive


class Process:
    def __init__(self):
        print("Loading")

    def winView(self, path, name=None, external=False):
        if not external:
            users = Functions.RemoveNonGames(os.path.join(path, name))
            for user in users:
                sS = save.save(path)
                sSpath = os.path.join(name, user)

                print("{}'s' grid\n(where they shot)".format(user))
                save.board.DisplayBoard(sS.readFile(sSpath, "grid"))
                print("{}'s' ships\n(The ship layout they had)".format(user))
                save.board.DisplayBoard(sS.readFile(sSpath, "ships"))
            print("{} won this game.".format(sS.readFile(name, "win")))
            input("Press enter when you are ready to continue.")
            return None

    def Inputs(self, path, name=None, external=False, create=False):
        if create:
            [name, users, Location, online] = Create.create().inputs()
            return name, users, False, Location, online
        if not external:
            # Path Name
            err_Msg = "Failed -> Folder not found"
            win = save.save(path, False).readFile(name, "win")
            if win != err_Msg:  # change msg
                return self.winView(path, name)
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
            for item in path:
                if item['name'] == name:
                    name = item
                    break
            print(name['id'])
            usersInfo = Drive.Api(name['id']).ListFolder()
            multiPlayerId = None
            for user in usersInfo:
                if user['name'] == "multi":
                    multiPlayerId = user['id']
            users = Functions.RemoveNonGames(usersInfo)
            print(users)
            print(multiPlayerId)
            placed = [False, False]
            for user in range(len(usersInfo)):
                if usersInfo[user] in users:
                    print(usersInfo[user])
                    Files = Drive.Api(usersInfo[user]['id']).ListFolder()
                    for file in Files:
                        if file['name'] == "ships":
                            placed[user] = True
                            break
            multi = False
            if multiPlayerId is not None:
                multi = Drive.Api(name['id']).DownloadData({
                    'name': multiPlayerId,
                    'path': 'multiPlayer.temo'
                })
                if multi:
                    with open('multiPlayer.temo.txt', 'r') as mp:
                        multi = mp.read()
                    os.system('rm multiPlayer.temo.txt')

            return name['name'], users, placed[0] and placed[1], name['id'], multi  # noqa
