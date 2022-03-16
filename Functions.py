import time
import os


class LocationConvert:
    def __init__(self, value):
        self.input = value
        self.letters = ""
        self.y = ""

    def _decode(self, s: str) -> int:
        s = s.lower()
        ref = ord('a') - 1
        v = 0
        exp = 1
        for c in reversed(s):
            v += (ord(c) - ref) * exp
            exp *= 26

        return v

    def Convert(self):
        if len(self.input) >= 2:
            # split string into number and letters
            self.input = self.input.lower()
            for v in self.input:
                if v.isdigit():
                    self.y += v
                else:
                    self.letters += v

            # convert letters into numbers
            return self._decode(self.letters) - 1, (int(self.y) - 1)
        else:
            clear(1, "Must be at least two digits, a letter (x) and a number (y)")  # noqa
            return None, None


def NumberRangeCheck(value, x):
    if value >= 0 and value <= x:
        return True
    return False


def clear(timeS=0, message=None):
    if message:
        print(message)
    time.sleep(timeS)
    os.system("clear")


class check:
    def __init__(self, request, extra=None, extraValue=None, rangeCheck=None, rangeCheckValue=None):  # noqa
        self.request = request
        self.extra = extra
        self.extraValue = extraValue
        self.rangeCheck = rangeCheck
        self.rangeCheckValue = rangeCheckValue
        self.Id = None
        self.check = None

    def _PassCheck(self):
        # Checks to see if the value is okay
        self.Id = int(self.Id)
        if self.rangeCheck is not None:  # checks if in certain range
            if callable(self.rangeCheck):
                if self.rangeCheckValue is None:
                    self.check = self.rangeCheck(self.Id)
                else:
                    self.check = self.rangeCheck(self.Id, self.rangeCheckValue)

                if self.check:
                    return self.Id
                else:
                    clear(1, "Out of range.")
                    self._CallExtra()
                    return self.InputDigitCheck()
            else:
                print("ERROR, range check is not a function!")
                return self.Id
        else:
            return self.Id

    def _FailCheck(self):
        # user notification
        clear(1, "Please enter a valid input")
        self._CallExtra()
        self.Id = None

    def _CallExtra(self):  # repeats any information the user needs to know
        if self.extra is not None:
            if callable(self.extra):
                if self.extraValue is None:
                    self.extra()  # call function
                else:
                    self.extra(self.extraValue)
            else:
                print(self.extra)

    def InputDigitCheck(self):  # noqa
        while not self.Id:
            self.Id = input(f"{self.request}")  # get input
            if not self.Id.isdigit() and len(self.Id) >= 2:  # check
                if not self.Id[1:].isdigit():
                    self._FailCheck()
                else:
                    return self._PassCheck()
            else:
                return self._PassCheck()


if __name__ == "__main__":
    lc = LocationConvert(input("Test: "))
    print(lc.Convert())
