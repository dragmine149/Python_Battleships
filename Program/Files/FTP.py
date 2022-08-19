import ftplib
import importlib
import os
import time
Functions = importlib.import_module('Files.Functions')
# Settings = importlib.import_module('Files.Settings')

class FileTransferProtocole:
    """
    Details:
    --------
    A class to have easy FTP access to a server. Just a couple of small commands.
    
    Paramaters:
    -----------
    server: string -> Server Address, ip allowed.
    username: string -> Your username for the FTP server.
    password: string -> Your password for the FTP server.
    location: string -> the directory to go to after login, default root.
    port: int -> The port of the FTP server
    """
    
    def __slash(self):
        # Determinds how to split paths
        return "\\" if os.name == "nt" else "/"
    
    def __init__(self, server, username, password, location="/", port=21):
        self.username = username
        self.password = password
        self.server = server
        self.location = location
        self.port = port
        self.msg = "FTP"  # message to show when on load screen,
    
    def login(self):
        """Login to the FTP server using the details given.
        """
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.server, self.port)
        self.ftp.login(self.username, self.password)
        self.ftp.cwd(self.location)
    
    def logout(self):
        """Log out of the FTP server. (Recommeneded)
        """
        self.ftp.quit()
    
    def ListDirectory(self):
        """Gets a list of all files in the current directory

        Returns:
            list: The items in the current working directory
        """
        return self.ftp.nlst()

    def MakeDirectory(self, name):
        """Make a directory, automatically make sub directories if specified.

        Args:
            name (string): The name of the file, supports sub directories.
        Returns:
            string: The name input
        """
        
        directories = name.split(self.__slash())
        currentPath = self.GetPath()
        for item in directories:
            if item not in self.ListDirectory():
                self.ftp.mkd(item)
            self.ftp.cwd(item)
        self.ftp.cwd(currentPath)
        return name
    
    def GetPath(self):
        """Returns the current working path

        Returns:
            string: The path where the FTP client is currently located.
        """
        return self.ftp.pwd()

    def ChangeDirectory(self, dir):
        """Changes the working directory on the FTP link

        Args:
            dir (string): The directory to change to

        Returns:
            Success: Whever the code was successfully in changing directory.
        """        

        try:
            print(f"Current directory: {self.GetPath()} New dir: {dir}")
            self.ftp.cwd(dir)
            return True
        except ftplib.error_perm:
            Functions.PrintTraceback()
            return False

    def UploadFile(self, path):
        """Upload a file to the server

        Args:
            path (string): The local path of the file.
        Returns:
            path (string): Location of where the file got saved
        """
        pathInfo = path.split(self.__slash())
        name = pathInfo[len(pathInfo) - 1]
        handle = open(path, 'rb')
        self.ftp.storbinary('STOR %s' % name, handle)
        handle.close()
        return path
    
    def DownloadFile(self, path):
        """Download a file from the server

        Args:
            path (string): The local destination of the path.
        Returns:
            path (string): Path of the downloaded file, none if failed.
        """
        pathInfo = path.split(self.__slash())
        name = pathInfo[len(pathInfo) - 1]
        
        handle = open('Saves{}.Temp{}{}'.format(self.__slash(),
                                                self.__slash(),
                                                name), 'wb')
        self.ftp.retrbinary('RETR %s' % name, handle.write)
        handle.close()
        return path
    
    def Delete(self, path):
        self.ftp.delete(path)



if __name__ == "__main__":
    ftpClient = FileTransferProtocole('192.168.120.3', 
                                      'Example', 
                                      'Example',
                                      '/home/Example')
    ftpClient.login()
    print(ftpClient.ListDirectory())
    ftpClient.MakeDirectory('FTPTest/a/b')
    ftpClient.ChangeDirectory('FTPTest/a/b')
    print(ftpClient.ListDirectory())
    print(ftpClient.GetPath())
    ftpClient.UploadFile('Data/Settings')
    os.remove('Data/Settings')
    time.sleep(1)
    ftpClient.DownloadFile('Data/Settings')
    time.sleep(1)
    ftpClient.Delete('Settings')
    ftpClient.ChangeDirectory('..')
    ftpClient.Delete('b')
    ftpClient.ChangeDirectory('..')
    ftpClient.Delete('a')
    ftpClient.ChangeDirectory('..')
    ftpClient.Delete('FTPTest')
    print(ftpClient.ListDirectory())
    ftpClient.logout()