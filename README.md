# Archero Bot 57
This is an archero bot that works on a mobile smartphone connected with usb cable.

## Installation
On linux :
- Install __adb__, package using `$ apt install adb`
- Install __Pillow__,__matplotlib__ packages using `$ pip install Pillow matplotlib`
- Install __Android Studio__ with sdk ([link here](https://developer.android.com/studio))
- Enable __debug mode__ on your Smartphone

## Usage
Once cloned the repo, open your smartphone, open __Archero__ app and run the executable:

```console
$ python static_bot_cave.py
```

To check button locations, use [checkCoordinates](checkCoordinates.py) script.
Create a folder with all your screenshots.
Set [images_path](https://github.com/fabian57fabian/archero_bot_57/blob/7c698dc856576cb986093dd3b352cb54c774df84/checkCoordinates.py#L46) to screenshots path.
launch checkCoordinates script and follow instructions.

## Compatibility
This software works with following devices:
- Samsung s8+

More devices will be added and tested once coordinates will be normalized wrt screen res.