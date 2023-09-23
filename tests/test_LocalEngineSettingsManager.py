import os
import json
import logging
from unittest import TestCase

from src.LocalEngineSettingsManager import LocalEngineSettingsManager, LocalEngineSettings
from src.BotStrategies import HealingStrategy, EnergyStrategy, VIPSub,BattlepassAdvSub,ReviveIfDead


class TestLocalEngineSettingsManager(TestCase):
    def setUp(self) -> None:
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

        self.settings_file = "test1_1_1.json"
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
        self.settings_1 = {
            "selected_dungeon": 3,
            "healing_strategy": "smart_heal",
            "energy_strategy": "always_ignore",
            "vip_sub": "vip_false",
            "bpadv_sub": "bpadv_false",
            "revive_ifdead": "revive_false",
            "threshold_abilities": 5}
        with open(self.settings_file, 'w') as file:
            file.write(json.dumps(self.settings_1))
        self.man = LocalEngineSettingsManager(self.settings_file)

        self.settings_file2 = "test1_1_2.json"
        if os.path.exists(self.settings_file2):
            os.remove(self.settings_file2)
        self.man2 = LocalEngineSettingsManager(self.settings_file2)

    def tearDown(self) -> None:
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
        if os.path.exists(self.settings_file2):
            os.remove(self.settings_file2)

    def test_save(self):
        s = LocalEngineSettings()
        self.man.save(s)
        assert os.path.exists(self.settings_file)

        with open(self.settings_file, 'r') as file:
            new_s = json.load(file)
        assert s.selected_dungeon == new_s["selected_dungeon"]
        assert s.threshold_abilities == new_s["threshold_abilities"]
        assert HealingStrategy(s.healing_strategy) == new_s["healing_strategy"]
        assert EnergyStrategy(s.energy_strategy) == new_s["energy_strategy"]
        assert VIPSub(s.vip_sub) == new_s["vip_sub"]
        assert BattlepassAdvSub(s.bpadv_sub) == new_s["bpadv_sub"]
        assert ReviveIfDead(s.revive_ifdead) == new_s["revive_ifdead"]

    def test_load(self):
        s = self.man.load()
        new_s= self.settings_1
        assert s.selected_dungeon == new_s["selected_dungeon"]
        assert s.threshold_abilities == new_s["threshold_abilities"]
        assert HealingStrategy(s.healing_strategy) == new_s["healing_strategy"]
        assert EnergyStrategy(s.energy_strategy) == new_s["energy_strategy"]
        assert VIPSub(s.vip_sub) == new_s["vip_sub"]
        assert BattlepassAdvSub(s.bpadv_sub) == new_s["bpadv_sub"]
        assert ReviveIfDead(s.revive_ifdead) == new_s["revive_ifdead"]

    def test_load_nofile(self):
        s = self.man2.load()
        assert os.path.exists(self.settings_file2)

        with open(self.settings_file2, 'r') as file:
            new_s = json.load(file)
        assert s.selected_dungeon == new_s["selected_dungeon"]
        assert s.threshold_abilities == new_s["threshold_abilities"]
        assert HealingStrategy(s.healing_strategy) == new_s["healing_strategy"]
        assert EnergyStrategy(s.energy_strategy) == new_s["energy_strategy"]
        assert VIPSub(s.vip_sub) == new_s["vip_sub"]
        assert BattlepassAdvSub(s.bpadv_sub) == new_s["bpadv_sub"]
        assert ReviveIfDead(s.revive_ifdead) == new_s["revive_ifdead"]

