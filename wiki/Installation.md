# Installation instructions

## Installation on Linux
Follow these steps to install __adb__, python lisb such as __Pillow__,__matplotlib__, __numpy__, __pure-python-adb__, __pyqt5__:
- `$ apt install adb`
- `$ pip install Pillow matplotlib numpy pure-python-adb requests`
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
  
  `pip install Pillow matplotlib numpy pure-python-adb pyqt5 requests`
  
- Finally, download this program by clicking (in this page) on "Clone or download ->Download Zip". Once downloaded extract the compressed file (Left click -> Extract Here) and copy where you want. This is the program folder.

## Installation on MAC

Follow these steps:
- Install [Homebrew](https://brew.sh/)
- Install [ADB](https://medium.com/macoclock/launch-adb-installed-by-homebrew-on-macos-59d87f4336c9)

  ```bash
  brew install android-platform-tools
  ```

- Install Python prerequirements

  ```bash
  pip install Pillow matplotlib numpy pure-python-adb
  pip install pyqt5
  ```

- Install __Android Studio__ with sdk ([link here](https://developer.android.com/studio))
- Enable __debug mode__ on your Smartphone (Settings -> about phone/info and tap 7 times on kernel version, then Settings -> debug options, activate it, debug mode and activate it). May vary based on phone model.

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
