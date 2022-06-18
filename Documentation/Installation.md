# Installation
  How to install / download the program

Current State: BROKEN (includes all versions)

# Python Versions:
  These are versions that have been tested for this program to work. I recommend you get the newest version though.
  - Python3.4
    - Main part (might be a bit broken)
    - Google Drive Api (unknown)
  - Python3.5
    - Main part (unknown)
    - Google Drive Api (unknown)
  - Python3.6
    - Main part (unknown)
    - Google Drive Api (unknown)
  - Python3.7
    - Main part (unknown)
    - Google Drive Api (unknown)
  - Python3.8
    - Main part (unknown)
    - Google Drive Api (unknown)
  - Python3.9
    - Main part (works)
    - Google Drive Api (in progress)
  - Python3.10
    - Main part (unknown)
    - Google Drive Api (unknown)

# How To:
  The next steps assume you have python3+ installed.
  1. Download a zip file of `Program` folder. Or clone the repo.
  2. Navagate to the repo in a terminal window. (`cd <PATH TO FILE>`)
      Note: if using the python terminal (instead of command prompt, mac/linux terminal) you need to take these steps:
      1. `import os`
      2. `os.system('STEP 3')`
      Note: if you downloaded the repo, you need to cd into the Program folder as well
  3. Run Main.py (`python Main.py`)

## Optional Modules.
  These are optional modules you can install for this program to work. These are not needed but might provide a better experience.
  You can either go through them all seperatly or call `pip install -r requirements.txt` to automatically install all the optional modules.

### Google Drive api
  This also requires more setup as per this [documentation][https://developers.google.com/drive/api/quickstart/python]:
  `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
