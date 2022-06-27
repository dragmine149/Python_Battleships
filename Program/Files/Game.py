import importlib
import getpass
import os
newSave = importlib.import_module('Files.newSave')
Functions = importlib.import_module('Files.Functions')
newPlace = importlib.import_module('Files.newPlace')
newFire = importlib.import_module('Files.newFire')


class Game:
    def __init__(self, data):
        self.name = data[0]
        self.users = data[1]
        self.placed = data[2]
        self.location = data[3]
        self.gamePath = os.path.join(self.location, self.name)
        self.multiplayer = data[4]
        self.gameData = newSave.save({
            'name': self.name,
            'path': self.location,
        })

    def Place(self):
        for user in range(len(self.users)):
            if not self.placed[user]:
                userPlace = newPlace.Place(self.name,
                                           os.path.join(self.gamePath, self.users[user]),  # noqa E501
                                           self.users[user])
                self.placed[user] = userPlace.Main()
            
        return self.placed[0] and self.placed[1]

    def Fire(self):
        newFire.Fire([self.name, self.location, self.multiplayer], self.users).Fire()

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
            result = self.Place()
            
            if result:
                return self.Fire()
            return "Ended during placement."
        return "Incorrect password entered!"
