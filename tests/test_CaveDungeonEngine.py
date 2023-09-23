import logging
import os
import shutil
import json
from unittest import TestCase
from src.CaveDungeonEngine import CaveEngine
from src.UsbConnector import UsbConnector
from src.Utils import initialize_logging

class TestCaveEngine(TestCase):

    def setUp(self) -> None:
        initialize_logging(logging.DEBUG - 5)

        if os.path.exists("datas"): shutil.rmtree("datas")
        os.mkdir("datas")
        os.mkdir("datas/abilities")

        with open('datas/abilities/tier_list.json', 'w') as file:
            file.write(json.dumps({"multishot": 1,"front_arrow_1": 2}))

        dev_conn = UsbConnector(connect_now=False)
        self.engine = CaveEngine(dev_conn, "datas")

    def tearDown(self) -> None:
        self.engine.setStopRequested()

    def test_change_current_level(self):
        new_level = 8
        self.level_signal_arrived = False
        def on_level_changed(level_arrived):
            assert new_level == level_arrived, "Level changed differently"
            self.level_signal_arrived = True

        self.engine.levelChanged.connect(on_level_changed)
        self.engine.changeCurrentLevel(new_level)
        assert new_level == self.engine.currentLevel, "Level not changed"
        assert self.level_signal_arrived, "Signal for level change not arrived"

