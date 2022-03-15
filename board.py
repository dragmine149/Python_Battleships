import Message


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
    Message.sendGrid(board)


if __name__ == "__main__":
    board = CreateBoard([10, 10])
    DisplayBoard(board)
