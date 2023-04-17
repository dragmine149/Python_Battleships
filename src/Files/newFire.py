import os

from PythonFunctions.Save import save
from PythonFunctions import Message
from Files import ShipInfo


class Fire:
    """
    gameInfo -> Contains data about the game
    userInfo -> Contains user data [fire, target]
    """
    def __init__(self, gameInfo, userInfo, localUser=None):
        self.save = save()
        
        # Loads information
        self.gameInfo = gameInfo
        self.userInfo = userInfo
        self.localUser = localUser
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
        # self.userColours = Settings.request(['colour', 'colour'])

    def __RetrieveBoards(self):
        # Even more information
        print({"Path": self.gameInfo[1]})
        self.gameData = Save.save({
            'path': self.gameInfo[1]
        })
        # Paths for each individual users.
    
        user1 = Save.save({
            'path': os.path.join(self.gameInfo[1], self.userInfo[0])
        })
        user2 = Save.save({
            'path': os.path.join(self.gameInfo[1], self.userInfo[1])
        })
    
        self.userData = [user1, user2]

        self.userBoards = [
            [
                user1.readFile("shots"),
                user1.readFile("ships"),
            ],
            [
                user2.readFile("shots"),
                user2.readFile("ships"),
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
            localIndex = self.userInfo.index(self.localUser)
            localOpponentIndex = 0 if localIndex == 1 else 1
            boards = [self.userBoards[localIndex][0],
                      self.userBoards[localIndex][1],
                      self.userBoards[localOpponentIndex][0]]
            Text = [
                'Your shots',
                'Your ships'
            ]
            Functions.board.MultiDisplay(boards, Text)  # noqa E501
        else:
            boards = [self.userBoards[self.turnIndex][0],
                      self.userBoards[self.opponentTurnIndex][0]]
            Text = [self.userInfo[self.turnIndex] + "'s board",
                    self.userInfo[self.opponentTurnIndex] + "'s board"]
            Functions.board.MultiDisplay(boards, Text)

    def __Clear(self, msg):
        Functions.clear(1, msg)
        self.__Display()

    def __Shot(self):
        takenShot = False
        while not takenShot:
            # get input from user
            shotPosition = input("Please enter position to shoot (0 = quit): ")
            if shotPosition == '' or shotPosition is None:
                # No input test
                continue

            if shotPosition[0].lower() == "0":
                # Quit test
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
            self.userData[0].writeFile(
                self.userBoards[0][0], "shots")
            self.userData[1].writeFile(
                self.userBoards[1][0], "shots")

            self.game["turn"] = self.userInfo[self.opponentTurnIndex]

            self.gameData.writeFile(self.game, "GameData")

            # win check
            if self.WinGame() is True:
                return False

        # readchar?
        # optional?
        # bold highlighted
        # confirmation
        # x, +, -
        return

    def WinGame(self, winCheck=False):
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
            winner = self.userInfo[self.turnIndex]
            looser = self.userInfo[self.opponentTurnIndex]
            Functions.clear(2, "GG! {} has beaten {}".format(winner, looser))
            self.gameData.writeFile(self.game, "GameData")
            self.gameData.writeFile({
                'win': self.userInfo[self.turnIndex]
                }, 'win')
            return True

        if not winCheck:
            Functions.clear(2, destroyedText)

    def Fire(self):
        # Main game loop
        game = True
        while game:
            # This is something we want to avoid really,
            # clearing every loop and recalling data again.
            Functions.clear()

            # Shows the display
            self.__Display()

            if self.multiplayer != 'n':
                
                winner = self.gameData.CheckForFile('win')
                if winner:
                    winner = self.gameData.readFile('win')['win']
                    winnerIndex = self.userInfo.index(winner)
                    looserIndex = 0 if winnerIndex == 1 else 1
                    Functions.clear(2, "GG! {} has beaten {}".format(self.userInfo[winnerIndex], self.userInfo[looserIndex]))
                    return "Game Over"
                # Multiplayer loop
                if self.turn == self.localUser:  # if current turn, shoot fine.
                    result = self.__Shot()
                    if result is False:
                        return
                else:  # else wait for instructions
                    msg = "Waiting for {} to shoot".format(
                        self.userInfo[self.turnIndex])
                    returnValue = Functions.waiting(msg)
                    if returnValue == "Back":
                        return "Stopped whilst shooting."

                # Checks if game has already been won (completed.) (TODO)
                # self.WinGame(True)
            else:
                result = self.__Shot()
                if result is False:
                    return

            # Load the data again
            self.__RetrieveBoards()
            self.__getGameInformation()
