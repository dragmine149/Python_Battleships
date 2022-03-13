import time
import os
import json


def save(data, name, users):
    if not os.path.exists("Saves"):
        os.mkdir("Saves")
    if os.path.exists(f"Saves/{name}"):
        print("Please enter a name that has not already been used.")
        time.sleep(1)
        return None
    else:
        os.system(f"mkdir Saves/{name}")
        os.system(f"mkdir Saves/{name}/{users[0]}")
        UpdateFile(data, f"Saves/{name}/{users[0]}", "grid")
        os.system(f"mkdir Saves/{name}/{users[1]}")
        UpdateFile(data, f"Saves/{name}/{users[1]}", "grid")
        return True


def UpdateFile(data, path, o):
    with open(f'{path}/{o}.txt', 'w+') as file:
        file.write(str(json.dumps(data)))


def read(game, user):
    data = None
    with open(f'Saves/{game}/{user}/grid.txt', 'r') as file:
        data = file.read()
        data = json.loads(data)
    return data
