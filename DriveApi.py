from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import datetime
import io
import time
os.chdir(os.path.dirname(os.path.realpath(__file__)))

SCOPES = ['https://www.googleapis.com/auth/drive']


class Api:
    def __init__(self, folderId):
        if not os.path.exists("ApiFiles"):
            os.mkdir("ApiFiles")
        self.service = self.__LoadAPI__()
        self.folder = folderId

    def __LoadAPI__(self):
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

    def Test(self, folderId):
        def makeFolder(folderId):
            folder_metadata = {
                'name': 'Battleships_test',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [folderId]
            }
            return self.service.files().create(body=folder_metadata,
                                            fields='id').execute()

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

        def DelLocal():
            if os.path.exists("DownloadFileTest.txt"):
                os.remove("DownloadFileTest.txt")
                return True
            else:
                return False

        def DelServer(file, folder):
            self.service.files().delete(fileId=file).execute()
            self.service.files().delete(fileId=folder).execute()

        folder = makeFolder(folderId)
        print(folder)
        file = uploadFile(folder)
        print(file)
        down = downloadFile(file['id'])
        time.sleep(5)  # updates
        DelLocal()
        DelServer(file['id'], folder['id'])

    def UploadData(self, data={'name':'error', 'path':'UploadFileTest.txt'}, folder=False):
        metadata = {}
        media = None
        if folder:
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
            media = MediaFileUpload(data['path'],
                                    mimeType='*/*',
                                    resumable=True)
        if media:
            return self.service.files().create(body=metadata,
                                                media_body=media,
                                                fields='id').execute()
        else:
            return self.service.files().create(body=metadata,
                                                fields='id').execute()


    # def GetFilesForDownload(self):
    #     self.Files = []
    #     page_token = None
    #
    #     while True:
    #         print(self.folder_id)
    #         response = self.service.files().list(
    #             q=f"mimeType='image/png' and parents in '{self.folder_id}'",
    #             spaces='drive',
    #             fields='nextPageToken, files(id, name)',
    #             pageToken=page_token).execute()
    #
    #         for file in response.get('files', []):
    #             self.Files.append(file)
    #
    #         page_token = response.get('nextPageToken', None)
    #         if page_token is None:
    #             break
    #
    # def DownloadFiles(self):
    #     self.GetFilesForDownload()
    #     print("-------------------Downloading Files----------------------")
    #     self.newFiles = []
    #     for file in self.Files:
    #         file_Id = file.get('id')
    #         print(f"{file.get('name')} ({file.get('id')})")
    #
    #         # download stuff
    #         request = self.service.files().get_media(fileId=file_Id)  # noqa
    #         fileHandler = io.BytesIO()
    #         downloader = MediaIoBaseDownload(fileHandler, request)
    #         done = False
    #         while done is False:
    #             status, done = downloader.next_chunk()
    #             print(f"Downloaded {int(status.progress()) * 100}%")
    #         html = fileHandler.getvalue()
    #
    #         with open(f"{self.Path}{file.get('name')}", 'wb') as f:
    #             f.write(html)
    #             self.newFiles.append(f)
    #     print("----------------------------END---------------------------")
    #
    # def MoveFiles(self):
    #     print("Moving Files")
    #     # self.GetFilesForDownload()  # make sure it has files
    #     if len(self.Files) == 0:
    #         self.GetFilesForDownload()
    #     self.newid = self.MakeFolder()
    #     for file in self.Files:
    #         file_Id = file.get('id')
    #         currentfile = self.service.files().get(fileId=file_Id,
    #                                                fields='parents').execute()
    #         previousParent = ",".join(currentfile.get('parents'))
    #         self.service.files().update(fileId=file_Id,
    #                                     addParents=self.newid,
    #                                     removeParents=previousParent,
    #                                     fields='id, parents').execute()
    #         print(f"Moved file: {file.get('name')} to {id}")
    #
    # def MoveFilesBack(self):
    #     print("Moving files back")
    #     self.GetFilesForDownload()
    #     for file in self.files:
    #         file_Id = file.get('id')
    #         self.service.files().update(fileId=file_Id,
    #                                     addParents=self.moveFolder_Id,
    #                                     removeParents=self.newid,
    #                                     fields='id, parents').execute()
    #         print(f"Moved file: {file.get('name')} back to {self.moveFolder_Id}")  # noqa
    #
    # def List(self):
    #     print("----------------------Files in Drive----------------------")
    #     self.GetFilesForDownload()
    #     for file in self.Files:
    #         print(f"{file.get('name')} ({file.get('id')})")
    #     print("----------------------------END---------------------------")
    #
    # def MakeFolder(self):
    #     file_metadata = {
    #         'name': f'{datetime.datetime.now()}',
    #         'mimeType': 'application/vnd.google-apps.folder',
    #         'parents': [self.moveFolder_Id]
    #     }
    #     file = self.service.files().create(body=file_metadata,
    #                                        fields='id').execute()
    #     return file.get('id')

if __name__ == "__main__":
    api = Api(input("Folder id: "))
    api.Test(input("folder id: "))
    # result = api.UploadData({'name':'FolderTest', 'path':''}, True)
    # print(result)
    # api.UploadData({'name':'FileTest', 'path':'UploadFileTest.txt'}, False)
