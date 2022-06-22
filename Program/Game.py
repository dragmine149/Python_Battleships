import importlib
import getpass
newSave = importlib.import_module('newSave')
Functions = importlib.import_module('Functions')
newPlace = importlib.import_module('newPlace')


class Game:
    def __init__(self, data):
        self.name = data[0]
        data[1].sort()
        self.users = data[1]
        self.placed = data[2]
        self.location = data[3]
        self.multiplayer = data[4]
        self.gameData = newSave.save({
            'name': self.name,
            'path': self.location,
        })

    def Place(self):
        for user in range(len(self.users)):
            if not self.placed[user]:
                userPlace = newPlace.Place(self.name,
                                           self.location,
                                           self.users[user])
                self.placed[user] = userPlace.Main()
        # self.gameData.writeFile()
        return "Completed place"

    def Password(self):
        gameData = self.gameData.readFile('{}/GameData'.format(self.name))
        if gameData['password'] is not None:
            word = getpass.getpass("Please enter game password: ")
            if word == gameData['password']:
                return True
            return False
        return True

    def Main(self):
        if self.Password():
            return self.Place()
        return "Incorrect password entered!"
