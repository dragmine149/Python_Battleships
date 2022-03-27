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
            os.system('rm ApiFiles/token.json')
            self.__LoadAPI__()

    # Runs a series of tests to make sure the client has all correct permission
    def Test(self):
        # Makes test folder
        def makeFolder(folderId):
            folder_metadata = {
                'name': 'Battleships_test',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [folderId]
            }
            return self.service.files().create(body=folder_metadata,
                                               fields='id').execute()

        # Makes test file
        def uploadFile(folderMadeId):
            file_metadata = {
                'name': 'README.txt',
                'mimeType': 'text/plain',
                'parents': [folderMadeId.get('id')]
            }
            media = MediaFileUpload('UploadFileTest.txt',
                                    mimetype='text/plain',
                                    resumable=True)
            return self.service.files().create(body=file_metadata,
                                               media_body=media,
                                               fields='id').execute()

        # Download test file
        def downloadFile(file):
            request = self.service.files().get_media(fileId=file)
            fileHandler = io.BytesIO()
            downloader = MediaIoBaseDownload(fileHandler, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Downloaded {}%".format(int(status.progress()) * 100))
            html = fileHandler.getvalue()

            with open("DownloadFileTest.txt", 'wb') as f:
                f.write(html)
            return True

        # Delete local files (that got downloaded)
        def DelLocal():
            if os.path.exists("DownloadFileTest.txt"):
                os.remove("DownloadFileTest.txt")
                return True
            else:
                return False

        # Delete server files (test)
        def DelServer(file, folder):
            self.service.files().delete(fileId=file).execute()
            self.service.files().delete(fileId=folder).execute()

        # Runs tests.
        # TODO: Add checks for fails
        # TODO: Replace some checks with the actual function
        folder = makeFolder(self.folder)
        print(folder)
        file = uploadFile(folder)
        print(file)
        downloadFile(file['id'])
        time.sleep(5)  # updates
        DelLocal()
        DelServer(file['id'], folder['id'])
        return True

    def DeleteData(self, id):
        self.service.files().delete(fileId=id).execute()

    # Makes folder / uploads data based on input
    def UploadData(self, data={'name': 'error', 'path': 'UploadFileTest.txt', 'folder': None}, folder=False):  # noqa
        print("Uploading... {}\nFolder:{}".format(data, folder))
        metadata = {}
        media = None
        try:
            if data['folder']:
                self.folder = data['folder']
        except KeyError:
            self.folder = self.folder
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
            media = MediaFileUpload(os.path.join(os.path.dirname(os.path.realpath(__file__)), data['path']),  # noqa
                                    mimetype='*/*',
                                    resumable=True)
        if media:
            return self.service.files().create(body=metadata,
                                               media_body=media,
                                               fields='id').execute()
        else:
            return self.service.files().create(body=metadata,
                                               fields='id').execute()

    # Download data from fileid. (Change to file name?)
    def DownloadData(self, data={'name': 'error', 'path': 'Saves'}):
        try:
            request = self.service.files().get_media(fileId=data['name'])
            fileHandler = io.BytesIO()
            downloader = MediaIoBaseDownload(fileHandler, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Downloaded {}%".format(int(status.progress()) * 100))
            html = fileHandler.getvalue()

            with open("{}.txt".format(data['path']), 'wb') as f:
                f.write(html)
            return True
        except HttpError as error:
            print("Error occured!: {}".format(error.reason))
            return False

    def ListFolder(self):
        try:
            # Some things don't work...
            results = self.service.files().list(
                q="'{}' in parents".format(self.folder),
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            return items
        except HttpError as error:
            print(f'An error occurred: {error}')
            return "Error"


if __name__ == "__main__":
    api = Api(input("Folder id: "))
    print(api.ListFolder())
    # result = api.UploadData({'name': 'FolderTest', 'path': '', 'folder': None}, True)  # noqa
    # print(result)
    # file = api.UploadData({'name': 'FileTest', 'path': 'UploadFileTest.txt', 'folder': result['id']}, False)  # noqa
    # print(file)
    # api.DownloadData({'name': file['id'], 'path': 'Download'})
