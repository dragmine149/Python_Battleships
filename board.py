# Create the board in a 2d array.
def CreateBoard(size):
    board = []
    for _ in range(size[1]):  # _ = assaign it to nothing.
        x = []
        for _ in range(size[0]):  # x grid
            x.append('-')
        board.append(x)

    return board


# Loops through the board and prints it out.
def DisplayBoard(board):
    # board = json.loads(board)
    for y in board:
        for x in y:
            print(x, end="")
        print()


if __name__ == "__main__":
    board = CreateBoard([10, 10])
    DisplayBoard(board)
