"""
colours.py, the best file to print colours out in the console!

Usage:
import colours
from colours import * (advanced recommended)
from colours import c (recommended)

Functions:
ConsoleFormat -- returns 2 lists of codes, not recommended use for quick.
Print(msg, colour, options) -- prints message out using selected colour and options.
c(colour) -- returns the format for the code inputted.

Extra help:
- Look at the functions test_Test() for example on how to run the program
- Copy codes from ConsoleFormat if needed.
"""
def ConsoleFormat():
    # defines the colours and what they do
    format = {
        'reset': '\033[0m',
        'bold': '\033[01m',
        'disable': '\033[02m',
        'italic': '\033[03m',
        'underline': '\033[04m',
        'reverse': '\033[07m',
        'strikethrough': '\033[09m',
        'invisible': '\033[08m',
    }
    colours = {
        'fg': {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'orange': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'cyan': '\033[36m',
            'light grey': '\033[37m',
            'dark grey': '\033[90m',
            'light red': '\033[91m',
            'light green': '\033[92m',
            'yellow': '\033[93m',
            'light blue': '\033[94m',
            'pink': '\033[95m',
            'light cyan': '\033[96m'
        },
        'bg': {
            'black': '\033[40m',
            'red': '\033[41m',
            'green': '\033[42m',
            'orange': '\033[43m',
            'blue': '\033[44m',
            'purple': '\033[45m',
            'cyan': '\033[46m',
            'light grey': '\033[47m'
        }
    }
    return format, colours


class Print:
    """
    Colours:
    foreground : {
        black, red, green, orange, blue, purple, cyan, light grey, dark grey,
        light red, light green, yellow, light blue, pink, cyan
    }
    background : {
        black, red, green, orange, blue, purple, cyan, light grey
    }
    options = [
        reset, bold, disable, underline, reverse, strikethrough, invisible
    ]
    """

    def __init__(self, msg, colour=[None, None], options=[
        None, None, None, None, None, None, None
    ]):
        self.msg = msg

        # gets the colour and checks it
        self.colour = self.__ColourCheck(colour)
        self.options = options
        if not self.colour:
            # print if no colour, saving time
            print(msg)
        else:
            # print with colour
            self._format, self._colours = ConsoleFormat()
            self.__output()

    def __ColourCheck(self, colour):
        if colour is None:  # if none, return
            return False
        if isinstance(colour, list):
            if len(colour) > 2:  # if more than 2, shrink
                return colour[0:1]
            if len(colour) == 2:
                # only care if they are both none
                if colour[0] is None and colour[1] is None:
                    return False
                return colour
            # assume foreground
            if len(colour) == 1:
                return [colour[0], None]
        return [colour, None]

    def __getOptionValues(self):
        optStr = ''
        _FormatOptions = [
            'reset',
            'bold',
            'disable',
            'underline',
            'reverse',
            'strikethrough',
            'invisible'
        ]
        # checks if string
        if isinstance(self.options, str):
            if self.options in _FormatOptions:
                return self._format[self.options]

        # loops through and get all the options
        for option in self.options:
            if option in _FormatOptions:
                optStr += self._format[option]
        return optStr

    def __output(self):
        # Take colour and message and print them correctly
        colourValues = ['', '']

        # get the foreground colour value
        for i in range(2):
            if self.colour[i] is None:
                colourValues[i] = ''
                break

            # background and foreground colour set
            try:
                colourValue = self.colour[i].lower()
                if i == 0:
                    colourValues[i] = self._colours['fg'][colourValue]
                if i == 1:
                    colourValues[i] = self._colours['bg'][colourValue]

            except KeyError:
                colourValues[i] = ''  # don't include one if not present
            except AttributeError:
                colourValue[i] = ''

        # print out colours
        print('{}{}{}{}'.format(self.__getOptionValues(),
                                colourValues[0],
                                colourValues[1],
                                self.msg),
              end='')  # no end so it reset bg colour as well

        # reset to normal afterwards
        print(self._format['reset'])


"""
c(choice)
-- returns the code of the choice, breaks if fails to find.
-- if multiple options, returns the first one found.

-- Usage: [mode][colour/format]
--- mode > One of the : features, fg, bg
--- colour/format > One of the possible options in ConsoleFormat()
--- leave blank to reset the colours used.

Example usage:
print(c('fgr') + 'Hello' + c() + c('bgg') + 'World' + c())
- prints "Hello" in red, "World" in white with a green background.
"""
def c(choice=None):
    cR = colourRetrieve(choice)
    return cR.colourCode


class colourRetrieve:
    """
    Usage: [f, bg, fg][colour, result]
    """
    def __init__(self, choice=None):
        self.format, self.colours = ConsoleFormat()
        
        # reset if no input
        if choice is None or len(choice) == 0:
            self.colourCode = self.format['reset']
        else:
            mode = self.__getMode(choice)
            self.colourCode = self.format['reset']

            if mode[0] == 'colours':
                self.colourCode = self.__getColour(choice, mode)
            if mode[0] == 'format':
                self.colourCode = self.__getFormat(choice)
    
    def __getMode(self, choice):
        # take first 2 and get result
        if len(choice) == 1:
            return 'c', 'fg'
        f2L = choice[0] + choice[1]
        
        # process result
        if f2L == 'bg':
            return 'colours', 'bg'
        if f2L == 'fg':
            return 'colours', 'fg'
        if choice[0] == 'f':
            return 'format', ''
        return 'c', 'fg'  # default
        
    def __getColour(self, choice, mode):
        # checks what needs to be found
        if mode[0] != 'c':
            choice = choice[2:]

        # checks if whole word
        if choice in self.colours[mode[1]]:
            return self.colours[mode[1]][choice]
        
        # checks for first letter
        for option in self.colours[mode[1]]:
            if option[:len(choice)] == choice:
                return self.colours[mode[1]][option]
        
            # checks for multi word
            spltStr = option.split(' ')
            if choice[0] == 'l':
                if option[6:6 + len(choice[1:])] == choice[1:]:
                    return self.colours[mode[1]][option]
        
        raise ValueError("Invalid colour inputted!")
    
    def __getFormat(self, choice):
        choice = choice[1:]
        # check if word
        if choice in self.format:
            return self.format[choice]
            
        # check for letter
        for option in self.format:
            if option[:len(choice)] == choice:
                return self.format[option]
        
        raise ValueError('Invalid format option inputted!')


# run python colours.py to see the results from this
def test_Test():
    print("Normal Colour")
    print('{}Hello{}World{}'.format(c('fgr'), c() + c('bgg'), c()))
    Print("Hello World", ["dark grey", "cyan"], ["bold", "underline"])
    return True


if __name__ == '__main__':
    assert test_Test()