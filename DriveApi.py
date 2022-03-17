from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

SCOPES = ['https://www.googleapis.com/auth/drive']


class Api:
    def __init__(self, folder_Id, move_Folder_Id, path):
        self.service = self.__LoadAPI__()
        self.folder_id = folder_Id
        self.moveFolder_Id = move_Folder_Id
        self.Path = path
        self.FolderPath = os.path.dirname(__file__)

    def __LoadAPI__(self):
        creds = None
        if os.path.exists('{}/token.json'.format(self.FolderPath)):  # noqa
            creds = Credentials.from_authorized_user_file('{}/token.json'.format(self.FolderPath), SCOPES)  # noqa
        # If there are no (valid) credentials available, let the user login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '{}/credentials.json'.format(self.FolderPath), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('{}/token.json'.format(self.FolderPath), 'w') as token:  # noqa
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)

            # Call the Drive v3 API
            results = service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    def GetFilesForDownload(self):
        self.Files = []
        page_token = None

        while True:
            print(self.folder_id)
            response = self.service.files().list(
                q=f"mimeType='image/png' and parents in '{self.folder_id}'",
                spaces='drive',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token).execute()

            for file in response.get('files', []):
                self.Files.append(file)

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    def DownloadFiles(self):
        self.GetFilesForDownload()
        print("-------------------Downloading Files----------------------")
        self.newFiles = []
        for file in self.Files:
            file_Id = file.get('id')
            print(f"{file.get('name')} ({file.get('id')})")

            # download stuff
            request = self.service.files().get_media(fileId=file_Id)  # noqa
            fileHandler = io.BytesIO()
            downloader = MediaIoBaseDownload(fileHandler, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Downloaded {int(status.progress()) * 100}%")
            html = fileHandler.getvalue()

            with open(f"{self.Path}{file.get('name')}", 'wb') as f:
                f.write(html)
                self.newFiles.append(f)
        print("----------------------------END---------------------------")

    def MoveFiles(self):
        print("Moving Files")
        # self.GetFilesForDownload()  # make sure it has files
        if len(self.Files) == 0:
            self.GetFilesForDownload()
        self.newid = self.MakeFolder()
        for file in self.Files:
            file_Id = file.get('id')
            currentfile = self.service.files().get(fileId=file_Id,
                                                   fields='parents').execute()
            previousParent = ",".join(currentfile.get('parents'))
            self.service.files().update(fileId=file_Id,
                                        addParents=self.newid,
                                        removeParents=previousParent,
                                        fields='id, parents').execute()
            print(f"Moved file: {file.get('name')} to {id}")

    def MoveFilesBack(self):
        print("Moving files back")
        self.GetFilesForDownload()
        for file in self.files:
            file_Id = file.get('id')
            self.service.files().update(fileId=file_Id,
                                        addParents=self.moveFolder_Id,
                                        removeParents=self.newid,
                                        fields='id, parents').execute()
            print(f"Moved file: {file.get('name')} back to {self.moveFolder_Id}")  # noqa

    def List(self):
        print("----------------------Files in Drive----------------------")
        self.GetFilesForDownload()
        for file in self.Files:
            print(f"{file.get('name')} ({file.get('id')})")
        print("----------------------------END---------------------------")

    def MakeFolder(self):
        file_metadata = {
            'name': f'{datetime.datetime.now()}',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.moveFolder_Id]
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()
        return file.get('id')
