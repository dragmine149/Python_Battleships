# Installation
  How to install / download the program

Current State: BROKEN (includes all versions)

# Python Versions:
  In theory, this program should work for py3.4+ but this has not been tested. Tests are not fun to write either, so this isn't going to get updated for a while

# How To:
  The next steps assume you have python3+ installed.
  1. Download a zip file of `Program` folder. Or clone the repo **(recommended)** `git clone git@github.com:dragmine149/Python_Battleships.git`.
  2. Navagate to the repo in a terminal window. (`cd <PATH TO FILE>`)
      Note: if using the python terminal (instead of command prompt, mac/linux terminal) you need to take these steps:
      1. `import os`
      2. `os.system('STEP 3')`
      If you don't take the above steps and run the file, you won't be able to see the output and report a bug if you encounter one. (You can still play, but when it breaks you can't report the bug)
      Note: if you downloaded the repo, you need to cd into the Program folder as well
  3. Run Main.py (`python Main.py`)

  [Google Drive Setup](Documentation/Drive.md)

## Optional Modules.
  These are optional modules you can install for this program to work. These are not needed but might provide a better experience.
  You can either go through them all seperatly or call `pip install -r requirements.txt` to automatically install all the optional modules.

  If you don't want to install them manually, the program comes with a built-in setup function.

### Extra Notes:
  Some modules, as you may have noticied, the code has been downloaded and automatically placed into the program itself.
  This is because the code used in those modules are required in other parts of the program to make the program what it is.
  Some of these modules, for example 'colorama' are required and as so, automatically used even if the user has their own local version installed.
