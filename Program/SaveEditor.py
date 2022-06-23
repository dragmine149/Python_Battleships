import importlib
import os
readchar = importlib.import_module('.readchar', 'Files.readchar')
newSave = importlib.import_module('Files.newSave')
colours = importlib.import_module('Files.colours')
Functions = importlib.import_module('Files.Functions')
Settings = importlib.import_module('Files.Settings')


class saveEditor:
    # basic setup
    def __init__(self):
        self.folder = os.path.abspath(Settings.request("path"))
        self.files = []
        self.activeFile = 0
        self.columnCount = 4

    # header
    def ShowDisplay(self):
        Functions.clear()
        print('''--------------------------------------------------------------------
Save Editor

Current Folder: {}
--------------------------------------------------------------------'''.format(self.folder))  # noqa E501

    # lets the user change directory without having to navigate though dirs.
    def __ChangeDirectory(self):
        self.folder = os.path.abspath(Functions.changePath()[1])

    # Returns a custom list of all the files in the specified directory.
    def __ListFiles(self):
        files = ['..']  # so they can go up directory.
        newFiles = os.listdir(self.folder)
        newFiles.sort()
        files.extend(newFiles)  # adds the folders onto the main list.
        self.folderLength = len(files)
        return files

    # Sorts the files and makes them into a printable list.
    # Also adds a currently selected indicator
    def __SortFiles(self):
        files = self.__ListFiles()
        newFileList = []
        tempList = []
        for file in range(len(files)):

            fileData = ""
            if file == self.activeFile:  # checks for currently active file
                fileData += "> "  # signifies active file.
                self.activeFileIndex = [len(newFileList), len(tempList) + 1]

            # if os.path.isdir(os.path.join(self.folder, files[file])):
            #     fileData += colours.c('cyan')

            fileData += files[file]

            # if os.path.isdir(os.path.join(self.folder, files[file])):
            #     fileData += colours.c()

            tempList.append(fileData)

            # make sure only columns of X
            if len(tempList) == self.columnCount:
                newFileList.append(tempList)
                tempList = []

        if len(tempList) > 0:
            newFileList.append(tempList)

        return newFileList

    # Prints out all the files
    def __ShowFiles(self):
        self.files = self.__SortFiles()

        length_lst = [len(item) for row in self.files for item in row]

        col_wdth = max(length_lst)

        for row in self.files:
            print(''.join(item.ljust(col_wdth + 2) for item in row))

    # Update the screen
    def __UpdateScreen(self):
        self.ShowDisplay()
        self.__ShowFiles()

    # Move the cursor
    def __Move(self, value):
        if self.activeFile + value >= 0 and self.activeFile + value < self.folderLength:  # noqa E501
            self.activeFile += value
            self.__UpdateScreen()
            return

        Functions.clear(.1, "Invalid movement!", "red")
        self.__UpdateScreen()
        return

    # Cursor Controlls
    def __MoveCursor(self):
        a = True
        while a:
            print("""
----------------------
Options:
----------------------
Movement:       Other:
---------       ------
W: Up           C: Change Directory
A: Left         Q: Quit Program
S: Down
D: Right
            """)
            c = readchar.readchar().lower()
            if c == "q":
                a = False
            if c == "w":
                self.__Move(-self.columnCount)
            if c == "a":
                self.__Move(-1)
            if c == "s":
                self.__Move(self.columnCount)
            if c == "d":
                self.__Move(1)
            if c == "\r":
                # sorts ouut file stuff.
                file = self.files[self.activeFileIndex[0]][self.activeFileIndex[1] - 1]  # noqa E501
                file = file.strip("> ")
                if os.path.isdir(os.path.join(self.folder, file)):
                    if file != "..":
                        self.folder = os.path.join(self.folder, file)
                    else:
                        self.folder = os.path.split(self.folder)[0]
                else:
                    # Functions.clear(1, "This is a file!", "red").
                    FileEditor = File(self.folder, file)
                    FileEditor.Main(self)

                self.activeFile = 0
                self.activeFileIndex = []
                self.__UpdateScreen()
            if c == "c":
                self.__ChangeDirectory()

    # main
    def Main(self):
        self.__UpdateScreen()
        self.__MoveCursor()


class File:
    def __init__(self, file, name=''):
        self.file = file
        self.saveData = newSave.save({
            'name': name,
            'path': file
        })

    def readFile(self):
        return self.saveData.readFile()

    def Main(self, se):
        Functions.clear()
        fileData = self.readFile()
        se.ShowDisplay()
        print(fileData)
        input()


if __name__ == "__main__":
    se = saveEditor()
    se.Main()
