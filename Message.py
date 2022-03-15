# Document to sort the messages and output them. Easy to use the ui as well.
import os
tkInter = False
if tkInter:
    import Ui


# normal bog standard output. No special thing needed.
def sendMessage(message):
    print(message)


# Grid needs a different output as it's going to be interactable.
def sendGrid(grid):
    for y in grid:
        for x in y:
            print(x, end="")
        print()


# Options also need a different thing due to the buttons.
def Load(options):
    for file in range(len(options)):
        if os.path.exists(f"Saves/{options[file]}/win.txt"):
            print(f"{file + 1}: {options[file]} (finished)")
        else:
            print(f"{file + 1}: {options[file]}")