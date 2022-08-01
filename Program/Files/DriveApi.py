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
setup = importlib.import_module('Files.DriveSetup')
Functions = importlib.import_module('Files.Functions')
os.chdir(os.path.dirname(os.path.realpath(__file__)))

SCOPES = ['https://www.googleapis.com/auth/drive']


class Api:
    # Setup the api class
    def __init__(self, folderId):
        self.folder = folderId
        self.service = self.__LoadAPI__()
        self.pageSize = 10  # Change to variable setting later.

    # Loads the api for use later.
    # Complicated function taken from google.
    def __LoadAPI__(self):
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

    def DeleteData(self, id):
        try:
            self.service.files().delete(fileId=id).execute()
            return "Deleted"
        except HttpError:
            return "Not found"

    # Checks if the folder / file exists before making a duplicate
    def checkIfExists(self, folder, name):
        # folder -> folder to check for file in
        # name -> name of the file to compare
        print({'folder': folder})
        items = self.ListFolder(folder)
        if items is not None:
            print(items)
            for item in items:
                print(item)
                if item['name'] == name:
                    return True, item
        return False, None

    # Makes folder / uploads data based on input
    def UploadData(self, data={'name': 'error', 'path': 'UploadFileTest.txt', 'folder': None}, folder=False, overwrite=False, game=False, gamePop=False):  # noqa

        # Splits the name and path information to get the sub
        # folder and name of the file
        try:
            savedPath = data['path']
        except KeyError:
            pass
        if game:
            data['path'] = data['path'].replace('-', '/')
            splitName = os.path.split(data['name'])
            data['folder'] = self.GetFileFromParentId(splitName[0], gamePop)
            data['name'] = splitName[1]

        print("Uploading... {}\tFolder:{}".format(data, folder))
        metadata = {}
        media = None

        localFolder = self.folder
        try:
            if data['folder']:
                localFolder = data['folder']
        except KeyError:
            # No need to do anything if error.
            pass

        if isinstance(localFolder, dict):
            localFolder = localFolder['id']

        # check if already exists, we don't want to make duplicates
        exists, Id = self.checkIfExists(localFolder, data['name'])

        # Deletes if we overwrite the data.
        if overwrite and exists:
            print(self.DeleteData(Id['id']))

        if (not exists and Id is None) or overwrite:
            if folder:  # folder metadata
                metadata = {
                    'name': data['name'],
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [localFolder]
                }
            else:
                # file metadata
                metadata = {
                    'name': data['name'],
                    'mimeType': '*/*',  # not readable on drive
                    'parents': [localFolder]
                }
                print(metadata)
                media = MediaFileUpload(savedPath,
                                        mimetype='*/*',
                                        resumable=True)
            if media:
                return self.service.files().create(body=metadata,
                                                   media_body=media,
                                                   fields='id').execute()
            else:
                return self.service.files().create(body=metadata,
                                                   fields='id').execute()
        else:
            return Id

    # Attempts to find the file in the id if the id is: 'PATH/NAME'
    def GetFileFromParentId(self, id, game=False):
        # Split up the path into each dir
        pathSplit = id.split('/')
        if game:
            pathSplit.pop(0)
        if len(pathSplit) == 1:
            # return original if only id with nothing else
            files = self.ListFolder(self.folder)
            try:
                for file in files:
                    if file['name'] == pathSplit[0]:
                        return file['id']
            except ValueError:
                pass
            return id

        parentFolder = pathSplit[0]
        for i in range(len(pathSplit)):
            files = self.ListFolder(parentFolder)
            for file in files:
                if file['name'] == pathSplit[i]:
                    if i + 1 == len(pathSplit):
                        return file['id']
                    parentFolder = file['id']
                    break
        return id  # none found, return original

    # Download data from fileid. (Change to file name?)
    def DownloadData(self, data={'Id': 'error', 'path': 'Saves'}, End=False):
        originalData = data # just in case of recheckt
        # debug
        print('Original: ' + data['Id'])
        data['Id'] = self.GetFileFromParentId(data['Id'])
        print('New: {}'.format(data['Id']))

        try:
            # Check if exists to avoid breaks
            fileName = data["path"].split("/")
            exists, _ = self.checkIfExists(data['Id'], fileName[len(fileName) - 1])
            
            if not exists:
                # attempts to redownload if not found
                print("File not found on server! Retrying in 5 seconds")
                Functions.clear(
                    5, "File not found on server! Retrying in 5 seconds", "red")
                return self.DownloadData(originalData, End)
            
            # Gets the file data from drive
            request = self.service.files().get_media(fileId=data['Id'])
            fileHandler = io.BytesIO()
            downloader = MediaIoBaseDownload(fileHandler, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Downloaded {}%".format(int(status.progress()) * 100),
                      end='\r')
            html = fileHandler.getvalue()

            # If the file should be presented as 'FILE.txt'
            fileEnd = ".txt" if End else ""

            # Sorts out the path incase '/' got included again.
            sPath = data['path'].split('/')
            start = 'Saves/.Temp'
            end = ''
            for i in range(len(sPath) - 2):
                end += sPath[i + 2]
                if i + 2 == len(sPath) - 2:
                    end += '-'
            data['path'] = os.path.join(start, end)

            # save
            with open("{}{}".format(data['path'], fileEnd), 'wb+') as f:
                f.write(html)

            Functions.clear()
            return "{}{}".format(data['path'], fileEnd)
        except HttpError as error:
            # If this fires and then the above fires, do not worry.
            print("Error occured!: {}".format(error.reason))
            return False

    def ListFolder(self, folder=None, dir=False):
        if folder is None:
            folder = self.folder

        if isinstance(folder, dict):
            folder = folder['id']
        try:
            query = "'{}' in parents and trashed=false".format(folder)
            if dir:  # return only directories
                query += " and mimeType = 'application/vnd.google-apps.folder'"

            # Some things don't work...
            results = self.service.files().list(
                q=query,
                pageSize=self.pageSize, fields="nextPageToken, files(id, name)").execute()  # noqa
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return []
            return items
        except HttpError:

            # Attempts to take the folder as a name and find files in folder
            # SO, if folder != drive ID, find folder, return files in folder
            try:
                files = self.ListFolder(dir=dir)
                for file in files:
                    if file['name'] == folder:
                        return self.ListFolder(file['id'], dir=dir)
            except HttpError as error:
                print('An error occurred: {}'.format(error))
                return "Error"
