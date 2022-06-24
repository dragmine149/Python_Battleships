import importlib
import random
import string
import os
print(os.path.abspath('.'))
Switch = importlib.import_module('./Files/Switch', 'Program')


# Test function to test the function ability of the script
def FuncTest():
    print("A")
    return "ABCDE"


def argFuncTest(A, B="c"):
    print(A, B)
    return "ABCDE"


# run a series of tests, like a lot
def SwitchTest():

    # Setup the data
    data = []
    for i in range(10):
        inItem = random.choice(string.ascii_letters)
        data.append(inItem)
        if random.randint(1, 3) == 1:
            data.append(FuncTest)
        if random.randint(1, 7) == 4:
            data.append(argFuncTest)
    Switch.data = data

    # Adds another error value
    data.append(random.choice(string.ascii_letters) for _ in range(10))

    # Loop through and get results
    results = []
    for item in data:
        try:
            results.append(Switch.Call(item, ("A", "C", "D")))
        except ValueError:
            results.append(Switch.Call(item, ("A", "cc")))

    # loops through and checks for errors.
    goodList = []
    for indexItem in range(len(results)):
        # Result should be the input, or the function called to be good
        result = results[indexItem]
        if result == data[indexItem]:
            goodList.append(result)
        elif result == "ABCDE":
            goodList.append(result)

    # Makes a bad list with all the results that was not in the good list
    bad = False
    badList = []
    for item in goodList:
        if item not in data and item != "ABCDE":
            badList.append(item)
            bad = True

    if bad:
        print(badList)
        assert False
        return False
    else:
        assert True
        return True


def test_Switch_STUFF():
    end = SwitchTest()
    print(end)
    assert end


if __name__ == '__main__':
    test_Switch_STUFF()
