import os
import Functions
import platform
os.chdir(os.path.dirname(os.path.realpath(__file__)))

class Setup:
    def __init__(self, Folder):
        self.Folder = Folder

    '''
    checkForFolder
    - Checks if the folders required for drive have been made, and if not make them.
    '''
    def checkForFolder(self):
        if not os.path.exists('ApiFiles'):
            print('Making folder {}/ApiFiles'.format(os.path.dirname(os.path.realpath(__file__))))
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

            if os.path.exists('credentials.json'): # working
                cmd = '{} credentials.json ApiFiles'.format(cmdStart)
                os.system(cmd)
                print('Moved file {}/credentials.json!'.format(os.path.dirname(os.path.realpath(__file__))))
            elif os.path.exists('../credentials.json'):  # checks 1 directory above as well.
                cmd = "{} ../credentials.json ApiFiles".format(cmdStart)
                os.system(cmd)
                print('Moved file {}credentials.json!'.format(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))))
            else:
                File = None
                while File is None:
                    File = input('Please enter location of google drive api token: ')  # add better info
                    if os.path.exists(File):
                        os.system('{} {} ApiFiles/'.format(cmdStart, File))  # fix with windows, add file check
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
