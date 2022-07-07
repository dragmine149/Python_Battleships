# Installation
  How to install / download the program

Current State: BROKEN (includes all versions)

# Python Versions:
  In theory, this program should work for py3.4+ but this has not been tested. Tests are not fun to write either, so this isn't going to get updated for a while

# How to run:
  The next steps assume you have python3+ installed.
  1. Download this repository or clone it **(recommended)** via `git clone git@github.com:dragmine149/Python_Battleships.git`
  
  The next steps depends on how you want to run your program
  ## Via command line (cmd)
  1. Open your system terminal (E.g. Terminal)
  2. Navagte to the download repository location (`cd <PATH>/Program`)
  3. Run file `Main.py`

  ## Via python Terminal (nearly the same as cmd)
  1. Open up python
  2. `Import os`
  3. `os.system('python <PATH>/Program/Main.py')`

  ## Via file (not recommened)
  1. Open your system file explorer
  2. Navagte to the download repository location
  3. Double click the file `Main.py` in the `Program` folder

  ## Via an idle (Not recommened)
  1. Open your IDE
  2. Navagate to the download repository location
  3. Open and run `Main.py` in `Program`

  Depending on what you go with depends on how the experience will be like, Different people will experience different things.
  [Google Drive Setup](Drive.md)

  ### Why the recommendation?
  As shown as above, some are not recommened for specif reasons, these still work but aren't the best for debugging and bug fixes. Below are the reasons.

  #### Download via git
  This is recommened as it is easier to get new updates, instead of having to download the whole repository again and moving certain files over (settings, data, etc...) Git will change only the files that need changing.

  #### Using command line / Python console
  This is a python program designed to be used in a command line, When you double click the file you are openning it in a command line, just not the best. This commandline also gives you access to the errors and output logs easier.

  #### Via file
  This is not recommended as once it breaks (crashes) the logs are gone, no way to get them back. If you are running into issues and sumbit a bug, you are required to include a log of the recent traceback output.

  #### Via an ide
  Better than a file but some functions will break, There are multiple cases where `os.system('clear')` has been used to clear the output, this will not work in an ide. As well as this, the formatting is terrible because of the use of the colour system. Not all IDEs support the ability to use colours and even when importing colorama they still don't work.

# Optional Modules.
  These are optional modules you can install for this program to work. These are not needed but might provide a better experience.
  You can either go through them all seperatly or call `pip install -r requirements.txt` to automatically install all the optional modules.

  If you don't want to install them manually, the program comes with a built-in setup function.

# Extra Notes:
  Some modules, as you may have noticied, the code has been downloaded and automatically placed into the program itself.
  This is because the code used in those modules are required in other parts of the program to make the program what it is.
  Some of these modules, for example 'colorama' are required and as so, automatically used even if the user has their own local version installed.
