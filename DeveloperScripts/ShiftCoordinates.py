from src.Utils import *
import shutil

old_width = 1080
old_height = 2220
instructions = """
Some smartphones have really high resolutions but they are normally cropped on the upper with a black strip.
So This script is intended to change (in-place) the movements, buttons and static_coords of a given resolution.

Instructions:
- take a screenshot, memorize width and height (e.g. 1080x2340)
- calculate rows_black, being the number of rows of black pixels in the screen you took (e.g. 75)
- Set the variables of this script according to what you have calculated before.
- Run it
"""
debug = False
print(instructions)
rows_black = 75
width = 1080
height = 2340
new_folder = buildDataFolder(width, height)
print("Data you have choosen:\nNew screen folder: %s\nBlack rows to remove: %d" % (new_folder, rows_black))
a = input("If the variables are coorect, select if you want to start (y/n):")
if a != 'y' and a != 'yes':
    exit(1)

old_folder_copy = os.path.join("../datas", buildDataFolder(old_width, old_height), "coords")
new_folder_copy = os.path.join("../datas", new_folder, "coords")
if os.path.exists(new_folder_copy):
    print("Folder %s already exists. Save a backup and remove it before starting")
    exit(1)

os.mkdir(os.path.join("../datas", new_folder))
os.mkdir(os.path.join("../datas", new_folder, "coords"))
os.mkdir(os.path.join("../datas", new_folder, "screens"))
for f in os.listdir(old_folder_copy):
    shutil.copy(os.path.join(old_folder_copy, f), os.path.join(new_folder_copy, f))


def points_map(x: float, in_min: float, in_max: float, out_min: float, out_max: float):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def shift_pos(pos: list):
    un_normalized = (pos[1] * old_height) * 1.0
    pos[1] = points_map(un_normalized, 0, old_height, rows_black, height) / float(height)


paths = [
    os.path.join("../", getCoordFilePath('buttons.json', sizePath=new_folder)),
    os.path.join("../", getCoordFilePath('movements.json', sizePath=new_folder)),
    os.path.join("../", getCoordFilePath('static_coords.json', sizePath=new_folder))
]

buttons, movements, static_coords = loadJsonData(paths[0]), loadJsonData(paths[1]), loadJsonData(paths[2])

print("Processing buttons")
for k, b in buttons.items():
    if debug: print("Shifting %s" % k)
    shift_pos(b)
saveJsonData_oneIndent(paths[0], buttons)
print("Processing movements")
for k, m in movements.items():
    if debug: print("Shifting %s" % k)
    shift_pos(m[0])
    shift_pos(m[1])
saveJsonData_oneIndent(paths[1], movements)
print("Processing static_coords")
for k, coord_check in static_coords.items():
    if debug: print("Shifting %s coordinates" % k)
    for coord in coord_check['coordinates']:
        shift_pos(coord)
saveJsonData_oneIndent(paths[2], static_coords)

print("End. You'll find your shifted files in %s." % os.path.join("../datas", new_folder))
print(
    "Make also sure to copy some screenshots to screens folder (%s)" % os.path.join("../datas", new_folder, 'screend'))
