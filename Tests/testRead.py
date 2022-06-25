import json

data = {}
with open("Tests/Test.json", "r") as f:
    data = json.loads(f.read())

def check(name):
    return data[name]