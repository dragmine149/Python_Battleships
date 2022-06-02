import Functions


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
    def __init__(self, info, options, choiceData, external=None, back="Quit"):
        Functions.clear(.25, "Loading data...")
        self.info = info
        self.options = options
        self.choiceData = choiceData
        self.back = back
        self.external = external

    # shows menu using user inputs
    def showMenu(self):
        print("""{}
Options:
{}

Other Options:
00: {}""".format(self.info, self.options, self.back))
        if self.external is not None:
            for item in self.external:
                print("{}: {}".format(item, self.external[item]))

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
                Functions.Print('Key Error 2', 'red', 'bold')
                return None
            return None
        except NameError:
            Functions.warn(2, "Error in calling function! -> {}".format(self.choiceData[choice]))  # noqa E501
            return None
        except TypeError:
            Functions.clear(2, "Error in calling function! Missing arguments", "light red")  # noqa E501
            return None

    def getInput(self, choice=-0.5, values=()):
        if len(values) != 2:
            return "Values length is not 2"
        if choice != -0.5:
            # complete Choice
            return self.process(choice)
        while choice == -0.5:
            Functions.clear()  # clears

            # process
            choice = Functions.check("Your choice (number): ",
                                     extra=(self.showMenu(), None),
                                     rangeCheck=(values[0], values[1])).getInput()  # noqa E501
            result = self.process(choice)
            if result is None or result == "back":
                choice = -0.5
                continue
            return result
