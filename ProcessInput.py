import Create
import Save as save
import Functions
import os


class Process:
    def __init__(self):
        print("Loading")

    def winView(self, path, name=None, external=False):
        if not external:
            users = Functions.RemoveNonGames(os.path.join(path, name))
            for user in users:
                sS = save.save(path, True, {
                    'name': path,
                    'file': user
                })

                print("{}'s' grid\n(where they shot)".format(user))
                Functions.board.DisplayBoard(sS.readFile("grid"))
                print("{}'s' ships\n(The ship layout they had)".format(user))
                Functions.board.DisplayBoard(sS.readFile("ships"))
            print("{} won this game.".format(save.save(path, False, {
                'name': path,
                'file': 'win'
            }).readFile("")))
            input("Press enter when you are ready to continue.")
            return None

    def Inputs(self, path, name=None, external=False, create=False):
        if create:
            [name, users, Location, online] = Create.create().inputs()
            return name, users, False, Location, online
        print({'external': external})
        if not external:
            # Path Name
            # Saves GameName
            # Id Name
            winPath = os.path.join(path, name)
            win = save.save(winPath).CheckForFile(os.path.join(winPath, "win"))
            if win:
                return self.winView(path, name)
            else:
                users = save.save(os.path.join(path, name), False, {
                    'name': path,
                    'file': name
                }).ListDirectory(dir=True)

                placed = [False, False]
                if save.save(path).CheckForFile(os.path.join(name, users[0], "ships")):  # noqa
                    placed[0] = True
                if save.save(path).CheckForFile(os.path.join(name, users[1], "ships")):  # noqa
                    placed[1] = True

                multi = False
                if save.save(path).CheckForFile(os.path.join(name, "multi")):
                    multi = True

                return name, users, placed, path, multi
        else:
            # Path, name (id, name)
            # Path usless
            for item in path:
                # Errors... why?
                if item['name'] == name:
                    saveLoc = item['id']
                    name = item
                    break

            usersInfo = save.save(name['id']).ListDirectory()
            multiPlayerId = None
            newUsers = []
            for user in usersInfo:
                if user['name'] == "multi":
                    multiPlayerId = user['id']
                elif user['name'] != "turn":
                    newUsers.append(user)
            print({'1. usersInfo': newUsers})
            users = Functions.RemoveNonGames(usersInfo)

            print({'users': users})
            print({'usersInfo': usersInfo})
            print({'multiPlayerId': multiPlayerId})
            placed = [False, False]

            for user in range(len(newUsers)):
                Files = save.save(newUsers[user]['id']).ListDirectory()
                for file in Files:
                    if file['name'] == "ships":
                        placed[user] = True
                        break

            print({'placed': placed})

            multi = False
            if multiPlayerId is not None:
                if not os.path.exists("Saves/.Temp/{}".format(name['id'])):
                    os.mkdir("Saves/.Temp/{}".format(name['id']))

                multi = save.save(name['id'], data={
                    'name': 'Saves',
                    'file': 'multi'
                }).readFile({
                    'name': multiPlayerId
                })
                print({'multi': multi})
                if multi:
                    save.save("Saves").Delete("Saves/.Temp/{}".format(name['id']))  # noqa

            return name['name'], newUsers, placed, saveLoc, multi  # noqa
