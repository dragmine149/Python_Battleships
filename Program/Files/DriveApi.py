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
    def __LoadAPI__(self):
        Functions.clear()
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
        # folder -> folder to upload file to.
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
    def UploadData(self, data={'name': 'error', 'path': 'UploadFileTest.txt', 'folder': None}, folder=False, overwrite=False):  # noqa
        print("Uploading... {}\tFolder:{}".format(data, folder))
        metadata = {}
        media = None
        try:
            if data['folder']:
                self.folder = data['folder']
        except KeyError:
            # No need to do anything if error.
            pass

        if isinstance(self.folder, dict):
            self.folder = self.folder['id']

        exists, Id = self.checkIfExists(self.folder, data['name'])

        # Deletes if we overwrite the data.
        if overwrite and exists:
            print(self.DeleteData(Id['id']))

        if (not exists and Id is None) or overwrite:
            if folder:  # makes folder
                metadata = {
                    'name': data['name'],
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [self.folder]
                }
            else:
                metadata = {
                    'name': data['name'],
                    'mimeType': '*/*',  # not readable on drive
                    'parents': [self.folder]
                }
                print(metadata)
                media = MediaFileUpload(data['path'],  # noqa
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
    def GetFileFromParentId(self, id):
        # Split up the path into each dir
        pathSplit = id.split('/')
        if len(pathSplit) <= 1:
            # return original if only id with nothing else
            return id

        # Get files under the parent folder
        parentFolder = pathSplit[0]
        files = self.ListFolder(parentFolder)
        for file in files:
            if file['name'] == pathSplit[1]:
                parentFolder = file['id']
                files = self.ListFolder(parentFolder)
                break

        # Loop through the files in that folder to find the file
        # searching for at the beginning.
        print(files)
        for file in files:
            if file['name'] == pathSplit[2]:
                return file['id']

        return id  # if none found, return original

    # Download data from fileid. (Change to file name?)
    def DownloadData(self, data={'Id': 'error', 'path': 'Saves'}, End=False):
        print('Original: ' + data['Id'])
        data['Id'] = self.GetFileFromParentId(data['Id'])
        print('New: {}'.format(data['Id']))
        try:
            request = self.service.files().get_media(fileId=data['Id'])
            fileHandler = io.BytesIO()
            downloader = MediaIoBaseDownload(fileHandler, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Downloaded {}%".format(int(status.progress()) * 100),
                      end='\r')
            html = fileHandler.getvalue()

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
            if dir:
                query += " and mimeType = 'application/vnd.google-apps.folder'"

            # Some things don't work...
            results = self.service.files().list(
                q=query,
                pageSize=self.pageSize, fields="nextPageToken, files(id, name)").execute()  # noqa
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            return items
        except HttpError as error:
            print('An error occurred: {}'.format(error))
            return "Error"
