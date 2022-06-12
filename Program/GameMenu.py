import Functions
import traceback


class menu:
    """
    menu(info, options, choiceData, back)
    info -> any information you want to display before the options
    options -> what you want to display
    choiceData -> what happens when that option is selected (MUST BE A DICT)
               -> Each element must be callable
    external -> options that aren't included (like -1)
    Back -> the message to go back. default: quit
    """
    def __init__(self,
                 info,
                 options=None,
                 choiceData=None,
                 external=None,
                 back="Quit"):
        Functions.clear(.25, "Loading data...")

        empty = options is None and choiceData is None and external is None
        if not callable(info) and empty:
            raise TypeError("Failed to find callable function!")

        self.callableFunction = None
        if callable(info):
            self.callableFunction = info
            info, options, choiceData, external = info()

        self.info = info
        self.options = options
        self.choiceData = choiceData
        self.back = back
        self.external = external

    # shows menu using user inputs
    def showMenu(self):
        if self.callableFunction is not None:
            self.info, self.options, self.choiceData, self.external = self.callableFunction()  # noqa E501
        print("""{}
Options:
{}

Other Options:
00: {}""".format(self.info, self.options, self.back))
        if self.external is not None:
            for item in self.external:
                print("{}: {}".format(item, self.external[item]))

    def __PrintTraceback(self):
        print('\033[41m----')
        traceback.print_exc()
        print('----\033[0m')

    # gets their choice and does stuff
    def process(self, choice):
        print(choice)
        if len(self.choiceData) == 1:
            for i in self.choiceData.values():
                return i(choice)

        # try and call their choice
        try:
            return self.choiceData[choice]()
        except KeyError:
            Functions.Print('Key Error 1', 'red', ['bold', 'underline'])
            # tries and calls all their choices
            try:
                return self.choiceData['All'](choice)
            except KeyError:
                self.__PrintTraceback()
                Functions.Print('Key Error 2', 'red', 'bold')
                return None
            return None
        except NameError as NE:
            self.__PrintTraceback()
            Functions.warn(2, "Error in calling function! -> {}\n\n{}".format(self.choiceData[choice], NE), "light red")  # noqa E501
            return None
        except TypeError as TE:
            self.__PrintTraceback()
            Functions.clear(2, "Error in calling function! Missing arguments\n\n{}".format(TE), "light red")  # noqa E501
            return None

    def getInput(self, choice=-0.5, values=()):
        if len(values) != 2:
            return "Values length is not 2"
        if choice != -0.5:
            # complete Choice
            result = self.process(choice)

            # Fix issue with going back after having a different choice input
            if result is None or result == "back":
                choice = -0.5
            else:
                return result

        while choice == -0.5:
            Functions.clear()  # clears

            # process
            choice = Functions.check("Your choice (number): ",
                                     (self.showMenu, None),
                                     rangeCheck=(values[0], values[1])).getInput()  # noqa E501
            result = self.process(choice)
            if result is None or result == "back":
                choice = -0.5
                continue
            return result
