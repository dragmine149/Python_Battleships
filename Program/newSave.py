import os
import Functions
import json
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
    Api -> Forces use of api over normal data
    """
    def __init__(self, data={'name': '',
                             'path': '',
                             'Json': False}, Api=False):
        # removes characters from the path
        self.path = data['path'].rstrip()
        self._api = self.__loadApi()
        self._Json = data['Json']
        self.__Foldercheck(self)
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
        if (self.path.find("/") == -1 and self.path.find("\\") == -1 and self.path != "Saves") or Api:  # noqa E501
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
    def _Json(self, data, save):
        if self._Json:
            if not save:
                return json.loads(data)
            return json.dumps(data)
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
        if self.api:
            # Makes folder on drive
            folderId = self.api.UploadData({
                'name': self.data['name'],
                'folder': self.path
            }, True)

            # Check for sub folder path
            if sub is not None:
                splitInfo = self.__split(sub)
                newFolder = folderId['id']

                # Makes sub folders on drive
                for item in splitInfo:
                    newFolder = self.api.UploadData({
                        'name': item,
                        'path': newFolder
                    }, True)['id']

                folderId = newFolder

            # replace and return
            if replace:
                self.path = folderId
            return folderId

        # normal local folder
        path = self.path
        if self.data['name'] != '':
            path = os.path.join(self.path, self.data['name'])

        # this is because os.path.exists doesn't like it but os.mkdir AAAAAAA
        Npath = self.__replace(path)
        if not os.path.exists(Npath):
            os.mkdir(path)

        if sub is not None:
            os.makedirs(sub)

        if replace:
            self.path = path
        return path, None

    def writeFile(self, data, overwrite=False):
        if data is None:
            return None

        tempLocation = "Saves/.Temp/{}".format(self.data['name'])
        with open(tempLocation, 'w+') as tempFile:
            tempFile.write(self._Json(data, True))

        if self.api:
            id = self.api.UploadData({
                'name': self.data['name'],
                'path': tempLocation,
                'folder': self.path,
            }, overwrite=overwrite)
            os.remove(tempLocation)
            return id
        slash = self.__slash()
