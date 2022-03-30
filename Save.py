import os
import Functions
import shutil
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
    """
    def __init__(self, path, Json=True, data={
        'name': None,
        'file': None
    }, Api=False):
        # removes hidden characters and replaces the "" if dragged in.
        self.path = path.rstrip().replace('', '')
        self.api = None
        if (self.path.find("/") == -1 and self.path.find("\\") == -1 and self.path != "Saves") or Api:  # noqa
            # Google drive api check
            # A lot of checks, here and in the script
            try:
                import DriveApi as d
                self.api = d.Api(self.path)
                if not self.api.TR:
                    Functions.clear(2, "Something failed in testing the google drive api. Correct permissions?")  # noqa
                    return 'GD failed'
            except ModuleNotFoundError:
                Functions.clear(2, "Google drive api is not installed, Please follow the installation instructions or change path")  # noqa
                return 'No GD'
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
            return False
    
    """
    _FolderCheck()
    - Checks if all primary / required folders are made. If not make them.
    """
    def _FolderCheck(self):
        if not os.path.exists("Saves"):
            os.mkdir("Saves")
        if not os.path.exists("Saves/Temp"):
            os.mkdir("Saves/Temp")

    """
    makeFolder(sub)
    -- sub -> Keeps looping until all the directories are fullfilled. 
    - Makes a folder with the string imported from before. In save.save(). No extra imports required.
    - Returns the path to the folder. Either a dict (api) or string (local)
    """
    def makeFolder(self, sub=None):
        splitInfo = []
        if sub:
            if platform.system() == "Windows":
                splitInfo = sub.split("\\")
            else:
                splitInfo = sub.split("/")
        if self.api:
            # Usess the google drive api and return the folder id.
            folderId = self.api.UploadData({
                'name': self.data['name']
            }, True)
            if sub:
                newFolder = None
                for item in splitInfo:
                    newFolder = self.api.UploadData({
                        'name': item
                    }, True)
                return newFolder
            return folderId
        else:
            # Makes a local folder
            path = os.path.join(self.path, self.data['name'])
            if not os.path.exists(path):
                os.mkdir(path)
            if sub:
                for item in splitInfo:
                    os.path.join(path, item)
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
    }, name=None):
        if name:
            self.data['name'], self.name = name, self.data['name']
        # Check to make sure there actually IS data
        if data['data'] is None:
            return False
        
        # Makes the data in a file. (Both reasons)
        with open("Saves/Temp/{}".format(self.data['name']), 'w+') as tempFile:
            if self.json:
                tempFile.write(json.dumps(data['data']))
            else:
                tempFile.write(data['data'])

        # Upload the data to google. Returns the dict
        if self.api:
            id = self.api.UploadData({
                'name': self.data['name'],
                'path': 'Saves/Temp/{}'.format(self.data['name']),
                'folder': data['folder']
            })
            os.system('rm Saves/Test/{}'.format(self.data['name']))
            if name:
                self.data['name'] = name
            return id
        else:
            # Saves the data to a file. Returns the file path.
            command = "mv"
            if platform.system() == "Windows":
                command = "move"
            os.system('{} Saves/Temp/{} {}/{}'.format(command, self.data['name'], data['folder'], self.data['name']))

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
        saveLocation = "{}/{}/{}".format(self.data['name'],
                                         self.data['file'],
                                         data['name'])
        if self.api:
            Id = self.api.DownloadData({
               'name': data['name'],
               'path': saveLocation
            })
            with open(Id, 'r') as file:
                if self.json:
                    return json.loads(file.read())
                return file.read()
        else:
            if os.path.exists(saveLocation):
                with open(saveLocation, "r") as file:
                    if self.json:
                        return json.loads(file.read())
                    return file.read()
            else:
                print("Failed -> File to read from not found!\nPath: {}".format(saveLocation))
                return False

    """
    ListDirectory()
    - Returns all the files in the directory
    """
    def ListDirectory(self):
        if self.api:
            return self.api.ListFolder()
        else:
            return os.listdir(self.path)