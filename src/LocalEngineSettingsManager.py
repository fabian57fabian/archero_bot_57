import os
import logging
import json
from json import JSONEncoder
from src.Utils import loadJsonData, writeToFile, saveJsonObject
from src.BotStrategies import HealingStrategy, EnergyStrategy, VIPSub, BattlepassAdvSub, ReviveIfDead


class LocalEngineSettings:
    def __init__(self):
        self.selected_dungeon = 6
        self.healing_strategy = HealingStrategy.SmartHeal
        self.energy_strategy = EnergyStrategy.AlwaysIgnore
        self.vip_sub = VIPSub.FalseVIP
        self.bpadv_sub = BattlepassAdvSub.FalseBPAdv
        self.revive_ifdead = ReviveIfDead.FalseRevive
        self.threshold_abilities = 5


class _LocalSettEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class LocalEngineSettingsManager:
    def __init__(self, settings_path: str):
        self.current_settings_path = settings_path
        self.encoder = _LocalSettEncoder()

    def save(self, settings: LocalEngineSettings) -> bool:
        js = self.encoder.encode(settings)
        s_dict = json.loads(js)
        saveJsonObject(self.current_settings_path, s_dict)
        return False

    def load(self) -> LocalEngineSettings:
        logging.log(logging.DEBUG - 5, "Loading Local Settings")

        # Create basic settings
        if not os.path.exists(self.current_settings_path):
            logging.debug("Creating basic local settings...")
            settings = LocalEngineSettings()
            self.save(settings)
            return settings

        # Try loading Manually with json parsing
        try:
            new_sett = loadJsonData(self.current_settings_path)
            settings = self._json_settings_to_object(new_sett)
        except Exception as e:
            logging.error(f"Unable to load existing {self.current_settings_path}: {str(e)}. setting to default.")
            settings = LocalEngineSettings()
            self.save(settings)
        return settings

    def _json_settings_to_object(self, new_sett: dict) -> LocalEngineSettings:
        def load_if_not_create(s: dict, key: str, default):
            if key in s:
                return s[key]
            else:
                logging.warning(f"Current local settings have no '{key}'. Setting to default {default}")
                return default

        loc_sett = LocalEngineSettings()
        loc_sett.selected_dungeon = int(load_if_not_create(new_sett, "selected_dungeon", 3))
        loc_sett.healing_strategy = HealingStrategy(
            load_if_not_create(new_sett, "healing_strategy", HealingStrategy.SmartHeal))
        loc_sett.energy_strategy = EnergyStrategy(
            load_if_not_create(new_sett, "energy_strategy", EnergyStrategy.AlwaysIgnore))
        loc_sett.vip_sub = VIPSub(load_if_not_create(new_sett, "vip_sub", VIPSub.FalseVIP))
        loc_sett.bpadv_sub = BattlepassAdvSub(load_if_not_create(new_sett, "bpadv_sub", BattlepassAdvSub.FalseBPAdv))
        loc_sett.revive_ifdead = ReviveIfDead(load_if_not_create(new_sett, "revive_ifdead", ReviveIfDead.FalseRevive))
        loc_sett.threshold_abilities = int(load_if_not_create(new_sett, "threshold_abilities", 5))
        return loc_sett
