# Google drive api inputs (a lot)
from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient.http import MediaFileUpload, MediaIoBaseDownload


import os
import io
import time
os.chdir(os.path.dirname(os.path.realpath(__file__)))

SCOPES = ['https://www.googleapis.com/auth/drive']


class Api:
    # Setup the api class
    def __init__(self, folderId):
        if not os.path.exists("ApiFiles"):
            os.mkdir("ApiFiles")
        self.service = self.__LoadAPI__()
        self.folder = folderId
        self.TR = True  # In case it doesn't get set somehows...
        self.pageSize = 10  # Change to variable setting later.
        # self.Test()  # change to not testing every time.

    # Loads the api for use later.
    def __LoadAPI__(self):
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
        except:  # noqa  Try and find error handle 'RefreshError'
            if os.path.exists('ApiFiles/token.json'):
                os.system('rm ApiFiles/token.json')

                # Check if files are actually there and not missing due to folder creation.  # noqa
                if not os.path.exists('ApiFiles/credentials.json'):
                    os.sys.exit('ApiFiles/credentials.json has not been found! Please follow the google drive api setup instructions or contact the owner.')  # noqa
            return self.__LoadAPI__()

    # Runs a series of tests to make sure the client has all correct permission
    def Test(self):
        read, write1, write2 = None, None, None
        # Runs tests.
        # TODO: Add checks for fails
        # TODO: Replace some checks with the actual function
        folder = self.UploadData({
            'name': 'DriveApiTest',
            'folder': self.folder
        }, True)
        print(folder)
        if folder:
            write1 = True
            file = self.UploadData({
                'name': 'README (dont)',
                'path': 'UploadFileTest.txt',
                'folder': folder
            })
            print(file)
            if file:
                write2 = True
                success = self.DownloadData({
                    'Id': file['id'],
                    'path': 'DownloadFileTest'
                }, True)
                if success:
                    read = True
                else:
                    read = False
            else:
                write2 = False
        else:
            write1 = False
        time.sleep(5)  # updates
        if os.path.exists("DownloadFileTest.txt"):
            os.remove("DownloadFileTest.txt")

        if write2:
            self.DeleteData(file['id'])

        if write1:
            self.DeleteData(folder['id'])

        if write1 and write2 and read:
            print("Everything is ready!")
            self.TR = True
            return
        elif write1 and write2 and not read:
            print("Can write but not read!")
            self.TR = False
            return
        elif write1 and not write2 and not read:
            print("Can make folder, not upload file!")
            self.TR = False
            return
        elif not write1 and not write2 and not read:
            print("Failed to read or write")
            self.TR = False
            return
        else:
            self.TR = False
            print("Something failed...")
            print("Results: {}".format({'write1': write1,
                                        'write2': write2,
                                        'read': read}))
            return

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

    # Download data from fileid. (Change to file name?)
    def DownloadData(self, data={'Id': 'error', 'path': 'Saves'}, End=False):
        try:
            request = self.service.files().get_media(fileId=data['Id'])
            fileHandler = io.BytesIO()
            downloader = MediaIoBaseDownload(fileHandler, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Downloaded {}%".format(int(status.progress()) * 100))
            html = fileHandler.getvalue()

            fileEnd = ".txt"
            if not End:
                fileEnd = ""

            with open("{}{}".format(data['path'], fileEnd), 'wb+') as f:
                f.write(html)
            return "{}{}".format(data['path'], fileEnd)
        except HttpError as error:
            print("Error occured!: {}".format(error.reason))
            return False

    def ListFolder(self, folder=None, dir=False):
        if folder is None:
            folder = self.folder
        if isinstance(folder, dict):
            folder = folder['id']
        try:
            query = "'{}' in parents".format(folder)
            if dir:
                query += " and mimeType = 'application/vnd.google-apps.folder'"

            # print(query)
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


if __name__ == '__main__':
    api = Api('1jgyfEG0R76adWlnyzqDU030ps-mk4M20')
    # print(api.ListFolder(dir=False))
    # print(api.ListFolder(dir=True))
