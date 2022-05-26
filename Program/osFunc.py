import os


"""
mkdir(path, targetDir=os.path.realpath(__file__))
- path -> path of files to make, support subfolders (e.g. Test/Test/Test)
- targetDir -> Where to start making the files, Default this file directory
"""
def mkdir(path, targetDir=os.path.realpath(__file__)):
    splitPath = path.split("/")  # gets all sub folders of path
    if os.name != "nt":  # ANNOYING WINDOWS
        splitPath = path.split("\\")

    # Change to targetDir
    os.chdir(targetDir)

    # Checks if sub folders
    if len(splitPath) > 1:
        # loops through
        currentPath = ""
        for dir in splitPath:
            currentPath = os.path.join(currentPath, dir)
            os.mkdir(currentPath)
        # returns the result, should be the same to begin with.
        return currentPath
    # returns the result of making the directory
    os.mkdir(path)
    return path
