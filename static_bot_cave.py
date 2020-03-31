from CaveDungeonEngine import CaveEngine
import sys


def get_start_lvl_from_args():
    start_lvl = 0
    if len(sys.argv) > 1:
        try:
            arg = sys.argv[1]
            start_lvl = int(arg)
            if start_lvl < 0 or start_lvl > 20:
                print("Given starting level is not a valid start level in [0,20]. Starting from zero")
                start_lvl = 0
        except:
            print("Given starting level is not a valid start level. Starting from zero")
            start_lvl = 0
    return start_lvl


while True:
    engine = CaveEngine()
    engine.start_infinite_play(get_start_lvl_from_args())
