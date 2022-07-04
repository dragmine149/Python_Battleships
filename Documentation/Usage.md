# Python Battleship usage
This is a simple intuative program to use but below are all the menus and how they work and what they do in detail.

## Main Menu (python Main.py)
The first menu you will see, simple easy to navigate and use.
Not much is on this menu, a link to the github repo and selections for other parts of the program

### Options
0: Quit
- Closes the program

1: Select game
- Lets you select a game from a list of saved games

2: Make game
- Lets you make a game with your own custom settings

3: Settings
- Lets you edit settings


## Settings
There are currently 5 different options in settings, each doing a different thing which you can customise to your liking.
Note: settings will change overtime and mods might add more settings to the list that aren't listed here. Please check the mod description for those settings.

### Settings (Options)
-1: Load from file
- Loads old settings from a file. Can be better than locating the folder of where the files are saved. (Program Location/Program/Files/Data btw)

0: Back
- Does what it says on the tin, goes back to main menu

1: Change location
- Changes the default save location to specified location. As well as tests whever it can access that location.
- Useful for playing multiplayer games

2: Change Colour
- A fun feature that's not really needed but i personally like. You can set your colour to anything and during multiplayer, your name will be shown in the colour you set it to. 
- This setting also works by giving it only the first letter of the colour you would like your name to be. Useful if you can't spell.

3: Delete Cache
- Not really a setting, but something worth having. This command will delete all the cache in __pycache__ and and folders that end in __cache.
- This does not stop the program on use, Delete any saved data.

4: Setup
- Installs modules that are optional to use but could make the experience overall better.
- These modules are not installed / bundled with the program by default as they are purley optional with little parts of the program using them.

## Make Game
This screen lets you make a game based on your own settings. By default, most of the options will be filled out for you but they can still be changed.

### Make Game Options
0: Back
- Returns back to the main meun

1: Game Name
- Required: yes
- Input: string
- A name of the game, helps to find easier in long list of games. 

2: Usernames
- Required: yes
- Input: string
- Two usernames, inputted one after enough. These are the name of the players that are going to be playing.
- Special features
 -- Using the word `me` will use your system username.
 -- If both names are the same, then `(2)` will automatically be added to the second name
 -- If `me` is used, anything after the `me` will be placed in brackets. Example: `me149` -> `dragmine149`

3: Board Size
- Required: no
- Input: two interger numbers
- Default: [10, 10]
- The board size, really important. This board can go from 5x5 to infxinf, although i would recommend not changing it unless you have mods installed (for extra ships)

4: Save Location
- Required: no
- Input: string (path)
- Default: Save location determind in settings
- Where to save the game, needs to be a path and has a read write check for that path to make sure it will be able to save there.

5: Multiplayer
- Required: no
- Input: boolean (yes or no)
- Default: no
- Locked by: Save Location (If Save location is set to `Saves` will not let the user initalise multiplayer.)
- Whever to specify multiplayer, just because you have an external save doesn't mean you want to play multiplayer.

6: Password
- Required: no
- Input: password
- Default: None
- Recommened: yes
- This password makes your game more secure to the average user. Instead of letting anyone play, this will mean only those with the password (and save location) can play. 
- Note, the password is not 100% encrypted and can be decrypted using the save editor, but for the normal user will stop them getting into the wrong games.

7: Save
- Saves the game with the settings above.
- Does checks to make sure you can save.
- Returns you back to placing the ships.

## Select game
Another simply menu like the main menu, with a few more features.

### Features and options
Features
- At the top of the page, will display the save location and whever it's an external or internal save location.

Options:

1 -> inf: The save game number, these are automatically assagined to the save games found in the desired folder.
0: Back, returns the user back to the main menu
-1: Delete a game using the index number above.
-2: Changes the path in the cache, Resets on cache cleared, program reboot.


## Place Menu
A menu accessed by loading into a game where your ships haven't been placed yet.
Lets you place your ships on a grid.

### Options
1 -> inf: Ships, these can also include modded ones.
0: Back, returns.

Whilst placing a ship, there are multiply questions that you will be asked.
1: Location
- Where the ship is to be placed on the grid.
- Requirement XY (letter, number)
- This is like normal battleships where you would fire at letter number.

2: Rotation
- Rotation of ship.
- North, East, South, West.
- Which way your ship should be rotated.
- Note, you can say the whole word but it will only check of `N`, `E`, `S` or `W` in the first character of the word.

3: Confirmation
- Confirm you are happy with your ship placement.

## Shooting Menu
Finally, after going through all the other menus, you get to shoot at your opponent.
This menu contains all the information about the game, where both people have shot. And if playing online multiplayer, your board as well. There really isn't many things on this menu because you are only shooting.

### Options
Location: Where to shoot
- Follows the same logic as the location in the place system (above)
- Returns `X` or `+` on hit or miss. (Automatic feadback without them having to say anything)
- Using `0` will return you and quit out of the game

# Other
Modes can have some influence in menus and what they do.
When menus get updated, this file will also be updated.
