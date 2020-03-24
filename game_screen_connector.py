import time
from adb_connector import *


class GameScreenConnector:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # This should be in format rgba
        self.end_data = [[[170 / 1080, 1230 / 2220], [890 / 1080, 1230 / 2220], [800 / 1080, 780 / 2220]],
                         self.repeat_as_list([48, 98, 199, 255], 3)]
        self.equip_data = [[[855 / 1080, 1576 / 2220]],
                           self.repeat_as_list([231, 191, 105, 255], 1)]
        self.low_enegy_data = [[[370 / 1080, 60 / 2220]],
                               self.repeat_as_list([53, 199, 41, 255], 1)]
        self.lvl_up_data = [[[70 / 1080, 530 / 2220], [1020 / 1080, 530 / 2220]],
                            self.repeat_as_list([255, 181, 0, 255], 2)]  # Yellow
        self.fortune_wheel_data = [[[70 / 1080, 370 / 2220], [1020 / 1080, 370 / 2220]],
                                   self.repeat_as_list([255, 181, 0, 255], 2)]  # Yellow
        self.devil_question_data = [[[70 / 1080, 370 / 2220], [1020 / 1080, 370 / 2220]],
                                    self.repeat_as_list([243, 38, 81, 255], 2)]  # Red
        self.mistery_vendor_data = [[[70 / 1080, 370 / 2220], [1020 / 1080, 370 / 2220]],
                                    self.repeat_as_list([255, 181, 0, 255], 2)]  # Yellow
        # Line coordinates: x1,y1,x2,y2
        self.lineHorExpBarCoordinates = [180 / 1080, 170 / 2220, 890 / 1080, 170 / 2220]

    def repeat_as_list(self, data, times=1):
        new_arr = []
        for i in range(times):
            new_arr.append(data)
        return new_arr

    def pixel_equals(self, px_readed, px_expected, around=0):
        # checking only RGB from RGBA
        return px_expected[0] - around <= px_readed[0] <= px_expected[0] + around \
               and px_expected[1] - around <= px_readed[1] <= px_expected[1] + around \
               and px_expected[2] - around <= px_readed[2] <= px_expected[2] + around

    def getFrameAttr(self, frame, attributes):
        attr_data = []
        for attr in attributes:
            x = int(attr[0] * self.width)
            y = int(attr[1] * self.height)
            attr_data.append(frame[int(y * self.width + x)])
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
            if not self.pixel_equals(attr_data[i], points_value[i], around=2):
                return False
        return True

    def checkEndFrame(self, frame=None):
        """
        Returns if we are on end frame
        :return:
        """
        if frame is None:
            frame = self.getFrame()
        return self.check_screen_points_equal(frame, self.end_data[0], self.end_data[1])

    def getFrame(self):
        return adb_screen_getpixels()

    def have_energy(self, frame=None):
        """
        Returns True if have 5 or more energy left. If no frame given, it takes a screen.
        :return:
        """
        if frame is None:
            frame = self.getFrame()
        return self.check_screen_points_equal(frame, self.low_enegy_data[0], self.low_enegy_data[1])

    def onEquipMenu(self, frame=None):
        """
        Returns True if have 5 or more energy left. If no frame given, it takes a screen.
        :return:
        """
        frame = self.getFrame()
        return self.check_screen_points_equal(frame, self.equip_data[0], self.equip_data[1])

    def checkLevelEnded(self, frame=None):
        """
        Return True if level up screen reached. If no frame given, it takes a screen.
        :return:
        """
        if frame is None:
            frame = self.getFrame()
        lvl_up = self.check_screen_points_equal(frame, self.lvl_up_data[0], self.lvl_up_data[1])
        fortune_wheel = self.check_screen_points_equal(frame, self.fortune_wheel_data[0], self.fortune_wheel_data[1])
        devil_question = self.check_screen_points_equal(frame, self.devil_question_data[0], self.devil_question_data[1])
        mistery_vendor = self.check_screen_points_equal(frame, self.mistery_vendor_data[0], self.mistery_vendor_data[1])
        return lvl_up or fortune_wheel or devil_question or mistery_vendor

    def getHorLine(self, hor_line, frame):
        """
        Returns a horizontal line (list of colors) given hor_line [x1, y1, x2, y2] coordinates. If no frame given, it takes a screen.
        :param hor_line:
        :param frame:
        :return:
        """
        x1, y1, x2, y2 = hor_line  # Those are normalized attributes in [0,1]
        if frame is None:
            frame = self.getFrame()
        start = int(round((y1 * self.height) * self.width, 0))
        size = int((round(x2 * self.width, 0) - round(x1 * self.width, 0)))
        return frame[start:start + size]

    def getLineExpBar(self, frame=None):
        """
        Returns the colors of Experience bar as a line. If no frame given, it takes a screen.
        :param frame:
        :return:
        """
        return self.getHorLine(self.lineHorExpBarCoordinates, frame)

    def checkExpBarHasChanged(self, old_line_hor_bar, frame=None):
        """
        Checks if old experience bar line is different that this one. If no frame given, it takes a screen.
        :param old_line_hor_bar:
        :param frame:
        :return:
        """
        current_exp_bar = self.getLineExpBar(frame)
        if len(old_line_hor_bar) != len(current_exp_bar):
            min_len = min(len(old_line_hor_bar), len(current_exp_bar))
            old_line_hor_bar = old_line_hor_bar[:min_len]
            current_exp_bar = current_exp_bar[:min_len]
        changed = False
        for i in range(len(old_line_hor_bar)):
            if not self.pixel_equals(old_line_hor_bar[i], current_exp_bar[i], around=2):
                changed = True
                break
        return changed
