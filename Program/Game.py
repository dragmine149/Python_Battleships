import newSave
import Functions
import placeSystem

class Game:
    def __init__(self, data):
        self.name = data[0]
        data[1].sort()
        self.users = data[1]
        self.placed = data[2]
        self.location = data[3]
        self.multiplayer = data[4]
    
    def Place(self):
        for user in range(len(self.users)):
            if not self.placed[user]:
                userPlace = placeSystem.Place()
    
    def Main(self):
        return self.Place()