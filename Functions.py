import time
import os


def NumberRangeCheck(value, x):
    if value >= 0 and value <= x:
        return True
    else:
        return False


def clear(timeS=0, message=None):
    if message:
        print(message)
    time.sleep(timeS)
    os.system("clear")


def InputDigitCheck(request, extra=None, extraValue=None, rangeCheck=None, rangeCheckValue=None):  # noqa
    Id = None
    while not Id:
        Id = input(f"{request}")  # get input
        if not Id.isdigit():  # check
            Id = None  # reset

            # user notification
            clear(1, "Please enter a valid input")
            if extra is not None:
                if callable(extra):
                    if extraValue is None:
                        extra()  # call function
                    else:
                        extra(extraValue)
                else:
                    print(extra)
        else:
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
                            print(extra)
                        return InputDigitCheck(request, extra, extraValue, rangeCheck, rangeCheckValue)  # noqa
                else:
                    print("ERROR, range check is not a function!")
                    return Id
            else:
                return Id
