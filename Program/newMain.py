# Might remove and just rewrite main instead

import os
import Functions

# setup program.
filePath = os.path.dirname(os.path.realpath(__file__))
print("Stored Path: {}".format(filePath))
os.chdir(filePath)
Functions.clear(.5)


class Main:
    def __init__(self):
        self.gameName = None
        self.users = None
        self.Placed = None
        self.Location = None
        self.multi = None
        self.cont = 0
        self.opponent = None

    def Loop(self, argv):
        if len(argv) == 2:
            digit = Functions.NumberRangeCheck(argv[1], 3)
            if digit:
                # call function
                return
