"""
Switch class!

Adding switch statements to python (kinda)

NOTES:
- Yes i know they are in newer versions,
this program is designed to work with all py3 versions.
- Just a bunch of ifs
"""

# Make variable with all data
# atom gets annoyed here as data is [], but we want it to be that for later
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
    result = Switch.Call(callableFunction)

If you want to add in a callable function, this script will automatically call it once it gets selected  # noqa (why atom?)
Due to how python works, functions results will not be added through function call. E.g. "print({data})" for the result of error.
"""


def Call(argv=None):
    if argv is None:
        return callTest(default)
    for item in data:
        if item == argv:
            return callTest(item)
    return callTest(default)


def callTest(value):
    if callable(value):
        return value()
    return value
