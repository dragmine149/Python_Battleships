import os
import Functions
import platform
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

    '''
    getFile
    - If ApiFiles/credentials.json is not found, attempts to find it.
    '''
    def getFile(self):
        if not os.path.exists('ApiFiles/credentials.json'):
            cmdStart = "mv"
            if platform.system() == "windows":
                cmdStart = "move"

            self.levels = 0
            path = Functions.search(self.dir, 'credentials.json').Locate()[1]

            if path is not None:
                cmd = "{} {} ApiFiles".format(cmdStart, path)
                os.system(cmd)
                print('Moved File: {} to {}/ApiFiles'.format(path, self.dir))
            else:
                print('Failed to find in folders!')
                File = None
                while File is None:
                    File = input('Please enter location of google drive api token: ')  # noqa
                    if os.path.exists(File):
                        # moves and renames just in case.
                        os.system('{} {} ApiFiles/credentials.json'.format(cmdStart, File))  # noqa
                    else:
                        Functions.clear(2, "File not found!")
                        File = None
        else:
            print("File 'credentials.json' already found in directory!")
        return True

    def main(self):
        self.checkForFolder()
        self.getFile()


if __name__ == '__main__':
    Set = Setup('1jgyfEG0R76adWlnyzqDU030ps-mk4M20')
    Set.main()
