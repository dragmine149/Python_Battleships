import os
import importlib
Functions = importlib.import_module('Files.Functions')
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class Setup:
    def __init__(self, Folder):
        self.Folder = Folder
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.parentdir = os.path.abspath(os.path.join(self.dir, '../'))

    '''
    checkForFolder
    - Checks if the folders required for drive have been made
      and if not make them.
    '''
    def checkForFolder(self):
        if not os.path.exists('ApiFiles'):
            print('Making folder {}/ApiFiles'.format(self.dir))
            os.mkdir('ApiFiles')

    # Asks the user for where the file is
    def getLocation(self):
        File = None
        while File is None:
            File = input('Please enter the location of `credentials.json` (leave blank to search again): ')  # noqa E501
            if File == '':  # Search again
                return

            # If correct file, move
            if os.path.exists(File):
                os.system('{} {} ApiFiles/credentials.json'.format(cmdStart, File))  # noqa E501
                return File

            # shout at user
            Functions.clear(2, "File not found!")
            File = None

    def getFile(self):
        # Check if file is already there and returns
        if os.path.exists('ApiFiles/credentials.json'):
            return True

        # Sets up the command. THANKS WINDOWS!!!
        cmdStart = "mv"
        if os.name == "nt":
            cmdStart = "move"

        # Searches for the path
        path = None
        while path is None:
            path = Functions.search(self.dir, 'credentials.json').Locate()[1]

            if path is None:
                print("Failed to find path in folders")
                path = self.getLocation()  # gets the user to input location
                if path is not None:
                    return path
                continue
            os.system('{} {} ApiFiles/credentials.json'.format(cmdStart, File))  # noqa E501

    def main(self):
        self.checkForFolder()
        self.getFile()


if __name__ == '__main__':
    Set = Setup('1jgyfEG0R76adWlnyzqDU030ps-mk4M20')
    Set.main()
