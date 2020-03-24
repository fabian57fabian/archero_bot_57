# Archero Bot 57
This is an archero bot that works on a mobile smartphone connected with usb cable.

## Installation on Linux
Follow these steps to install __adb__, python lisb such as __Pillow__,__matplotlib__, __numpy__, __pure-python-adb__, __pyqt5__:
- `$ apt install adb`
- `$ pip install Pillow matplotlib numpy pure-python-adb`
- `$ pip install pyqt5` . If it fails, try with `$ sudo apt-get install python3-pyqt5`
- Install __Android Studio__ with sdk ([link here](https://developer.android.com/studio))
- Enable __debug mode__ on your Smartphone (Settings -> about phone/info and tap 7 times on kernel version, then Settings -> debug options, activate it, debug mode and activate it). May vary based on phone model.

## Installation on Windows
Follow these steps:
- Install latest __python__ from [here](https://www.python.org/downloads/). When installing, make sure to select "Add to PATH" in first page of installation wizard
- Install __Android Debug Bridge__:
  - Download adb package from [here](https://www.androidworld.it/2017/01/07/adb-fastboot-download-windows-mac-linux-450541/)
  - Extract the compressed file (Left click -> Extract Here)
  - Rename the extracted folder to 'adb'
  - Copy 'adb' folder into 'C:'
  - Go to Control Panel -> System -> Advanced system settings -> Environment Variables
  - Under "System variables" list, find 'Path', click on it and then click on 'Edit...' button below
  - Click 'New' and in the created TextBox write 'C:\adb'
  - Click 'OK' and then exit
- Open a Command Line (press start, write CMD, press enter) and execute following commands by copying and pasting in the command line and pressing enter (one by one):
  - pip install Pillow matplotlib numpy pure-python-adb pyqt5

## Adb not working
If adb doesn't work or installation failed, check out this [video](https://www.youtube.com/watch?v=vr0GLIufzkM). It explains how to install on windows and ubuntu.

### Disable Blue auto lock screen
When using this bot with a Samsung (like S7, S8, S9, S10 and S20 along with plus, edge, note and ultra versions) the Game Tools will automatically lock your screen with a little blue lock every 35 seconds.
To disable it, follow this:

- Open your gamea, and swipe UP FROM THE BOTTOM OF THE SCREEN. You will see the Game Tools icon in the bottom left. Click this.
- Click on Advanced game features.
- Turn Auto screen lock OFF 

Thanks to [userYIxYmjMxs6](https://us.community.samsung.com/t5/user/viewprofilepage/user-id/14128964) for this [post](https://us.community.samsung.com/t5/Galaxy-S8/Annoying-quot-Drag-Lock-icon-to-unlock-quot/td-p/539737) on samsung community.

## Usage
Once cloned the repo, open your smartphone, open __Archero__ app. Set UseGeneratedData variable to True in next scripts if automatic energy level detection does not work.

### Slow and high loot
Set dungeon to **The Cave** (number 6) and run the executable:
```console
$ python static_bot_cave.py
```
This will check your energy. If 5 or above, then starts a game and plays until he dies. He normally does between 12 to 18 levels.
Once it ends, he goes to main menu and checks another time if it has energy.

### Fast and low loot
Open Archero, choose dungeon **Ruined Lands** (number 10) and launch the script:
```console
$ python static_bot_ruined_lands.py
```
This will go to your avatar, remove the weapon, go back, check for energy and when available plays by dying at level 1.
Then goes back to main level and repeats until no energy left.

## Buttons location check
If the program is clicking in wrong places, then use [TouchManager](TouchManager.py) script.
Create a folder with all your screenshots.
Set [images_path](https://github.com/fabian57fabian/archero_bot_57/blob/7c698dc856576cb986093dd3b352cb54c774df84/checkCoordinates.py#L46) to screenshots path.
launch TouchManager script and use the interface.
Current version: basic_usage.

To execute archero bot by interface, use [GameController](GameController.py.py) script.
Just launch it with python and start using it.
Current version: not_ended.

## Compatibility
This software works with following devices:
- Samsung s8+

More devices will be added and tested once coordinates will be normalized wrt screen res.

## How it works
The package adb lets us use various android tools like:
- tapping on a screen coordinate
- swiping between two points in an amount of time
- taking a screenshot

With those functions, i built a dictionary with needed coordinates (in datas/default_dict.py) to start with.

All coordinates are normalized in [0, 1]. This is done because then we will set our screen width and height according to the phone screen used.

Using the TouchManager app we can check each point location for each screenshot that we have (default folder images/samsungs8+).

When we are in need to check something on the screen, we take a screenshot (saved as 'screen.png'), load the image as a list of pixels and get from it a set of pixel locations. Then check those with our needed pixels. All this is done in the game_screen_connector script.
For example when checking if having 5 or more energy to play one game, we check that pixel corresponding to 5th bar of energy is blue:

![Check_bar](wiki_data/check_energy_green_bar_location.png)

## Extra

Thanks to [RimanCz](https://github.com/RimanCz) for screenshorts done with Samsung S10e.