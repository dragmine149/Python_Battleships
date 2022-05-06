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
        inItem = random.choice(string.ascii_letters)
        data.append(inItem)
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
    for indexItem in range(len(results)):
        result = results[indexItem]
        print(result, data[indexItem])
        print(result != data[indexItem])
        print(result != "ABCDE")
        print(str(result) != str(data[indexItem]) and result != "ABCDE")
        if str(result) != str(data[indexItem]) or str(result) != "ABCDE":
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
    end = SwitchTest()
    print(end)
    assert end
    
if __name__ == '__main__':
    test_Switch_STUFF()
