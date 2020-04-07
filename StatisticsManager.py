import os
import csv
from datetime import datetime
import time


class StatisticsManager(object):

    def __init__(self):
        self.file_path = "datas/statistics.csv"
        self.dateFormat = "%d%m%Y_%H%M%S"
        if not os.path.exists(self.file_path):
            self._write(self.getHeader())

    def getHeader(self):
        return ["Time start", "Time end", "Level start", "Level End", "duration", ]

    def saveOneGame(self, start_date, lvl_start, lvl_end):
        end_date = datetime.now()
        self._write([start_date.strftime(self.dateFormat), end_date.strftime(self.dateFormat), lvl_start, lvl_end,
                     (end_date - start_date).total_seconds()])

    def _write(self, data: list):
        try:
            with open(self.file_path, 'a+', newline='') as write_obj:
                csv_writer = csv.writer(write_obj)
                csv_writer.writerow(data)
            return True
        except Exception as e:
            print("Errors writing statistics: %s" % str(e))
            return False

    def _readAll(self) -> list:
        try:
            datas = []
            columns = len(self.getHeader())
            header = self.getHeader()
            with open(self.file_path, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                # if len(header) != columns: print("Warning: Header different that file header")
                for row in csv_reader:
                    line = [
                        datetime.strptime(row[header[0]], self.dateFormat),
                        datetime.strptime(row[header[1]], self.dateFormat),
                        int(row[header[2]]),
                        int(row[header[3]]),
                        float(row[header[4]])
                    ]
                    datas.append(line)
            return datas
        except Exception as e:
            print("Errors reading statistics: %s" % str(e))
            return []
