import time
import os
import Message


def LetterConvert(letter):
    List = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    if letter.strip() != "":
        return List.index(letter.strip())
    return 0


def LocationInput(value):
    # split string into number and letters
    value = value.lower()
    letters = ""
    y = 0
    for v in value:
        if v.isdigit():
            y += int(v)
        else:
            letters += v

    # convert letters into numbers
    x = 0
    for letter in letters:
        x = LetterConvert(letter)
    return x, y - 1


def NumberRangeCheck(value, x):
    if value >= 0 and value <= x:
        return True
    else:
        return False


def clear(timeS=0, message=None):
    if message:
        Message.sendMessage(message)
    time.sleep(timeS)
    os.system("clear")


def PassCheck(Id, rangeCheck, rangeCheckValue, extra, extraValue, request):
    Id = int(Id)
    if rangeCheck is not None:
        if callable(rangeCheck):
            check = None
            if rangeCheckValue is None:
                check = rangeCheck(Id)
            else:
                check = rangeCheck(Id, rangeCheckValue)

            if check:
                return Id
            else:
                clear(1, "Out of range.")
                if callable(extra):
                    if extraValue is None:
                        extra()
                    else:
                        extra(extraValue)
                elif extra is not None:
                    Message.sendMessage(extra)
                return InputDigitCheck(request, extra, extraValue, rangeCheck, rangeCheckValue)  # noqa
        else:
            Message.sendMessage("ERROR, range check is not a function!")
            return Id
    else:
        return Id


def FailCheck(extra, extraValue):
    # user notification
    clear(1, "Please enter a valid input")
    if extra is not None:
        if callable(extra):
            if extraValue is None:
                extra()  # call function
            else:
                extra(extraValue)
        else:
            Message.sendMessage(extra)
    return None


def InputDigitCheck(request, extra=None, extraValue=None, rangeCheck=None, rangeCheckValue=None):  # noqa
    Id = None
    while not Id:
        Id = input(f"{request}")  # get input
        if not Id.isdigit():  # check
            if len(Id) >= 2:
                if not Id[1:].isdigit():
                    Id = FailCheck(extra, extraValue)
                else:
                    return PassCheck(Id, rangeCheck, rangeCheckValue, extra, extraValue, request)  # noqa
        else:
            return PassCheck(Id, rangeCheck, rangeCheckValue, extra, extraValue, request)  # noqa
