import os


# Those are normalized coordinates of data to be taken and trained into a simple nn to predict game status (multiclass)
def getAttributesArr(self):
    calculus_width = 1080
    calculus_heigth = 2220
    attr = [
        [1024 / calculus_width, 530 / calculus_heigth],  # level up/initial ability choose (right up)
        [50 / calculus_width, 530 / calculus_heigth],  # level up/initial ability choose (left up)
        [1010 / calculus_width, 370 / calculus_heigth],  # blessing and devil (up right)
        [50 / calculus_width, 370 / calculus_heigth],  # blessing and devil (up left)
        [70 / calculus_width, 870 / calculus_heigth],  # Ending game green and ending final red (up left)
        [1110 / calculus_width, 870 / calculus_heigth],  # Ending game green and ending final red (up right)
        [713 / calculus_width, 1665 / calculus_heigth],
        # special prize color (ad when blessing and devil is yellow) (center right)
        [400 / calculus_width, 1665 / calculus_heigth],
        # special prize color (ad when blessing and devil is yellow) (center left)
        [193 / calculus_width, 1740 / calculus_heigth],  # Devil Reject
        [896 / calculus_width, 1740 / calculus_heigth],  # Devil Accept
        [113 / calculus_width, 1336 / calculus_heigth],  # Left ability background
        [446 / calculus_width, 1336 / calculus_heigth],  # Center ability background
        [784 / calculus_width, 1336 / calculus_heigth],  # Right ability background
        [184 / calculus_width, 1690 / calculus_heigth],  # Left angel blessing background
        [690 / calculus_width, 1690 / calculus_heigth],  # Right angel blessing background
        [500 / calculus_width, 1900 / calculus_heigth],  # Left playing joystick blue
        [570 / calculus_width, 1690 / calculus_heigth],  # Right playing joystick blue
        [1060 / calculus_width, 60 / calculus_heigth],  # up right money grey count playing
    ]
    return attr


def getAttributes(self, frame):
    pass


attributes = []
