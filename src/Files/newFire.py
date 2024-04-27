import colorama
import os

from PythonFunctions.Check import Check
from PythonFunctions.Convert import Location
from PythonFunctions.Save import save
from PythonFunctions import Message, Board, Colours
from Files import ShipInfo


class Fire:
    """
    gameInfo -> Contains data about the game
    userInfo -> Contains user data [fire, target]
    """

    def __init__(self, gameInfo, userInfo, localUser=None):
        self.sv = save()
        self.ck = Check()

        # Loads information
        self.gameInfo = gameInfo
        self.gameFolder = os.path.join(
            self.gameInfo.get("path"), self.gameInfo.get("name")
        )
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

        self.gameData = self.sv.Read(
            os.path.join(self.gameFolder, "GameData"), encoding=self.sv.encoding.BINARY
        )
        # Paths for each individual users.

        self.userBoards = [
            [
                self.sv.Read(
                    os.path.join(self.gameFolder, self.userInfo[0], "shots"),
                    encoding=self.sv.encoding.BINARY,
                ),
                self.sv.Read(
                    os.path.join(self.gameFolder, self.userInfo[0], "ships"),
                    encoding=self.sv.encoding.BINARY,
                ),
            ],
            [
                self.sv.Read(
                    os.path.join(self.gameFolder, self.userInfo[1], "shots"),
                    encoding=self.sv.encoding.BINARY,
                ),
                self.sv.Read(
                    os.path.join(self.gameFolder, self.userInfo[1], "ships"),
                    encoding=self.sv.encoding.BINARY,
                ),
            ],
        ]

    def __Display(self):
        # Prints out the display, contains the user and boards.
        Message.clear()
        print(f"{self.turn}'s turn to shoot!\n")

        # Cool feature so if you are playing on two different devices
        # you can see where your ships are as well.
        if self.multiplayer != "n":
            localIndex = self.userInfo.index(self.localUser)
            localOpponentIndex = 0 if localIndex == 1 else 1
            boards = [
                self.userBoards[localIndex][0],
                self.userBoards[localIndex][1],
                self.userBoards[localOpponentIndex][0],
            ]
            Text = ["Your shots", "Your ships"]
            Board.MultiBoardDisplay(boards, Text)
        else:
            boards = [
                self.userBoards[self.turnIndex][0],
                self.userBoards[self.opponentTurnIndex][0],
            ]
            Text = [
                self.userInfo[self.turnIndex] + "'s board",
                self.userInfo[self.opponentTurnIndex] + "'s board",
            ]
            Board.MultiBoardDisplay(boards, Text)

    def __Clear(self, msg):
        Message.clear(msg, timeS=1)
        self.__Display()

    def __Shot(self):
        takenShot = False
        while not takenShot:
            # get input from user
            x, y = self.ck.getInput(
                "Please enter position to shoot (0 = quit): ",
                self.ck.ModeEnum.location,
                x=self.game["size"][0],
                y=self.game["size"][1],
            )

            # Already shot check. (Can't fire twice in the same spot)
            if self.userBoards[self.turnIndex][0][y][x] != "-":
                self.__Clear("You have already shot there!")
                continue

            # Hit miss check
            if self.userBoards[self.opponentTurnIndex][1][y][x] != "-":
                self.userBoards[self.turnIndex][0][y][x] = "X"
                print(
                    Colours.Translate(
                        f"{colorama.Fore.GREEN}HIT!{colorama.Fore.RESET}",
                        Colours.Format.BOLD,
                    )
                )

            else:
                self.userBoards[self.turnIndex][0][y][x] = "+"
                print(
                    Colours.Translate(
                        f"{colorama.Fore.RED}Miss :({colorama.Fore.RESET}",
                        Colours.Format.BOLD,
                    )
                )

            # Saving data...
            takenShot = True
            self.sv.Write(
                self.userBoards[0][0],
                os.path.join(self.gameFolder, self.userInfo[0], "shots"),
                encoding=self.sv.encoding.BINARY,
            )
            self.sv.Write(
                self.userBoards[1][0],
                os.path.join(self.gameFolder, self.userInfo[1], "shots"),
                encoding=self.sv.encoding.BINARY,
            )

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
                    colour = ship.Colour + ship.Symbol + colorama.Style.RESET_ALL

                    if BIV[0][y][x] == "X" and OIV[1][y][x] == colour:
                        ship.Health -= 1

            # Check if destroyed (all shot out)
            if ship.Health == 0:
                destroyedText += "{}\n".format(ship.Name)
                destroyedAmount += 1

        # if more (how) or equal are destroyed, end
        if destroyedAmount >= len(ships):
            Message.clear()
            winner = self.userInfo[self.turnIndex]
            looser = self.userInfo[self.opponentTurnIndex]
            Message.clear(f"GG! {winner} has beaten {looser}", timeS=2)

            self.sv.Write(
                self.game,
                os.path.join(self.gameFolder, "GameData"),
                encoding=self.sv.encoding.BINARY,
            )
            self.sv.Write(
                {"win": self.userInfo[self.turnIndex]},
                os.path.join(self.gameFolder, "win"),
                encoding=self.sv.encoding.BINARY,
            )

            return True

        if not winCheck:
            Message.clear(destroyedText, timeS=2)

    def Fire(self):
        # Main game loop
        game = True
        while game:
            # This is something we want to avoid really,
            # clearing every loop and recalling data again.
            Message.clear()

            # Shows the display
            self.__Display()

            if self.multiplayer != "n":
                winner = self.gameData.CheckForFile("win")
                if winner:
                    winner = self.gameData.readFile("win")["win"]
                    winnerIndex = self.userInfo.index(winner)
                    looserIndex = 0 if winnerIndex == 1 else 1
                    Message.clear(
                        (
                            f"GG! {self.userInfo[winnerIndex]} has beaten"
                            f" {self.userInfo[looserIndex]}"
                        ),
                        timeS=2,
                    )
                    return "Game Over"
                # Multiplayer loop
                if self.turn == self.localUser:  # if current turn, shoot fine.
                    result = self.__Shot()
                    if result is False:
                        return
                # else:  # else wait for instructions
                # msg = f"Waiting for {self.userInfo[self.turnIndex]} to shoot"
                # returnValue = Functions.waiting(msg)
                # if returnValue == "Back":
                #     return "Stopped whilst shooting."

                # Checks if game has already been won (completed.) (TODO)
                # self.WinGame(True)
            else:
                result = self.__Shot()
                if result is False:
                    return

            # Load the data again
            self.__RetrieveBoards()
            self.__getGameInformation()
