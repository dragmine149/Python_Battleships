import os
import importlib
import shutil
Functions = importlib.import_module('Files.Functions')
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class Setup:
    def __init__(self, Folder):
        # Get informaton about where this file is stored
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
    def getLocation(self, cmdStart):
        File = None
        while File is None:
            File = input('Please enter the location of `credentials.json` (leave blank to search again): ')  # noqa E501
            if File == '':  # Search again
                return

            # If correct file, move
            if os.path.exists(File):
                shutil.move(File, 'ApiFiles/credentials.json')
                return File

            # shout at user
            Functions.clear(2, "File not found!", "red")
            File = None

    def getFile(self):
        # Check if file is already there and returns
        if os.path.exists('ApiFiles/credentials.json'):
            return True

        # Sets up the command. THANKS WINDOWS!!!
        cmdStart = "mv" if os.name == "nt" else "move"

        # Searches for the path
        path = None
        while path is None:
            try:
                path = Functions.search(self.dir, 'credentials.json', 4).Locate()
                print(path)
                
                if path is not None:
                    # If there is nothing returned, no path.
                    if len(path) == 0:
                        path = None
                    
                    # If something got returned, use that
                    elif len(path) == 1:
                        path = path[0]
                    
                    # If multiple items got returned, ask the user to choose one
                    elif len(path) > 1:
                        print('Multiple `credentials.json` files found!')
            except (KeyError, IndexError):  # any errors, no path
                path = None

            if path is None:
                print("Failed to find path in folders")
                path = self.getLocation(cmdStart)  # gets the user to input location
                if path is not None:
                    return True
                continue
            
            print(f'Moving {path} to ApiFiles/credentials.json')
            shutil.move(path, 'ApiFiles/credentials.json')
            return True

    def main(self):
        try:
            self.checkForFolder()
            return self.getFile()
        except Exception: # catch anything, we dont really care
            Functions.PrintTraceback()
            return 'Saves'

if __name__ == '__main__':
    Set = Setup('1jgyfEG0R76adWlnyzqDU030ps-mk4M20')
    Set.main()
