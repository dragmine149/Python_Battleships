import importlib
import os
ShipInfo = importlib.import_module('Files.ShipInfo')
newSave = importlib.import_module('Files.newSave')
Functions = importlib.import_module('Files.Functions')
colours = importlib.import_module('Files.colours')
Settings = importlib.import_module('Files.Settings')


class Fire:
    """
    gameInfo -> Contains data about the game
    userInfo -> Contains user data [fire, target]
    """
    def __init__(self, gameInfo, userInfo):
        # Loads information
        self.gameInfo = gameInfo
        self.userInfo = userInfo
        self.ships = ShipInfo.shipInfo(ShipInfo.getShips()).Main()
        self.__RetrieveBoards()
        self.__getGameInformation()

    def __getGameInformation(self):
        # More information
        self.game = self.gameData.readFile("GameData")
        self.turn = self.game["turn"]
        self.turnIndex = self.userInfo.index(self.turn)
        self.opponentTurnIndex = 0 if self.turnIndex == 1 else 1
        self.multiplayer = self.game["multi"]
        self.userColours = [
            Settings.request('colour'),
            Settings.request('colour')
        ]

    def __RetrieveBoards(self):
        # Even more information
        self.gameData = newSave.save({
            'name': '',
            'path': os.path.join(self.gameInfo[1], self.gameInfo[0])
        })
        self.userData = [
            newSave.save({
                'name': '',
                'path': os.path.join(self.gameInfo[1],
                                     self.gameInfo[0],
                                     self.userInfo[0])
            }),
            newSave.save({
                'name': '',
                'path': os.path.join(self.gameInfo[1],
                                     self.gameInfo[0],
                                     self.userInfo[1])
            })
        ]
        self.userBoards = [
            [
                self.userData[0].readFile("shots"),
                self.userData[0].readFile("ships"),
            ],
            [
                self.userData[1].readFile("shots"),
                self.userData[1].readFile("ships"),
            ]
        ]

    def __Display(self):
        # Prints out the display, contains the user and boards.
        Functions.clear()
        print("{}{}{}'s turn to shoot\n".format(
            colours.c(self.userColours[self.turnIndex]),
            self.turn,
            colours.c()))

        # Cool feature so if you are playing on two different devices
        # you can see where your ships are as well.
        if self.multiplayer != "n":
            Functions.board.MultiDisplay([self.userBoards[self.turnIndex][0],
                                          self.userBoards[self.turnIndex][1]])
        else:
            Functions.board.DisplayBoard(self.userBoards[self.turnIndex][0])

    def __Clear(self, msg):
        Functions.clear(1, msg)
        self.__Display()

    def __Shot(self):
        takenShot = False
        while not takenShot:
            # get input from user
            shotPosition = input("Please enter position to shoot (q = quit): ")
            if shotPosition[0].lower() == "q":
                return False

            # converts to []
            x, y = Functions.LocationConvert(shotPosition).Convert()
            if x is None or y is None:  # checks if invalid
                self.__Clear("Please enter a valid input!")
                continue

            # off board checks (too big to be on board)
            if x >= self.game["size"][0]:
                self.__Clear("X coordinate is not on the board!")
                continue

            if y >= self.game["size"][1]:
                self.__Clear("Y coordinate is not on the board!")
                continue

            # Already shot check. (Can't fire twice in the same spot)
            if self.userBoards[self.turnIndex][0][y][x] != "-":
                self.__Clear("You have already shot there!")
                continue

            # Hit miss check
            if self.userBoards[self.opponentTurnIndex][1][y][x] != "-":
                self.userBoards[self.turnIndex][0][y][x] = "X"
                Functions.Print("HIT!", "green", "bold")
            else:
                self.userBoards[self.turnIndex][0][y][x] = "+"
                Functions.Print("Miss :(", "red", "bold")

            # Saving data...
            takenShot = True
            self.userData[0].writeFile(self.userBoards[0][0], True, "shots")
            self.userData[0].writeFile(self.userBoards[0][1], True, "ships")
            self.userData[1].writeFile(self.userBoards[1][0], True, "shots")
            self.userData[1].writeFile(self.userBoards[1][1], True, "ships")

            self.game["turn"] = self.userInfo[self.opponentTurnIndex]

            self.gameData.writeFile(self.game, True, "GameData")

            # win check
            if self.WinGame() is True:
                return False

        # readchar?
        # optional?
        # bold highlighted
        # confirmation
        # x, +, -
        return

    def WinGame(self):
        # setup (gets ships and text)
        ships = ShipInfo.shipInfo(ShipInfo.getShips()).Main()
        destroyedText = "Destroyed Ships:\n"
        destroyedAmount = 0

        # Make into a better loop?
        # BIV -> Board Index Value
        # OIV -> Opponent Index Value
        BIV = self.userBoards[self.turnIndex]
        OIV = self.userBoards[self.opponentTurnIndex]

        for ship in ships:
            for y in range(len(self.userBoards[self.turnIndex][0])):
                for x in range(len(self.userBoards[self.turnIndex][0][y])):
                    colour = ship.Colour + ship.Symbol + colours.c()

                    if BIV[0][y][x] == "X" and OIV[1][y][x] == colour:
                        ship.Health -= 1

            # Check if destroyed (all shot out)
            if ship.Health == 0:
                destroyedText += "{}\n".format(ship.Name)
                destroyedAmount += 1

        # if more (how) or equal are destroyed, end
        if destroyedAmount >= len(ships):
            Functions.clear()
            print("GG! {} has beaten {}".format(BIV,
                                                OIV))
            self.game["win"] = self.userInfo[self.turnIndex]
            self.gameData.writeFile(self.game, True, "GameData")
            return True

        Functions.clear(2, destroyedText)

    def Fire(self):
        # Main game loop
        game = True
        while game:
            Functions.clear()
            self.__Display()
            result = self.__Shot()
            if result is False:
                return
            self.__RetrieveBoards()
            self.__getGameInformation()
