import os
import Functions
import shutil
import json
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
                    return False
            except ModuleNotFoundError:
                Functions.clear(2, "Google drive api is not installed, Please follow the installation instructions or change path")  # noqa
                return False
        """
        Some files are encoded in json to make them not easly editable.
        Unfortuantly some files will break this program / file if they try to
        encode the data in json.

        A switch / toggle is what we need.
        """
        self.Json = Json
        if data['name'] is not None and data['file'] is not None:
            self.data = data
        else:
            return False

    def makeFolder(self):
        if self.api:
            # Usess the google drive api and return the folder id.
            folderId = self.api.UploadData({
                'name': self.data['name']
            }, True)
            return folderId
        else:
            # Makes a local folder
            path = os.path.join(self.path, self.data['name'])
            if not os.path.exists():
                os.mkdir(path)
            return path
