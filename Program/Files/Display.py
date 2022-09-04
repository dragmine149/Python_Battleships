import importlib
import os
import copy
Functions = importlib.import_module("Files.Functions")
readchar = importlib.import_module('.readchar', 'Files.readchar')

class Display:
    """A class to show information on the display via different functions
    """
    def __init__(self, headerText = "Python Battleships! Made by dragmine149") -> None:
        """Loads the Display class
        """
        # Load the class settings
        print("Display class loading")
        self.dashTextSize = os.get_terminal_size().columns
        self.ColumnCount = 4
        
        # store data about recent information
        self.options = []
        self.negOptions = []
        self.list = False
        self.cursorPosition = 0
        self.headerText = headerText
    
    def __PrintDashText(self):
        """Prints enough '-' on the terminal window to take up the whole width but not any extra lines
        """
        # Prints the header of things
        print(Functions.colours.c("green"), end='')
        print("-" * self.dashTextSize, end='')
        print(Functions.colours.c())
    
    def Header(self, text = ""):
        """Shows a header

        Args:
            text (str, optional): What text to show on the header. Defaults to "Python Battleships built by dragmine149".
        """
        # sets to the default stored text if none is found
        if text == "":
            text = self.headerText
        
        # Prints the header out onto the display
        self.__PrintDashText()
        print(text)
        self.__PrintDashText()
    
    def __WorkOutSpace(self, optIndex, optLength):
        """Works out how many spaces need to be added in to make everything in line

        Args:
            optIndex (int): the current index of the option
            optLength (int): the ammount of options overall

        Returns:
            string: the ammount of extra spaces to return
        """
        strOptIndex = str(optIndex)
        strOptLength = str(optLength)
        
        return " " * (len(strOptLength) - len(strOptIndex))

    def __OptionsOutputList(self, optionsIn):
        options = []
        negOptions = []
        
        if type(optionsIn) == tuple:
            negOptions = optionsIn[1]
            options = optionsIn[0]

        # loop through all items in options
        for optIndex in range(len(options)):
            opt = options[optIndex]
            
            # add spaces accordingly
            r = self.__WorkOutSpace(optIndex, len(options))
            
            if len(options) < 10 and len(negOptions) > 0:
                r += " "
            
            # print out item
            print("{}{}: {}".format(r, optIndex, opt))
        
        # only print if there aare options
        if len(negOptions) > 0:
            print()
            for optIndex in range(len(negOptions)):
                opt = negOptions[optIndex]
                print("-{}: {}".format(optIndex + 1, opt))
    
    def OptionsListDisplay(self, options=[], negOptions=[]):
        """Shows the options in a list view display

        Args:
            options (list, optional): The options to show. Defaults to [].
            negOptions (list, optional): The negative options to show (e.g. back, load from X). Defaults to [].
        """
        
        return Functions.check("Your Choice (Number): ", 
                               (self.__OptionsOutputList, (options, negOptions)),
                               (-len(negOptions), len(options))).getInput()
    
    def OptionsGridDisplay(self, options=[], position=0):
        """Shows the options in a grid display

        Args:
            options (list, optional): The options to show. Defaults to [].
            negOptions (list, optional): The negative options to show (e.g. back, load from X). Defaults to [].
            position (int, optional): The position of where the cursor currently is
        """
        # setup some values
        newList = []
        mainList = []
        
        # split the list into rows of X
        for opt in options:
            newList.append(opt)
            if len(newList) == self.ColumnCount:
                mainList.append(newList)
                newList = []
        
        # Loop through the list and print it
        mainList.append(newList)      
        
        # loop through all the lists to see 
        for table in range(len(mainList)):
            for item in range(len(mainList[table])):
                if item + (table * self.ColumnCount) == position:
                    mainList[table][item] = "> " + mainList[table][item]
                    break
        
        # loop through the list and output the display
        length_lst = [len(item) for row in mainList for item in row]
        col_wdth = max(length_lst)
        for rowIn in range(len(mainList)):
            row = mainList[rowIn]
            print(''.join(item.ljust(col_wdth + 2) for item in row))
        
        # output info on how to use ui
        print("""
----------------------
Options:
----------------------
Movement:
----------------------
W: Up       A: Left
S: Down     D: Right
            """)
    
    def Options(self, options=[], negOptions=[], list = False):
        """Main function which controlls all the options and what to show

        Args:
            options (list, optional): The options. Defaults to [].
            negOptions (list, optional): The options negativly (require -X to use). Defaults to [].
            list (bool, optional): Whever to view them in a list or not. Defaults to False.

        Returns:
            int: Selected option
        """
        self.options = options
        self.negOptions = negOptions
        
        self.jointOptions = copy.deepcopy(self.options)
        for opt in self.negOptions:
            self.jointOptions.append(opt)
        
        if list:
            return self.OptionsListDisplay(options, negOptions)
        self.OptionsGridDisplay(self.jointOptions)
        return self.MoveCursor()

    def MoveCursor(self):
        chosen = False
        while not chosen:
            c = readchar.readchar().lower()
            if c == "w":
                self.cursorPosition -= self.ColumnCount
            elif c == "a":
                self.cursorPosition -= 1
            elif c == "s":
                self.cursorPosition += self.ColumnCount
            elif c == "d":
                self.cursorPosition += 1
            elif c == "\r":
                chosen = True
                return self.cursorPosition

            if self.cursorPosition < 0:
                self.cursorPosition = 0
            if self.cursorPosition > len(self.jointOptions) - 1:
                self.cursorPosition = len(self.jointOptions) - 1
            
            print("\033[%d;%dH" % (0, 0))
            # print("\x1b[2J\x1b[H", end='')
            self.Header()
            self.OptionsGridDisplay(self.jointOptions, self.cursorPosition)
        

if __name__ == "__main__":
    print("\x1b[2J\x1b[H", end='')
    dis = Display("""Python Battleships

    Creator: Dragmine149
    Github: https://github.com/dragmine149/Python_Battleships""")
    dis.Header()
    choice = dis.Options(["Load Game", "Make Game", "Settings", "Mods"], ["Quit"])