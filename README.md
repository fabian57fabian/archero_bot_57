# Archero Bot 57

<p align="center">
  <img src="https://github.com/fabian57fabian/archero_bot_57/blob/master/repo_images/logo_small.png">
</p>

Watch the installation video:

[![Watch the video](https://github.com/fabian57fabian/archero_bot_57/blob/master/repo_images/video_thumbnail.png)](https://www.youtube.com/watch?v=XZTI_USaY-4)

## Contents
1. [Introduction](#introduction)
2. [Installation on Linux](#Installation-on-Linux)
3. [Installation on Windows](#installation-on-windows)
4. [Platform installation (emulator)](#platform-installation)
5. [Game lock disabling](#disable-blue-auto-lock-screen)
6. [Usage](#usage)
7. [Game Description](#game-description)
8. [Coordinates management](#coordinates-management)
9. [How it works](#how-it-works)
10. [Coordinates check explained](#coordinates-check-explained)
11. [Extra](#extra)

## Introduction 
This is an archero bot that works on a mobile smartphone connected with usb cable.
It was originally build to continously start a game (dungeon 6: the cave), play it until end and loop until energy bar is below 5. Then wait for energy to restart.

- Supported OS:
  - Windows
  - Ubuntu/Linux distro

- Supported platform:
  - Usb connection to phone
  - Nox emulator (installation video coming soon)

- Tested resolutions
  - 1080x1920 is full working. Remaining tests have to be done
  - 1080x2220 is full working. All tests show good coordinates positioning.
  - 1080x2280 is working. Remaining tests have to be done
  - 1080x2340 is working. Remaining tests have to be done
  - failing on other resolutions, but working on...

If you don't find your screen resolution and you want to contribue, follow these [instructions](wiki/ContributeWithScreens.md).

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
- Open a Command Line (press start, write CMD, press enter) and execute following commands by copying and pasting in the command line and pressing enter:
  
  `pip install Pillow matplotlib numpy pure-python-adb pyqt5`
  
- Finally, download this program by clicking (in this page) on "Clone or download ->Download Zip". Once downloaded extract the compressed file (Left click -> Extract Here) and copy where you want. This is the program folder.

## Platform installation
This bot can work either connected to smartphone trough usb or with Nox emulator on your pc.

If you want to use your phone, skip these steps.

If you want to use the emulator:
- Download Nox emulator from [here](https://www.bignox.com/) and install it.
- Open the emulator
- Insert your google mail and password (the account that you use on your phone, that archero uses to save data).
- Enable debug mode (settings->info and tap 7 times on build, then go back, development options, activate debug usb)
- Download the archero bot on the emulator.
- Open it

### Disable Blue auto lock screen
When using this bot with a Samsung (like S7, S8, S9, S10 and S20 along with plus, edge, note and ultra versions) the Game Tools will automatically lock your screen with a little blue lock every 35 seconds.
To disable it, follow this:

- Open your gamea, and swipe UP FROM THE BOTTOM OF THE SCREEN. You will see the Game Tools icon in the bottom left. Click this.
- Click on Advanced game features.
- Turn Auto screen lock OFF 

Thanks to [userYIxYmjMxs6](https://us.community.samsung.com/t5/user/viewprofilepage/user-id/14128964) for this [post](https://us.community.samsung.com/t5/Galaxy-S8/Annoying-quot-Drag-Lock-icon-to-unlock-quot/td-p/539737) on samsung community.

## Usage
Once cloned the repo, execute **GameController.py**. The interface is not complete but provides basic view and play operations.
\
Remember to __disable notifications__ or __activate Do Not Disturb mode__.


### Game description
Set dungeon to **The Cave** (number 6) and run the executable GameController.py:
\
If you launch from terminal, it is possible to specify the starting level of first run (e.g. `python static_bot_cave.py 16`).
\
If setting start from 0, the program will check your energy. If 5 or above, then starts a game and plays until he dies. He normally does between 12 to 20 levels.
\
Once it ends, he goes to main menu and checks another time if it has energy.
This program is not perfect. If he somehow thinks to be on a different level but the game is ahead, please manually end the game, return to main menu and restart the game.
\
Even if it will fail, no harm will be done (it will not exit and click randomly on your phone).

## Coordinates Management
### Static coordinates check

The bot takes screenshots over time and detecting what is currently on the screen is a requested operation before starting the bot.
With this said you have to execute **check_static_coors.py** and checking that each row starts with **OK**.

If some **NO_DETECTION** are found, don't start the bot.
Other **MULTIPLE_DETECTIONS** are allowed.

### Coordinates check
If the program is clicking in wrong places, then use [TouchManager](TouchManager.py) script.
Create a folder with all your screenshots.
Set [images_path](https://github.com/fabian57fabian/archero_bot_57/blob/7c698dc856576cb986093dd3b352cb54c774df84/checkCoordinates.py#L46) to screenshots path.
launch TouchManager script and use the interface (for windows double-click on 'checkCoordinates.py.').
Current version: basic_usage.


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
### Coordinates check explained
In order to detect the game state, a static coordinate check is done.
For each interesting state (on pause, on devil question, on skill choose) there is a list of (x,y) coordinates that checks if the color is in a specific color range.
Example:
\
Checking 'endgame' consist in checking that we see the 'blue' color in 3 different points.
\
These coordinates have to have red, green, blue colors in an interval being (48, 98, 199) +- 5.
\
In the future implementation, this hole static check will be replaced by a neural network model trained to automatically detect those data in the screenshot.


## Issue: Adb not working
If adb doesn't work or installation failed, check out this [video](https://www.youtube.com/watch?v=vr0GLIufzkM). It explains how to install on windows and ubuntu.

## Statistics saving

Every game statistics is saved in datas folder as a **statisics** csv file. It can be opened by LibreOffice or Excel.
\
This is usefull in future games plotting to know how it performed.

## Extra

Thanks to [RimanCz](https://github.com/RimanCz) for screenshorts done with Samsung S10e (1080x2280).
\
Thanks to [MahirZukic](https://github.com/MahirZukic) for screenshorts done with Xiaomi Mi 9 (1080x2340).
\
Thanks to [AgamemnonasKyr](https://github.com/AgamemnonasKyr) for screenshots done for upper black strip in game (1080x2280).
\
For any bug open an issue.
If not having a github account, email me at **fabian_57@yahoo.it**.
