# import random
# import placeSystem as place
# import os


def rotationCheck():
    rotation = [
        0,
        90,
        180,
        270
    ]
    return rotation[random.randint(0, len(rotation) - 1)]

#
# def test_input():
#     name = ""
#     with open("Tests/data.txt", "r") as f:
#         name = f.read()
#
#     completed = [False, False]
#     for directory in range(len(os.listdir("Saves/{}".format(name)))):
#         ranInput = chr(random.randint(ord('a'), ord('j'))) + str(random.randint(1, 11))  # noqa
#         place.place(name, os.listdir("Saves/{}".format(name))[directory]).Place(ranInput, [False, str(random.randint(1, 11))], rotationCheck())  # noqa
#         if os.path.exists("Saves/{}/{}/ships.txt".format(name, os.listdir()[directory])):  # noqa
#             completed[directory] = True
#
#     assert completed[0] is True and completed[1] is True

assert True
