import time
from adb_connector import *


class GameScreenConnector:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # This should be in format abgr
        self.end_data = self.load_end_data([190, 32, 24, 255])
        self.equip_data = self.load_equip_data([231, 191, 105, 255])
        self.low_enegy_data = self.load_energy_data([41, 182, 37, 255])
        self.lvl_up_data = self.load_lvlup_data([255, 181, 0, 255])
        self.fortune_wheel_data = self.loadFortune_wh_data([255, 181, 0, 255])

    def load_end_data(self, ending_color):
        end_frame_attr = [[170 / 1080, 1230 / 2220],
                          [890 / 1080, 1230 / 2220],
                          [800 / 1080, 780 / 2220]]
        end_frame_attr = [[el[0] * self.width, el[1] * self.height] for el in end_frame_attr]
        frame_red_ending = [ending_color for _ in end_frame_attr]
        return [end_frame_attr, frame_red_ending]

    def load_equip_data(self, eqip_color):
        equip_frame_attr = [[855 / 1080, 1576 / 2220]]
        equip_frame_attr = [[el[0] * self.width, el[1] * self.height] for el in equip_frame_attr]
        frame_equip = [eqip_color for _ in equip_frame_attr]
        return [equip_frame_attr, frame_equip]

    def load_energy_data(self, energy_green):
        energy_frame_attr = [[373 / 1080, 65 / 2220]]
        energy_frame_attr = [[el[0] * self.width, el[1] * self.height] for el in energy_frame_attr]
        energy_frame_value = [energy_green for _ in energy_frame_attr]
        return [energy_frame_attr, energy_frame_value]

    def load_lvlup_data(self, lvl_up_color_yellow):
        lvl_up_frame_attr = [[70 / 1080, 530 / 2220],
                             [1020 / 1080, 530 / 2220]]
        lvl_up_frame_attr = [[el[0] * self.width, el[1] * self.height] for el in lvl_up_frame_attr]
        frame_yellow_ending = [lvl_up_color_yellow for _ in lvl_up_frame_attr]
        return [lvl_up_frame_attr, frame_yellow_ending]

    def loadFortune_wh_data(self, color_yellow):
        for_wh_frame_attr = [[70 / 1080, 370 / 2220],
                             [1020 / 1080, 370 / 2220]]
        for_wh_frame_attr = [[el[0] * self.width, el[1] * self.height] for el in for_wh_frame_attr]
        frame_yellow_ending = [color_yellow for _ in for_wh_frame_attr]
        return [for_wh_frame_attr, frame_yellow_ending]

    def pixel_equals(self, px1, px2):
        # checking only RGB from ARGB
        return px1[1] == px2[1] and px1[2] == px2[2] and px1[3] == px2[3]

    def getFrameAttr(self, frame, attributes):
        attr_data = []
        for attr in attributes:
            attr_data.append(frame[int(attr[1] * self.width + attr[0])])
        return attr_data

    def check_screen_points_equal(self, frame, points_list, points_value):
        """
        Gets 2 lists of x,y coordinates where to get values and list of values to comapre.
        Returns true if current frame have those values
        :param points_list: a list of x,y coordinates (absolute, not normalized)
        :param points_value: a list (same size of points_list) with values for equals check (values are 4d)
        :return:
        """
        if len(points_list) != len(points_value):
            print("Wrong size between points and values!")
            return False
        attr_data = self.getFrameAttr(frame, points_list)
        for i in range(len(attr_data)):
            if not self.pixel_equals(attr_data[i], points_value[i]):
                return False
        return True

    def checkEndFrame(self):
        """
        Returns if we are on end frame
        :return:
        """
        frame = adb_screen_getpixels()
        return self.check_screen_points_equal(frame, self.end_data[0], self.end_data[1])

    def have_energy(self):
        """
        Returns True if have 5 or more energy left
        :return:
        """
        frame = adb_screen_getpixels()
        return self.check_screen_points_equal(frame, self.low_enegy_data[0], self.low_enegy_data[1])

    def onEquipMenu(self):
        """
        Returns True if have 5 or more energy left
        :return:
        """
        frame = adb_screen_getpixels()
        return self.check_screen_points_equal(frame, self.equip_data[0], self.equip_data[1])

    def checkLevelEnded(self):
        """
        Return True if level up screen reached
        :return:
        """
        frame = adb_screen_getpixels()
        lvl_up = self.check_screen_points_equal(frame, self.lvl_up_data[0], self.lvl_up_data[1])
        fortune_wheel = self.check_screen_points_equal(frame, self.fortune_wheel_data[0], self.fortune_wheel_data[1])
        devil_question = False
        mistery_vendor = False
        return lvl_up or fortune_wheel or devil_question or mistery_vendor
