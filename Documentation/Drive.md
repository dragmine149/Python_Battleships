# Google drive
Google drive is a good program, and the api is built into this program, Unfortunatly it takes a while to setup but is very useful if you don't want to download something like google drive for desktop.

## Setup (cloud)
1. Go to `https://console.cloud.google.com/` and create a new project
2. Go to `APIs & Services` (whilst in the project)
3. Go to `Credentials`
4. Create a new `OAuth 2.0` id with application type of `Desktop Client`
5. Download the json for this newly created `OAuth` id (we will deal with this file later). Name the file `credentials.json`
6. Go to `Enabled APIs & Services`
7. Click `ENABLE APIS AND SERVICES`
8. Search for `Drive` and click the first result
9. click `Enable`

## Setup (local)
Either way will work, but all of the options are here.

### Option 1
Move the file into the program yourself.
1. Navigate to `{LOCAL_FOLDER}/Python_Battleships/Program/Files/ApiFiles`
2. Place `credentials.json` (downloaded eariler) in that folder
That's all, nothing else needs to be done here.

### Option 2
Let the program find the file.
If you attempt to use the api without the required files, the program will automatically try and find `credentials.json` one directory above itself. If it gets found, it will move it automatically.

### Option 3
Let the program ask you for file location.
Like option 2, but the program will also ask your for file location. This way also renames the file in case you forgot to do it back up in step 5. But otherwise the same as option 2.

## Finally
Next time you go to use a google drive file, the program will make sure the files are there before doing anything.
There is one final step, but its not as complicated as some of the other things.

### Last Step
Google drive has a `token.json` file which gets automatically generated after giving this program permission to use drive. Sometimes, this file can expire forcing you to regenerate it (done semi-automatically.)

1. Open the URL in a browser if you haven't already been directed there
2. Click the account you want to use
3. Click `continue`
4. Click `continue` again
5. Close window, everything setup.