import inspect

"""
Switch class!

Adding switch statements to python (kinda)

NOTES:
- Yes i know they are in newer versions,
this program is designed to work with all py3 versions.
- Just a bunch of ifs
"""

# Make variable with all data
# PERSONAL NOTE: DO NOT WORRY ABOUT THIS ERROR (just my ide)-- drag
data = []
default = None

"""
USAGE:

Import:
    Import Switch

When you want to add data to a statement:
    Switch.data = ["A", callableFunction]
    Switch.data.append("B")

When you want to change the default returned value:
    Switch.default = None

When you want to call a function:
    result = Switch.Call(callableFunction, data)

If you want to add in a callable function, this script will automatically call it once it gets selected  # noqa (why atom?)
If you want to call a function with arguments, pass the arguments in a triple '()', the arguments will be in order of the way they are in the triple.
"""


# Input of data
def Call(argv=None, DATA=None, pos=-1):
    if pos > -1:
        return callTest(data[pos], DATA)
    if argv is None:  # check if no data recieved, return default
        return callTest(default, DATA)
    for item in data:  # loop through all data until value found
        if item == argv:
            return callTest(item, DATA)
    return callTest(default, DATA)


# Function to check if can be calls and calls it
def callTest(value, data=None):
    if callable(value):
        if data is None:
            return value()
        else:
            # only passes through required argument length
            sig = inspect.signature(value)
            requiredLength = 0
            for param in sig.parameters.values():
                if param.default is not param.empty:
                    requiredLength += 1
            maxLength = len(sig.parameters)
            data = data[:maxLength]
            if len(data) < requiredLength:
                raise ValueError(
                    "Incorrect ammount of arguments provided!"
                )
            value(*data)
    return value
