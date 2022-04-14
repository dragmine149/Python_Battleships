while True:
        # Actual game
        if v == 0:
            # Waiting for other user to setup their ships
            userSetup = False
            pathLocation = Location.rstrip().replace('"', '')
            if platform.system() != "Windows":
                pathLocation = pathLocation.replace("\\", "")
            while not userSetup:
                if os.path.exists(os.path.join(pathLocation, gameName, other, "ships")):  # noqa
                    userSetup = True
                else:
                    v = waitSim(v, "Waiting for opponent to place their ships")
                    if v != 0:
                        userSetup = "Stop"

            if v == 0:
                # Actually playing the game
                game = False
                print("Current game: {}\nOpponent: {}".format(gameName, other))
                while not game:
                    try:
                        if save.save(Location).readFile(gameName, "turn") == name:  # noqa
                            game = fire.fire(gameName, name, other, Location).Fire(True)  # noqa
                            if not game:
                                print("Current game: {}\nOpponent: {}".format(gameName, other))  # noqa
                        else:
                            game = waitSim(game, "Waiting for opponent to take a shot")  # noqa
                    except KeyboardInterrupt:  # Probably shouldn't do this...
                        game = "Fake"
                        Functions.clear()
                        print("Current game: {}.\nOpponent: {}".format(gameName, other))  # noqa
                if game != "Fake":
                    print("\n")
                    if game:
                        winner = save.save(Location, True).readFile(gameName, "win")  # noqa
                        looser = name
                        if winner == name:
                            looser = other
                        print("GG!\n{} has beaten {}".format(winner, looser))
                    Functions.clear(10)
                gameName, users, Placed, multi = None, None, None, None
            else:
                Functions.clear()
        else:
            Functions.clear()
