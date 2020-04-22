from UsbConnector import UsbConnector
import os
from Utils import loadJsonData, saveJsonData_oneIndent, saveJsonData_twoIndent, buildDataFolder


class GameScreenConnector:
    def __init__(self, device_connector=None):
        self.debug = True
        self.device_connector = device_connector
        self.width = 0
        self.height = 0
        # This should be in format rgba
        self.coords_path = ''
        self.specific_checks_path = ''
        self.hor_lines_path = ''
        self.specific_checks_coords = {}
        self.static_coords = {}
        self.door_width = 180.0 / 1080.0
        self.yellow_experience = [255, 170, 16, 255]
        self.green_hp = [70,158,47, 255]
        self.green_hp_high = [84,180,58, 255]
        self.black_hp = [25, 25, 25, 255]
        # Line coordinates: x1,y1,x2,y2
        self.hor_lines = {}
        self.stopRequested = False

    def changeDeviceConnector(self, new_dev):
        self.device_connector = new_dev

    def changeScreenSize(self, w, h):
        self.width, self.height = w, h
        self.coords_path = os.path.join("datas", buildDataFolder(self.width, self.height), "coords",
                                        "static_coords.json")
        self.specific_checks_path = os.path.join("datas", buildDataFolder(self.width, self.height), "coords",
                                                 "static_specific_coords.json")
        self.hor_lines_path = os.path.join("datas", buildDataFolder(self.width, self.height), "coords",
                                           "hor_lines.json")

        self.specific_checks_coords = loadJsonData(self.specific_checks_path)
        self.static_coords = loadJsonData(self.coords_path)
        self.hor_lines = loadJsonData(self.hor_lines_path)

    def pixel_equals(self, px_readed, px_expected, around=5):
        arr = [5, 5, 5]
        if isinstance(around, int):
            arr = [around, around, around]
        elif isinstance(around, list):
            arr = [around[0], around[1], around[2]]
        # checking only RGB from RGBA
        return px_expected[0] - arr[0] <= px_readed[0] <= px_expected[0] + arr[0] \
               and px_expected[1] - arr[1] <= px_readed[1] <= px_expected[1] + arr[1] \
               and px_expected[2] - arr[2] <= px_readed[2] <= px_expected[2] + arr[2]

    def getFrameAttr(self, frame, attributes):
        attr_data = []
        for attr in attributes:
            x = int(attr[0] * self.width)
            y = int(attr[1] * self.height)
            attr_data.append(frame[int(y * self.width + x)])
        return attr_data

    def _check_screen_points_equal(self, frame, points_list, points_value, around=2):
        """
        Gets 2 lists of x,y coordinates where to get values and list of values to comapre.
        Returns true if current frame have those values
        :param points_list: a list of x,y coordinates (absolute, not normalized)
        :param points_value: a list (same size of points_list) with values for equals check (values are 4d)
        :param around: an integer for interval of search: +around and -around.
        :return:
        """
        if len(points_list) != len(points_value):
            print("Wrong size between points and values!")
            return False
        if self.debug: print("-----------------------------------")
        if self.debug: print("|   Smartphone   |     Values     |")
        attr_data = self.getFrameAttr(frame, points_list)
        equal = True
        for i in range(len(attr_data)):
            if self.debug: print("| %4d %4d %4d | %4d %4d %4d |" % (
                attr_data[i][0], attr_data[i][1], attr_data[i][2], points_value[i][0], points_value[i][1],
                points_value[i][2]))
            if not self.pixel_equals(attr_data[i], points_value[i], around=around):
                equal = False
        if self.debug: print("|-->         %s" % ("  equal           <--|" if equal else "not equal         <--|"))
        if self.debug: print("-----------------------------------")
        return equal

    def checkFrame(self, coords_name: str, frame=None):
        """
        Given a coordinates name it checkes if the Frame has those pixels.
        If no Frame given , it will take a screenshot.
        :return:
        """
        dict_to_take = []
        if coords_name in self.static_coords.keys():
            dict_to_take = self.static_coords
        elif coords_name in self.specific_checks_coords.keys():
            dict_to_take = self.specific_checks_coords
        else:
            print("No coordinates called %s is saved in memory! Returning false." % coords_name)
            return False
        if self.debug: print("Checking %s" % (coords_name))
        if frame is None:
            frame = self.getFrame()
        around = 2 if "around" not in dict_to_take[coords_name].keys() else dict_to_take[coords_name]["around"]
        is_equal = self._check_screen_points_equal(frame, dict_to_take[coords_name]["coordinates"],
                                                   dict_to_take[coords_name]["values"], around=around)
        return is_equal

    def getFrame(self):
        if self.stopRequested:
            exit()
        return self.device_connector.adb_screen_getpixels()

    def getFrameStateComplete(self, frame=None) -> dict:
        """
        Computes a complete check on given frame (takes a screen if none passed.
        Returns a dictionary with all known states with boolean value assigned.
        :return:
        """
        result = {}
        if frame is None:
            frame = self.getFrame()
        for k, v in self.static_coords.items():
            around = 2 if "around" not in self.static_coords[k].keys() else self.static_coords[k]["around"]
            if self.debug: print("Checking %s, around = %d" % (k, around))
            result[k] = self._check_screen_points_equal(frame, v["coordinates"], v["values"], around=around)
        return result

    def getFrameState(self, frame=None) -> str:
        """
        Computes a complete check on given frame (takes a screen if none passed.
        Returns a string with the name of current state, or unknown if no state found.
        :return:
        """
        state = "unknown"
        if frame is None:
            frame = self.getFrame()
        for k, v in self.static_coords.items():
            around = 2 if "around" not in self.static_coords[k].keys() else self.static_coords[k]["around"]
            if self.debug: print("Checking %s, around = %d" % (k, around))
            if self._check_screen_points_equal(frame, v["coordinates"], v["values"], around=around):
                state = k
                break
        return state

    def _getHorLine(self, hor_line, frame):
        """
        Returns a horizontal line (list of colors) given hor_line [x1, y1, x2, y2] coordinates. If no frame given, it takes a screen.
        :param hor_line:
        :param frame:
        :return:
        """
        x1, y1, x2, y2 = hor_line[0] * self.width, hor_line[1] * self.height, hor_line[2] * self.width, hor_line[
            3] * self.height
        if frame is None:
            frame = self.getFrame()
        start = int(y1 * self.width + x1)
        size = int(x2 - x1)
        line = frame[start:start + size]
        return line

    def getLineExpBar(self, frame=None):
        """
        Returns the colors of Experience bar as a line. If no frame given, it takes a screen.
        :param frame:
        :return:
        """
        line = self._getHorLine(self.hor_lines["hor_exp_bar"], frame)
        masked_yellow = []
        for px in line:
            if self.pixel_equals(px, self.yellow_experience, 3):
                masked_yellow.append(px)
            else:
                masked_yellow.append([0, 0, 0, 0])
        return masked_yellow

    def getPlayerDecentering(self) -> (int, str):
        line = self.getLineHpBar()
        first = 0
        last = 0
        for i, el in enumerate(line):
            if self.pixel_equals(self.green_hp, el, 2):
                if first == 0:
                    first = i
                last = i
        center_px = (last + first) / 2
        center_diff = int((self.width / 2) - center_px)
        if abs(center_diff) < self.door_width * self.width / 4.0:
            dir = "center"
        else:
            dir = "right" if center_diff < 0 else "left"
        print("Character on the %s side by %dpx" % (dir, abs(center_diff)))
        return center_diff, dir

    def getLineHpBar(self, frame=None):
        """
        Returns the colors of Experience bar as a line. If no frame given, it takes a screen.
        :param frame:
        :return:
        """
        line = self._getHorLine(self.hor_lines["hor_hp_bar"], frame)
        masked_green = []
        i = 0
        for px in line:
            i += 1
            if i == 452:
                a = 0
            if self.pixel_equals(px, self.green_hp, [8,12,8]) or self.pixel_equals(px, self.green_hp_high, [8,12,8]):
                masked_green.append(self.green_hp)
            else:
                masked_green.append([0, 0, 0, 0])
        #Filter outlayers:
        masked_green_no_outlayers=self.removeOutlayersInLine(masked_green, self.green_hp)
        return masked_green_no_outlayers

    def removeOutlayersInLine(self, masked_green, high_pixel_color):
        line = masked_green.copy()
        n = len(line)
        i = 0
        window_width = 10
        while i < n:
            if i in range(window_width): # First 4 take black. no problem losing them
                line[i] = [0, 0, 0, 0]
            else:
                if i > 370:
                    a = 3
                sum = 0
                for j in range(window_width):
                    sum += 1 if masked_green[i-j][0] == high_pixel_color[0] else 0
                for j in range(window_width):
                    line[i-j] = [0, 0, 0, 0] if sum <7 else high_pixel_color
                i += window_width-1 #Skip() and go to next window
            i += 1
        for i in range(window_width):  # Last 4 take black. no problem losing them
            line[n-i-1] = [0, 0, 0, 0]
        return line

    def getHorLine(self, line_name: str, frame=None):
        """
        Returns the colors of Experience bar as a line. If no frame given, it takes a screen.
        :param line_name: line x,y coordinates
        :param frame:
        :return:
        """
        if line_name not in self.hor_lines:
            print("Given line name '%s' is not a known horizontal line name." % line_name)
            return []
        return self._getHorLine(self.hor_lines[line_name], frame)

    def _checkBarHasChanged(self, old_line_hor_bar, current_exp_bar, around=0):
        if len(old_line_hor_bar) != len(current_exp_bar):
            min_len = min(len(old_line_hor_bar), len(current_exp_bar))
            old_line_hor_bar = old_line_hor_bar[:min_len]
            current_exp_bar = current_exp_bar[:min_len]
        changed = False
        for i in range(len(old_line_hor_bar)):
            if not self.pixel_equals(old_line_hor_bar[i], current_exp_bar[i], around=around):
                changed = True
                break
        return changed

    def checkExpBarHasChanged(self, old_line_hor_bar, frame=None):
        """
        Checks if old experience bar line is different that this one. If no frame given, it takes a screen.
        :param old_line_hor_bar:
        :param frame:
        :return:
        """
        if self.debug: print("Checking LineExpBar has changed")
        new_line = self.getLineExpBar(frame)
        return self._checkBarHasChanged(old_line_hor_bar, new_line, around=2)

    def checkUpperLineHasChanged(self, old_line, frame=None):
        """
        Checks if old upper line is different that this one. If no frame given, it takes a screen.
        :param old_line:
        :param frame:
        :return:
        """
        if self.debug: print("Checking LineUpper has changed")
        new_line = self.getHorLine("hor_up_line", frame)
        return self._checkBarHasChanged(old_line, new_line, around=10)
