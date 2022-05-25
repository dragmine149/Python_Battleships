import os
import osFunc
import Functions
import json
import platform
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class save:
    """
    path -> path of the file.
    json -> encode in json?
    data -> {
        name -> name of the game
        file -> name of the subfile. Either user/ships or user
    }
    Api -> Api bypass. (skip the path check)

    self.error -> Value to check for. If this is not None return false.
    """

    def __replace__(self, path):
        if platform.system() != "Windows":
            # remove backslash from the path
            return path.replace("\\", "")

    def __init__(self, path, Json=True, data={
        'name': None,
        'file': None
    }, Api=False):
        # removes hidden characters and replaces the "" if dragged in.
        self.path = path.rstrip().replace('', '')
        # would set to None but windows be like... (why windows...)
        self.api = False
        self.ApiPath = None
        self.error = None
        if (self.path.find("/") == -1 and self.path.find("\\") == -1 and self.path != "Saves") or Api:  # noqa
            # Google drive api check
            # A lot of checks, here and in the script
            try:
                import DriveApi as d
                self.api = d.Api(self.path)
            # would use ModuleNotFoundError but py3.4 says use ImportError
            except ImportError:
                Functions.clear(2, "Google drive api is not installed, Please follow the installation instructions or change path")  # noqa
                print("DEBUG -> Drive api not installed")
                self.error = 'No GD'
        """
        Some files are encoded in json to make them not easly editable.
        Unfortuantly some files will break this program / file if they try to
        encode the data in json.

        A switch / toggle is what we need.
        """
        self.json = Json
        self._FolderCheck()
        if data['name'] is not None and data['file'] is not None:
            self.data = data
        else:
            self.error = "No Data"

        if False:
            try:
                self.writeFile("Hi")
                self.Delete()
            except PermissionError as e:
                os.sys.exit('Failed to write to directory!')  # make better instead of quiting. At least we catch it

    """
    _FolderCheck()
    - Checks if all primary / required folders are made. If not make them.
    """

    def _FolderCheck(self):
        if self.error is not None:
            return self.error
        if not os.path.exists("Saves"):
            os.mkdir("Saves")
        if not os.path.exists("Saves/.Temp"):
            os.mkdir("Saves/.Temp")

    """
    makeFolder(sub)
    -- sub -> Keeps looping until all the directories are fullfilled.
    -- replace (default: False) -> replace self.path with the new path.
    - Makes a folder with the string imported from before. In save.save().
      No extra imports required.
    - Returns the path to the folder. Either a dict (api) or string (local)
    """

    def makeFolder(self, sub=None, replace=False):
        if self.error is not None:
            return self.error

        if self.api:
            # Usess the google drive api and return the folder id.
            folderId = self.api.UploadData({
                'name': self.data['name'],
                'folder': self.path
            }, True)
            if sub is not None:
                splitInfo = sub.split("/")
                if platform.system() == "Windows":
                    splitInfo = sub.split("\\")

                newFolder = folderId['id']
                print(splitInfo)
                for item in splitInfo:
                    newFolder = self.api.UploadData({
                        'name': item,
                        'folder': newFolder
                    }, True)
                if replace:
                    self.path = newFolder
                return newFolder['id'], item
            if replace:
                self.path = folderId
            return folderId['id'], item
        else:
            # Makes a local folder
            path = self.path
            if self.data['name'] != '':  # If empty data, makes the path the path to not add other folders and stuff  # noqa E501
                path = os.path.join(self.path, self.data['name'])
            name = None  # set for later when making new game name
            Npath = self.__replace__(path)
            if not os.path.exists(Npath):
                os.mkdir(path)
            if sub is not None:
                osFunc.mkdir(path, os.path.realpath(__file__))
            if replace:
                self.path = path
            return path, name

    """
    writeFile({
        'data' -> Data to save
    },
    name -> A name different from the game name,
    overwrite -> Whever the overwrite the old file (USED FOR DRIVE)
    )
    - Makes a file in a folder before deciding how to upload.
    - If api will send the file to the api and them remove after upload.
    - If local, Moves the file to the save location.
    Returns: path where saved
    """

    def writeFile(self, data={
        'data': None,
    }, name=None, overwrite=False):
        if self.error is not None:
            return self.error
        if name:
            self.data['name'], self.name = name, self.data['name']
        # Check to make sure there actually IS data
        writeData = None
        if isinstance(data, dict):
            writeData = data['data']
            if writeData is None:
                return False
        else:
            writeData = data
            if data is None:
                return False

        # Makes the data in a file. (Both reasons)
        with open("Saves/.Temp/{}".format(self.data['name']), 'w+') as tempFile:  # noqa
            if self.json:
                tempFile.write(json.dumps(writeData))
            else:
                tempFile.write(writeData)

        # Upload the data to google. Returns the dict
        if self.api:
            id = self.api.UploadData({
                'name': self.data['name'],
                'path': 'Saves/.Temp/{}'.format(self.data['name']),
                'folder': self.path
            }, overwrite=overwrite)
            os.system('rm Saves/.Temp/{}'.format(self.data['name']))
            if name:
                self.data['name'] = name
            return id
        else:
            # Saves the data to a file. Returns the file path.
            command = "mv"
            slash = "/"
            if platform.system() == "Windows":
                command = "move"
                slash = "\\"

            runCommand = '{} Saves{}.Temp{}{} {}{}{}'.format(command,
                                                             slash,
                                                             slash,
                                                             self.data['name'],
                                                             self.path,
                                                             slash,
                                                             self.data['name'])
            print(runCommand)
            os.system(runCommand)

            if name:
                self.data['name'] = name
            return "{}{}{}".format(self.path,
                                   slash,
                                   self.data['name'])

    """
    readFile(
        'name' -> The name of the file. Either name or id
    )
    - Attempts to read the file. If its on the server or not.
    - Location to save/read = self.data['name']/self.data['file']/data['name']
    - If file is not found returns False
    - If file found / made, Returns data of file.
    """

    def readFile(self, name=None):
        if self.error is not None:
            return self.error

        slash = "/"
        if platform.system() == "Windows":
            slash = "\\"

        # Save location -> Where to save the file
        path = "{}{}{}".format(self.path,
                               slash,
                               self.data['name'])

        if self.api:
            self.saveLocation = "Saves/.Temp/{}".format(self.data['file'])
            Id = self.api.DownloadData({
               'Id': name,
               'path': self.saveLocation
            })
            if Id is False:
                # If id is false, try and find file in directory instead
                files = self.api.ListFolder()
                for file in files:
                    if file['name'] == name:
                        Id = self.api.DownloadData({
                            'Id': file['id'],
                            'path': self.saveLocation
                        })
                        break

            if isinstance(Id, str):
                print({'saveId', Id})
                with open(Id, 'r') as file:
                    if self.json:
                        return json.loads(file.read())
                    return file.read()
            return Id
        else:
            if platform.system() != "Windows":
                # remove backslash from the path
                path = path.replace("\\", "")

            # Checks before reading
            if os.path.exists(path):
                with open(path, "r") as file:
                    if self.json:
                        return json.loads(file.read())
                    return file.read()
            print("Failed -> File to read from not found!"
                  + "\nPath: {}".format(path))
            return False

    """
    ListDirectory(api, dir)
        - api -> If false, will not do the api no matter what.
        - dir -> If true, will return only directories
    - Returns all the files in the directory
    - No check as self.path is required.
    """

    def ListDirectory(self, api=True, dir=False):
        if self.api is not False and api is True:
            return self.api.ListFolder(dir=dir)
        else:
            if not dir:
                try:
                    return os.listdir(self.path)
                except NotADirectoryError:
                    return False
            else:
                DirInfo = os.listdir(self.path)
                newDirList = []
                for item in DirInfo:
                    if os.path.isdir(os.path.join(self.path, item)):
                        newDirList.append(item)
                return newDirList

    """
    CheckForFile(path)
    - Returns true if a file exists, returns false if not
    """

    def CheckForFile(self, path):
        Npath = self.__replace__(path)
        if self.api:
            return self.api.checkIfExists(self.path, Npath)[0]
        if os.path.exists(os.path.join(self.path, Npath)):
            return True
        return False

    """
    Delete(path=None)
    - Deletes the path without question
    """

    def Delete(self, path=None):
        # If no path specified, use self.path
        if path is None:
            path = self.path

        if not self.api:
            Npath = self.__replace__(path)
            if os.path.exists(Npath):
                os.remove(Npath)
                return True
            print('Path not found! -> {}'.format(path))
            return False
        return self.api.DeleteData(path)
