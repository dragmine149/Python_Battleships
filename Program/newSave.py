import os
import Functions
import json
import shutil
import pickle
# Stores whever program is stored.
filePath = os.path.dirname(os.path.realpath(__file__))
os.chdir(filePath)


class save:
    """
    data -> {
        name -> name of the file to create (supports subdirs)
        path -> where to save the file
        json -> whever to encode the data in json
    }
    """
    def __init__(self, data={'name': '',
                             'path': '',
                             'Json': False}):
        # removes characters from the path
        self.path = data['path'].rstrip()
        self._api = self.__loadApi()
        try:
            self._json = data['Json']
        except KeyError:
            self._json = False
        self.__Foldercheck()
        if data['name'] is not None and data['path'] is not None:
            self.data = data

    """
    __loadApi()
    - Attempts to load the google drive api.
    - If api not found, will ask user to either install (WIP) or change path
    """
    def __loadApi(self):
        # Attempts to load Api
        # Remove api bypass?
        if self.path.find("/") == -1 and self.path.find("\\") == -1 and self.path != "Saves" and self.path != "Data":  # noqa E501
            # Import drive and do stuff
            try:
                import DriveApi as d
                return d.Api(self.path)
            except ImportError:
                Functions.clear()
                Functions.warn(2, "Google drive api not installed!")
                # Asks the user if they want to change location
                change = input("Please enter the new path (type 'install' to install googledrive api): ")  # noqa E501
                if change.lower() == 'install':
                    os.quit(self.__installDrive())
                self.path = change.rstrip()
                return self.__loadApi()

    """
    __Foldercheck()
    - Checks if core folders are made, else make them
    """
    def __Foldercheck(self):
        # Data for files
        if not os.path.exists("Saves"):
            os.mkdir("Saves")
        if not os.path.exists("Saves/.Temp"):
            os.mkdir("Saves")

        # Settings and other data
        if not os.path.exists("Data"):
            os.mkdir("Data")

    """
    _Json(data, save)
    data -> data to jsonify
    save -> to encode or to decode
    - Encodes data with json, this makes it harder to edit normally
    """
    def _Json(self, data, fileData, save=False):
        oldData = data # backup
        
        if not save:  # loading
            data = pickle.loads(fileData)  #  decode binary first
            if self._json:
                data = json.loads(data)
            return data
        
        if self._json:
            data = json.dumps(data)  # encode json first
        data = pickle.dump(data, fileData)
        return data

    """
    __replace(path)
    path -> string to replace data
    - If not windows os, replace \\ with nothing
    """
    def __replace(self, path):
        if os.name != "nt":
            return path.replace("\\", "")

    """
    __split(data)
    data -> path to split into folders
    - Splits path into folders depending on os
    """
    def __split(self, data):
        return data.split(self.__slash())

    """
    __slash()
    - returns either \\ or / depending on os
    """
    def __slash(self):
        if os.name == "nt":
            return "\\"
        return "/"

    """
    makeFolder(sub, replace)
    sub -> Path of subdirectories under the main directories ('/e/e')
    replace -> whever to set the last directory created
    """
    def makeFolder(self, sub=None, replace=False):
        if self._api:
            # Makes folder on drive
            folderId = self._api.UploadData({
                'name': self.data['name'],
                'folder': self.path
            }, True)

            # Check for sub folder path
            if sub is not None:
                splitInfo = self.__split(sub)
                newFolder = folderId['id']

                # Makes sub folders on drive
                for item in splitInfo:
                    newFolder = self._api.UploadData({
                        'name': item,
                        'path': newFolder
                    }, True)['id']

                folderId = newFolder

            # replace and return
            if replace:
                self.path = folderId
            return folderId['id']

        # normal local folder
        path = self.path
        if self.data['name'] != '':
            path = os.path.join(self.path, self.data['name'])

        # this is because os.path.exists doesn't like it but os.mkdir AAAAAAA
        Npath = self.__replace(path)
        if not os.path.exists(Npath):
            os.mkdir(Npath)

        if sub is not None:
            # change, make, change
            if not os.path.exists(os.path.join(path, sub)):
                os.chdir(path)
                os.makedirs(sub)
                os.chdir(filePath)

        if replace:
            self.path = path
            if sub is not None:
                self.path = os.path.join(path, sub)

        return path

    """
    writeFile(data, overwrite=False)
    data -> data to save
    overwrite -> whever to overwrite the data on drive. Dones't work locally.
    name -> name of the file, just in case the file needs to be different from the current name inputted.
    - Save data to a file
    """  # noqa E501
    def writeFile(self, data, overwrite=False, name=""):
        if data is None:
            return None
        if name == "":
            name = self.data['name']

        # Makes the file with the data in the temparay location
        tempLocation = "Saves/.Temp/{}".format(name)
        with open(tempLocation, 'w+') as tempFile:
            tempFile.write(self._Json(data, True))

        if self._api:
            # uploads to drive
            id = self._api.UploadData({
                'name': name,
                'path': tempLocation,
                'folder': self.path,
            }, overwrite=overwrite)
            os.remove(tempLocation)  # remove local copy
            return id
        slash = self.__slash()
        # moves file to where it should be saved
        shutil.move("Saves{}.Temp{}{}".format(slash, slash, name),
                    "{}{}{}".format(self.__replace(self.path), slash, name))  # noqa E501
        return "{}{}{}".format(self.path, slash, name)

    """
    readFile
    - returns the data from a file.
    - If not found, returns False
    """
    def readFile(self, name="", joint=False):
        # Multi use case
        if name == "":
            name = self.data['name']
        if name != "" and joint:
            name = os.path.join(self.data['name'], name)

        slash = self.__slash()
        path = "{}{}{}".format(self.path, slash, name)
        if self._api:
            saveLoc = "Saves/.Temp/{}".format(name)
            Id = self._api.DownloadData({
                'Id': name,
                'path': saveLoc
            })
            # If can't find file, attempt to search
            if Id is False:
                files = self._api.ListFolder()
                for file in files:
                    if file['name'] == name:
                        Id = self._api.DownloadData({
                            'Id': file['id'],
                            'path': saveLoc
                        })
                        break

            if isinstance(Id, str):
                with open(Id, 'r') as file:
                    return self._Json(file.read())
            return Id

        # local read area
        # Don't need to add name here as done eariler
        path = self.__replace(path)
        if os.path.exists(path):
            with open(path, 'r') as file:
                return self._Json(file.read())
        Functions.Print("Failed to find data in path: {}".format(path), "red")
        return False

    """
    ls(dir)
    dir -> whever to include files (false) or not (true)
    - Same as 'ls' on 'posix' (os.name) systems.
    """
    def ls(self, dir=False):
        # use api if alvalible.
        if self._api:
            return self._api.ListFolder(dir=dir)

        # Local area
        if os.path.exists(self.path):
            dirData = os.listdir(self.path)
            if not dir:
                # return if all files wanted
                return dirData

            # Removes all none files
            newDirList = []
            for item in dirData:
                if os.path.isdir(os.path.join(self.path, item)):
                    newDirList.append(item)
            return newDirList
        return None  # if directory not found

    """
    CheckForFile(path)
    path -> the sub folder to check for.
    - Checks if the file in path exists under self.path
    """
    def CheckForFile(self, path):
        Npath = self.__replace(path)
        if self._api:
            return self._api.checkIfExissts(self.path, Npath)[0]
        return os.path.exists(os.path.join(self.path, Npath))

    """
    Delete(path)
    path -> path to delete
    - Delets without questioning... in theory
    """
    def Delete(self, path=None):
        if path is None:
            path = self.path

        if not self._api:
            Npath = self.__replace(path)
            if os.path.exists(Npath):
                shutil.rmtree(Npath)
                return True
            print('Path not found! -> {}'.format(Npath))
            return False
        return self._api.DeleteData(path)


if __name__ == "__main__":
    ss = save({'name': 'NSTTest', 'path': 'Saves'})
    print(vars(ss))
    ss.makeFolder('1/2', True)
    print(vars(ss))
    path = ss.writeFile('Testinfo')
    print(path)
    data = ss.readFile()
    print(data)
    folderData = ss.ls()
    print(folderData)
    file = ss.CheckForFile("1/2/3")
    print(file)
    deleted = ss.Delete()
    print(deleted)
