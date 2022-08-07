import importlib
import os
import shutil
import pickle
import sys
Functions = importlib.import_module('Files.Functions')
Settings = importlib.import_module('Files.Settings')
FTP = importlib.import_module('Files.FTP')
# Stores whever program is stored.
filePath = os.path.dirname(os.path.realpath(__file__))
os.chdir(filePath)


class save:
    """
    data -> {
        name -> name of the file to create (supports subdirs)
        path -> where to save the file
    }
    """
    def __init__(self, data={'name': '-',
                             'path': ''}):
        # removes characters from the path
        self.path = data['path'].rstrip()
        self._api = self.__loadSystem()
        self.__Foldercheck()

        try:
            if data['name'] is None:
                data['name'] = ''
        except KeyError:
            data['name'] = ''

        if data['name'] is not None and data['path'] is not None:
            self.data = data
    
    def __loadSystem(self):
        """Loads the file system to use

        Returns:
            Class: Class of the system to use.
        """
        if self.path == "Saves" or self.path == "Data":
            return
        
        if self.path.find(':/') != -1:
            return self.__loadFTP()
        
        if self.path.find("/") == -1 and self.path.find("\\") == -1:
            return self.__loadApi()
    
    def __loadFTP(self):
        # path is stored as IP::/PATH
        pathData = self.path.split(":/")
        
        userInfo = Settings.request(['FTPname', 'FTPpass'])
        ftp = FTP.FileTransferProtocole(pathData[0],
                                        userInfo[0],
                                        userInfo[1],
                                        pathData[1])
        ftp.login()
        return ftp
        

    """
    __loadApi()
    - Attempts to load the google drive api.
    - If api not found, will ask user to either install (WIP) or change path
    """
    def __loadApi(self):
        # Attempts to load Api
        # Import drive and do stuff
        try:
            d = importlib.import_module('Files.DriveApi')
            return d.Api(self.path)
        except ImportError:
            Functions.clear()
            Functions.warn(2, "Google drive api not installed!")
            # Asks the user if they want to change location
            # change = input("Please enter the new path (type 'install' to install googledrive api): ")  # noqa E501
            # if change.lower() == 'install':
            #     sys.exit(self.__installDrive())
            # self.path = change.rstrip()
            # return self.__loadApi()

    """
    __Foldercheck()
    - Checks if core folders are made, else make them
    """
    def __Foldercheck(self):
        # Data for files
        try:
            if not os.path.exists("Saves"):
                os.mkdir("Saves")
        except FileExistsError:
            print("Saves already exists yet doesn't exists...")

        try:
            if not os.path.exists("Saves/.Temp"):
                os.mkdir("Saves/.Temp")
        except FileExistsError:
            print("Saves/.Temp already exists yet doesn't exists...")

        try:
            # Settings and other data
            if not os.path.exists("Data"):
                os.mkdir("Data")
        except FileExistsError:
            print("Data already exists yet doesn't exists...")

    """
    _Encode(data, save)
    data -> data to binarify
    save -> to encode or to decode
    - Encodes data with binary, this makes it harder to edit normally
    """
    def _Encode(self, data, save=False):
        try:

            if not save:  # loading
                return pickle.loads(data)  # decode binary first
            return pickle.dumps(data)

        except Exception:
            Functions.clear()
            Functions.warn(3, "Please check the data stored! If this keeps happening please reset your data with 'python mainTemp.py +-delete'.")  # noqa E501
            print('Logs: ')
            Functions.PrintTraceback()
            sys.exit('Error in reading data')

    """
    __replace(path)
    path -> string to replace data
    - If not windows os, replace \\ with nothing
    """
    def __replace(self, path):
        return path.replace('\\', '') if os.name != "nt" else path

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
        return "\\" if os.name == "nt" else "/"

    def makeFolder(self):
        """Make a directory
        
        Returns:
            string: The path / id of the directory.
        """
        if self._api:
            return self._api.MakeDirectory(self.data['name'])

        # normal local folder
        path = self.path
        if self.data['name'] != '':
            path = os.path.join(self.path, self.data['name'])

            os.makedirs(path)
            return path

    """
    writeFile(data, overwrite=False)
    data -> data to save
    overwrite -> whever to overwrite the data on drive. Dones't work locally.
    name -> name of the file, just in case the file needs to be different from the current name inputted.
    - Save data to a file
    """  # noqa E501
    def writeFile(self, data, overwrite=False, name="", game=False, gamePop=False):
        if data is None:
            return None
        if name == "":
            name = self.data['name']

        # Makes the file with the data in the temparay location
        tempLocation = "Saves/.Temp/{}".format(name.replace('/', '-'))
        with open(tempLocation, 'wb+') as tempFile:
            tempFile.write(self._Encode(data, True))
            
        if self._api:
            result = self._api.UploadFile(tempLocation)
            os.remove(tempLocation)
            return result

        slash = self.__slash()
        # moves file to where it should be saved
        shutil.move(tempLocation,
                    "{}{}{}".format(self.__replace(self.path), slash, name))  # noqa E501
        return "{}{}{}".format(self.path, slash, name)

    """
    readFile
    - returns the data from a file.
    - If not found, returns False
    """
    def readFile(self, name="", nameAllowed=True, joint=False):
        # Multi use case
        if name == "" and nameAllowed:
            name = self.data['name']
        if name != "" and joint:
            name = os.path.join(self.data['name'], name)

        path = os.path.join(self.path, name) if name != "" else self.path
        if self._api:
            nameInfo = name.split("/")
            saveLoc = "Saves/.Temp/{}".format(nameInfo[len(nameInfo) -1])
            
            directory = ""
            for item in nameInfo[:len(nameInfo) - 1]:
                directory += item + "/"
            
            self._api.ChangeDirectory(directory)
            try:
                Id = self._api.DownloadFile(saveLoc)
            except:
                Functions.Print("Failed to find file on server")
                return ""
            # If can't find file, attempt to search

            with open(Id, 'rb') as file:
                fileData = self._Encode(file.read())

            return fileData

        # local read area
        # Don't need to add name here as done eariler
        path = self.__replace(path)
        if os.path.exists(path):
            with open(path, 'rb') as file:
                return self._Encode(file.read())
        Functions.Print("Failed to find data in path: {}".format(path), "red")
        return False

    def ChangeDirectory(self, dir):
        """Changes the directory stored.
        """
        self.data['name'] = dir
        if self._api:
            self._api.ChangeDirectory(dir)
    
    def GetPath(self):
        """Gets the current path

        Returns:
            String: The path.
        """        
        if self._api:
            return self._api.GetPath()
        return self.path

    """
    ls(dir)
    - Joint -> Joins self.path and self.name together
    """
    def ls(self, Joint=False):

        # Joins path and name together
        path = self.path
        if Joint:
            path = os.path.join(self.path, self.data['name'])

        # use api if alvalible.
        if self._api:
            return self._api.ListDirectory()

        # Local area
        if os.path.exists(path):
            dirData = os.listdir(path)
            return dirData
        return None  # if directory not found

    """
    CheckForFile(path)
    path -> the sub folder to check for.
    - Checks if the file in path exists under self.path
    """
    def CheckForFile(self, path):
        Npath = self.__replace(path)
        if self._api:
            path = self.path
            self._api.ChangeDirectory(self.data['name'])
            # Checks in self.data['name'] folder instead of self.path
            if self.data['name'] != '':
                files = self.ls()
                for file in files:
                    
                    if isinstance(file, dict):
                        if file['name'] == self.data['name']:
                            return True

                    if file == self.data['name']:
                        return True
            
            return False
        return os.path.exists(os.path.join(self.path,
                                           self.data['name'],
                                           Npath))

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
            save.delete(Npath)
        return self._api.Delete(path)

    """
    delete(path)
    - Static method, Deletes without questions
    """
    @staticmethod
    def delete(path):
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
                return True
            os.remove(path)
            return True
        print('Path not found! -> {}'.format(path))
        return False


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