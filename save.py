# The old save system
# Currently in progress of moving to SaveSystem.py

import Functions
import os
import json
import shutil
os.chdir(os.path.dirname(os.path.realpath(__file__)))





def UpdateFile(data, path, o="grid"):
    with open('{}/{}.txt'.format(path, o), 'w+') as file:
        file.write(str(json.dumps(data)))


def read(game, user, o="grid"):
    data = None
    with open('Saves/{}/{}/{}.txt'.format(game, user, o), 'r') as file:
        data = file.read()
        data = json.loads(data)
    return data
