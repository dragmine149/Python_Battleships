import DriveApi as Drive
import os
import Functions

class Setup:
    def __init__(self, Folder):
        self.Folder = Folder

    '''
    checkForFolder
    - Checks if the folders required for drive have been made, and if not make them.
    '''
    def checkForFolder(self):
        if not os.path.exists('ApiFiles'):
            os.mkdir('ApiFiles')

    '''
    getFile
    - If ApiFiles/token.json is not found, attempts to find it.
    '''
    def getFile(self):
        if not os.path.exists('ApiFiles/token.json'):
            if os.path.exists('token.json'): # working dir
                os.system('mv token.json ApiFiles/')  # fix for windows
            else:
                File = None
                while File is None:
                    File = input('Please enter location of google drive api token: ')  # add better info
                    if os.path.exists(File):
                        os.system('mv {} ApiFiles/'.format(File))  # fix with windows, add file check
                    else:
                        Functions.clear(2, "File not found!")
                        File = None
        return True
    
    def test(self):
        try:
            api = Drive.Api(self.Folder)
        except Exception:  # change maybe?
            print('Failed to setup API!')

    def main(self):
        self.checkForFolder()
        self.getFile()
        self.test()

if __name__ == '__main__':
    Set = Setup('1jgyfEG0R76adWlnyzqDU030ps-mk4M20')
    Set.main()
