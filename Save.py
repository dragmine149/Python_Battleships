import os
import Functions
import json
import platform
import shutil
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
    def __init__(self, path, Json=True, data={
        'name': None,
        'file': None
    }, Api=False):
        # removes hidden characters and replaces the "" if dragged in.
        self.path = path.rstrip().replace('', '')
        self.api = None
        self.ApiPath = None
        self.error = None
        if (self.path.find("/") == -1 and self.path.find("\\") == -1 and self.path != "Saves") or Api:  # noqa
            # Google drive api check
            # A lot of checks, here and in the script
            try:
                import DriveApi as d
                self.api = d.Api(self.path)
                if not self.api.TR:
                    Functions.clear(2, "Something failed in testing the google drive api. Correct permissions?")  # noqa
                    self.error = 'GD failed'
            except ModuleNotFoundError:
                Functions.clear(2, "Google drive api is not installed, Please follow the installation instructions or change path")  # noqa
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
    - Makes a folder with the string imported from before. In save.save().
      No extra imports required.
    - Returns the path to the folder. Either a dict (api) or string (local)
    """
    def makeFolder(self, sub=None):
        if self.error is not None:
            return self.error
        splitInfo = []
        if sub is not None:
            if platform.system() == "Windows":
                splitInfo = sub.split("\\")
            else:
                splitInfo = sub.split("/")

        if self.api:
            # Usess the google drive api and return the folder id.
            folderId = self.api.UploadData({
                'name': self.data['name'],
                'folder': self.path
            }, True)
            if sub is not None:
                newFolder = folderId['id']
                print(splitInfo)
                for item in splitInfo:
                    newFolder = self.api.UploadData({
                        'name': item,
                        'folder': newFolder
                    }, True)
                return newFolder
            return folderId
        else:
            # Makes a local folder
            path = os.path.join(self.path, self.data['name'])
            if not os.path.exists(path):
                os.mkdir(path)
            # make sure sub is None because could be same as parent folder
            elif sub is None:
                overwrite = None
                while overwrite is None:
                    overwrite = input("Are you sure you want to overwrite this game? (y = yes, n = no): ")  # noqa
                    if overwrite.lower()[0] == "n":
                        return False
                    elif overwrite.lower()[0] != "y":
                        overwrite = None
                        Functions.clear(2, "Please enter a valid option!")
            print(sub)
            if sub is not None:
                for item in splitInfo:
                    path = os.path.join(path, item)
                    if not os.path.exists(path):
                        os.mkdir(path)
            return path

    """
    writeFile({
        'data' -> Data to save
        'folder' -> Folder to save data to
    },
    name -> A name different from the game name
    )
    - Makes a file in a folder before deciding how to upload.
    - If api will send the file to the api and them remove after upload.
    - If local, Moves the file to the save location.
    """
    def writeFile(self, data={
        'data': None,
        'folder': None
    }, name=None, overwrite=False):
        if self.error is not None:
            return self.error
        if name:
            self.data['name'], self.name = name, self.data['name']
        # Check to make sure there actually IS data
        if data['data'] is None:
            return False

        # Makes the data in a file. (Both reasons)
        with open("Saves/.Temp/{}".format(self.data['name']), 'w+') as tempFile:  # noqa
            if self.json:
                tempFile.write(json.dumps(data['data']))
            else:
                tempFile.write(data['data'])

        # Upload the data to google. Returns the dict
        if self.api:
            id = self.api.UploadData({
                'name': self.data['name'],
                'path': 'Saves/.Temp/{}'.format(self.data['name']),
                'folder': data['folder']
            }, overwrite=overwrite)
            os.system('rm Saves/.Temp/{}'.format(self.data['name']))
            if name:
                self.data['name'] = name
            return id
        else:
            # Saves the data to a file. Returns the file path.
            command = "mv"
            if platform.system() == "Windows":
                command = "move"
            print('{} Saves/.Temp/{} {}/{}'.format(command,
                                                   self.data['name'],
                                                   data['folder'],
                                                   self.data['name']))
            os.system('{} Saves/.Temp/{} {}/{}'.format(command,
                                                       self.data['name'],
                                                       data['folder'],
                                                       self.data['name']))

            if name:
                self.data['name'] = name
            return "Saves/{}/{}".format(data['folder'], self.data['name'])

    """
    readFile({
        'name' -> The name of the file. Either name or id
    })
    - Attempts to read the file. If its on the server or not.
    - Location to save/read = self.data['name']/self.data['file']/data['name']
    - If file is not found returns False
    - If file found / made, Returns data of file.
    """
    def readFile(self, data={
        'name': None,
    }):
        if self.error is not None:
            return self.error

        # Save location -> Where to save the file
        self.saveLocation = ""
        if self.path is not None and self.path != '':
            self.saveLocation += self.path + "/"
        if self.data['name'] is not None and self.data['name'] != '':
            self.saveLocation += self.data['name'] + "/"
        if self.data['file'] is not None and self.data['file'] != '':
            self.saveLocation += self.data['file'] + "/"
        if data['name'] is not None and data['name'] != '':
            self.saveLocation += data['name']

        if self.api:
            self.saveLocation = "Saves/.Temp/{}".format(self.data['file'])
            Id = self.api.DownloadData({
               'Id': data['name'],
               'path': self.saveLocation
            })
            if Id is False:
                # If id is false, try and find file in directory instead
                files = self.api.ListFolder()
                for file in files:
                    if file['name'] == data['name']:
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
            if os.path.exists(self.saveLocation):
                with open(self.saveLocation, "r") as file:
                    if self.json:
                        return json.loads(file.read())
                    return file.read()
            print("Failed -> File to read from not found!" +
                  "\nPath: {}".format(self.saveLocation))
            return False

    """
    ListDirectory(api, dir)
        - api -> If false, will not do the api no matter what.
        - dir -> If true, will return only directories
    - Returns all the files in the directory
    - No check as self.path is required.
    """
    def ListDirectory(self, api=True, dir=False):
        if self.api is not None and api is True:
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
        if self.api:
            return self.api.checkIfExists(self.path, path)[0]
        elif os.path.exists(os.path.join(self.path, path)):
            return True
        return False

    """
    Delete(path)
    - Deletes the path without question
    """
    def Delete(self, path):
        if not self.api:
            if os.path.exists(path):
                shutil.rmtree(path)
                return True
            else:
                print('Path not found! -> {}'.format(path))
                return False
        else:
            return self.api.DeleteData(path)
