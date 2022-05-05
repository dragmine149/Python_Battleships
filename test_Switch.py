import Switch
import random
import string


# Test function to test the function ability of the script
def FuncTest():
    print("A")
    return "ABCDE"


# run a series of tests, like a lot
def SwitchTest():

    # Setup the data
    data = []
    for i in range(10):
        data.append(random.choice(string.ascii_letters) for _ in range(10))
        if random.randint(1, 3) == 1:
            data.append(FuncTest)
    Switch.data = data

    # Adds another error value
    data.append(random.choice(string.ascii_letters) for _ in range(10))

    # Loop through and get results
    results = []
    for item in data:
        results.append(Switch.Call(item))

    # loops through and checks for errors.
    bad = False
    badList = []
    for indexItem in len(range(results)):
        result = results[indexItem]
        if results != data[indexItem] and result != "ABCDE":
            badList.append([data[indexItem], result])  # Excepted, Recieved
            bad = True

    if bad:
        print(badList)
        assert False
        return False
    else:
        assert True
        return True


def test_Switch_STUFF():
    assert SwitchTest()
