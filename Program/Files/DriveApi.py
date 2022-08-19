# Google drive api inputs (a lot)
from __future__ import print_function
from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from apiclient.http import MediaFileUpload, MediaIoBaseDownload  # type: ignore


import os
import sys
import io
import importlib
import copy
setup = importlib.import_module('Files.DriveSetup')
Functions = importlib.import_module('Files.Functions')
os.chdir(os.path.dirname(os.path.realpath(__file__)))

SCOPES = ['https://www.googleapis.com/auth/drive']


class Api:
    def __slash(self):
        # Determinds how to split paths
        return "\\" if os.name == "nt" else "/"
    
    def __init__(self, folderId):
        self.msg = "Google Drive"  # message to show when on load screen,
        self.folder = folderId
        self.service = self.__LoadAPI__()
        self.pageSize = -1  # Change to variable setting later.

    # Loads the api for use later.
    # Complicated function taken from google.
    def __LoadAPI__(self):
        """Load the API.

        Returns:
            Service: The api.
        """
        setup.Setup(self.folder).main()
        try:
            creds = None
            if os.path.exists('ApiFiles/token.json'):  # noqa
                creds = Credentials.from_authorized_user_file('ApiFiles/token.json', SCOPES)  # noqa
            # If there are no (valid) credentials available, let the user login
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'ApiFiles/credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('ApiFiles/token.json', 'w') as token:  # noqa
                    token.write(creds.to_json())

            return build('drive', 'v3', credentials=creds)
        except KeyboardInterrupt:
            sys.exit('Bad drive... Please restart the program and try again.')
        except:  # noqa  Try and find error handle 'RefreshError'
            if os.path.exists('ApiFiles/token.json'):
                os.system('rm ApiFiles/token.json')

                # Check if files are actually there and not missing due to folder creation.  # noqa
                if not os.path.exists('ApiFiles/credentials.json'):
                    os.sys.exit('ApiFiles/credentials.json has not been found! Please follow the google drive api setup instructions or contact the owner.')  # noqa
            return self.__LoadAPI__()
    
    def ListDirectory(self):
        # Get everything except trashed items
        query = "'{}' in parents and trashed=false".format(self.folder)
        
        result = self.service.find().list(
            q=query,
            pageSize=self.pageSize,
            fields="nextPageToken, files(id, name)"
        ).execute()
        items = result.get("files", [])
        
        return items
    
    def __GetNameFromList(self, list):
        names = []
        for item in list:
            if isinstance(item, dict):
                names.append(item['name'])
            else:
                names.append(item)
        
        return names

    def __FindItemInList(self, list, name):
        for item in list:
            if item['name'] == name:
                return item
    
    def __checkIfExists(self, folder, name):
        # folder -> folder to check for file in
        # name -> name of the file to compare
        print({'folder': folder})
        items = self.ListDirectory()
        if items is not None:
            print(items)
            for item in items:
                print(item)
                if item['name'] == name:
                    return True, item
        return False, None
    
    def MakeDirectory(self, name):
        directories = name.split(self.__slash())
        currentPath = self.folder
        for item in directories:
            exists, id = self.__checkIfExists(currentPath, item)            
            if exists:
                self.Delete(id)
            
            metadata = {
                    'name': name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [currentPath]
                }
            currentPath = self.service.files().create(body=metadata,
                                                   fields='id').execute()
        return currentPath

    def GetPath(self):
        return self.folder

    def ChangeDirectory(self, dir):
        self.folder = dir
    
    def UploadFile(self, path):
        pathInfo = path.split(self.__slash())
        name = pathInfo[len(pathInfo) - 1]
        
        exists, id = self.__checkIfExists(self.folder, name)
        if exists:
            self.Delete(id)
        
        metadata = {
                    'name': name,
                    'mimeType': '*/*',  # not readable on drive
                    'parents': [self.folder]
                }
        print(metadata)
        media = MediaFileUpload(path,
                                mimetype='*/*',
                                resumable=True)

        id = self.service.files().create(body=metadata,
                                         media_body=media,
                                         fields='id').execute()
        return id

    def DownloadFile(self, path):
        pathInfo = path.split(self.__slash())
        name = pathInfo[len(pathInfo) - 1]
        
        attempts = 5
        currentAttempt = 0
        
        while currentAttempt < attempts:
            exists, id = self.__checkIfExists(self.folder, name)
            if exists:
                request = self.service.files().get_media(fileId=id)
                fileHandler = io.BytesIO()
                downloader = MediaIoBaseDownload(fileHandler, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Downloaded {}%".format(int(status.progress()) * 100),
                            end='\r')
                html = fileHandler.getvalue()

                # save
                with open(path, 'wb+') as f:
                    f.write(html)

                Functions.clear()
                return path

            print("File not found on server! Retrying in 5 seconds")
            Functions.clear(
                5, "File not found on server! Retrying in 5 seconds", "red")
            currentAttempt += 1
        
        Functions.Print("Failed to find file on server, max attempts reached!", "red", "bold")
        return 
    
    def Delete(self, id):
        try:
            self.service.files().delete(fileId=id).execute()
            return "Deleted"
        except HttpError:
            return "Not found"