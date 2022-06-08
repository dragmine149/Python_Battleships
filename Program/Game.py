import newSave
import Functions
import placeSystem

class Game:
    def __init__(self, name, users, placed, location, multiplayer):
        self.name = name
        users.sort()
        self.users = users
        self.placed = placed
        self.location = location
        self.multiplayer = multiplayer
    
    def Place(self):
        for user in users:
            userPlace = placeSystem.Place()