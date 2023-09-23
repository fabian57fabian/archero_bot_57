import logging
import enum


class ChapterLevelType(enum.Enum):
    T50 = "pattern_50"
    T40 = "pattern_40"
    T30 = "pattern_30"
    T20 = "pattern_20"
    T21 = "pattern_21" # Ch18 is a special snowflake
    T10 = "pattern_10"


class DungeonLevelType(enum.Enum):
    Intro = 'Intro'
    Normal = 'Normal'
    Heal = 'Heal'
    Boss = 'Boss'
    FinalBoss = 'Final_B'


class ChapterInfo(object):
    def __init__(self, name, type):
        self.name=name
        self.type=type


def BuildChapters() ->dict:
    chapters_info = {
        "1": ChapterInfo("Verdant Prairie", ChapterLevelType.T50),
        "2": ChapterInfo("Storm Desert", ChapterLevelType.T50),
        "3": ChapterInfo("Abandoned Dungeon", ChapterLevelType.T20),
        "4": ChapterInfo("Crystal Mines", ChapterLevelType.T50),
        "5": ChapterInfo("Lost Castle", ChapterLevelType.T50),
        "6": ChapterInfo("Cave of Bones", ChapterLevelType.T20),
        "7": ChapterInfo("Barens of Shadow", ChapterLevelType.T10),
        "8": ChapterInfo("Silent Expanse", ChapterLevelType.T50),
        "9": ChapterInfo("Frozen Pinnacle", ChapterLevelType.T50),
        "10": ChapterInfo("Land of Doom", ChapterLevelType.T20),
        "11": ChapterInfo("The Capital", ChapterLevelType.T50),
        "12": ChapterInfo("Dungeon of Traps", ChapterLevelType.T30),
        "13": ChapterInfo("Lava Land", ChapterLevelType.T50),
        "14": ChapterInfo("Frigid Tundra", ChapterLevelType.T10),
        "15": ChapterInfo("Pharaoh's Chamber", ChapterLevelType.T30),
        "16": ChapterInfo("Archaic Temple", ChapterLevelType.T20),
        "17": ChapterInfo("Dragon Lair", ChapterLevelType.T30),
        "18": ChapterInfo("Escape Chamber", ChapterLevelType.T21),
        "19": ChapterInfo("Devil's Tavern", ChapterLevelType.T50),
        "20": ChapterInfo("Palace of Light", ChapterLevelType.T20),
        "21": ChapterInfo("Nightmare Land", ChapterLevelType.T10),
        "22": ChapterInfo("Tranquil Forest", ChapterLevelType.T30),
        "23": ChapterInfo("Underwater Ruins", ChapterLevelType.T50),
        "24": ChapterInfo("Silent Wilderness", ChapterLevelType.T20),
        "25": ChapterInfo("Death Bar", ChapterLevelType.T50),
        "26": ChapterInfo("Land of the Dead", ChapterLevelType.T30),
        "27": ChapterInfo("Sky Castle", ChapterLevelType.T30),
        "28": ChapterInfo("Sandy Town", ChapterLevelType.T10),
        "29": ChapterInfo("dark forest", ChapterLevelType.T50),
        "30": ChapterInfo("Shattered Abyss", ChapterLevelType.T40),
        "31": ChapterInfo("Underwater City", ChapterLevelType.T20),
        "32": ChapterInfo("Evil Castle", ChapterLevelType.T10),
        "33": ChapterInfo("Aeon Temple", ChapterLevelType.T40),
        "34": ChapterInfo("Sakura Court", ChapterLevelType.T30),
        "35": ChapterInfo("Serene Town", ChapterLevelType.T10),
        "36": ChapterInfo("Evil Void", ChapterLevelType.T50),
        "37": ChapterInfo("Cloud City", ChapterLevelType.T40),
        "38": ChapterInfo("Climbing Temple", ChapterLevelType.T30),
        "39": ChapterInfo("Frozen Lands", ChapterLevelType.T20),
        "40": ChapterInfo("Eerie Castle", ChapterLevelType.T50),
        "41": ChapterInfo("Autumn Countyard", ChapterLevelType.T40),
        "42": ChapterInfo("Fairlytale Halmet", ChapterLevelType.T10)
    }
    return chapters_info


def BuildLevelsTypes() -> dict:

    levels_type_50 = { # 50 levels pattern
        0: DungeonLevelType.Intro,
        1: DungeonLevelType.Normal,
        2: DungeonLevelType.Normal,
        3: DungeonLevelType.Normal,
        4: DungeonLevelType.Normal,
        5: DungeonLevelType.Heal,
        6: DungeonLevelType.Normal,
        7: DungeonLevelType.Normal,
        8: DungeonLevelType.Normal,
        9: DungeonLevelType.Normal,
        10: DungeonLevelType.Boss,
        11: DungeonLevelType.Normal,
        12: DungeonLevelType.Normal,
        13: DungeonLevelType.Normal,
        14: DungeonLevelType.Normal,
        15: DungeonLevelType.Heal,
        16: DungeonLevelType.Normal,
        17: DungeonLevelType.Normal,
        18: DungeonLevelType.Normal,
        19: DungeonLevelType.Normal,
        20: DungeonLevelType.Boss,
        21: DungeonLevelType.Normal,
        22: DungeonLevelType.Normal,
        23: DungeonLevelType.Normal,
        24: DungeonLevelType.Normal,
        25: DungeonLevelType.Heal,
        26: DungeonLevelType.Normal,
        27: DungeonLevelType.Normal,
        28: DungeonLevelType.Normal,
        29: DungeonLevelType.Normal,
        30: DungeonLevelType.Boss,
        31: DungeonLevelType.Normal,
        32: DungeonLevelType.Normal,
        33: DungeonLevelType.Normal,
        34: DungeonLevelType.Normal,
        35: DungeonLevelType.Heal,
        36: DungeonLevelType.Normal,
        37: DungeonLevelType.Normal,
        38: DungeonLevelType.Normal,
        39: DungeonLevelType.Normal,
        40: DungeonLevelType.Boss,
        41: DungeonLevelType.Normal,
        42: DungeonLevelType.Normal,
        43: DungeonLevelType.Normal,
        44: DungeonLevelType.Normal,
        45: DungeonLevelType.Heal,
        46: DungeonLevelType.Normal,
        47: DungeonLevelType.Normal,
        48: DungeonLevelType.Normal,
        49: DungeonLevelType.Normal,
        50: DungeonLevelType.FinalBoss,
    }

    levels_type_40 = { # 40 levels pattern
        0: DungeonLevelType.Intro,
        1: DungeonLevelType.Normal,
        2: DungeonLevelType.Normal,
        3: DungeonLevelType.Normal,
        4: DungeonLevelType.Normal,
        5: DungeonLevelType.Heal,
        6: DungeonLevelType.Normal,
        7: DungeonLevelType.Normal,
        8: DungeonLevelType.Normal,
        9: DungeonLevelType.Normal,
        10: DungeonLevelType.Boss,
        11: DungeonLevelType.Normal,
        12: DungeonLevelType.Normal,
        13: DungeonLevelType.Normal,
        14: DungeonLevelType.Normal,
        15: DungeonLevelType.Heal,
        16: DungeonLevelType.Normal,
        17: DungeonLevelType.Normal,
        18: DungeonLevelType.Normal,
        19: DungeonLevelType.Normal,
        20: DungeonLevelType.Boss,
        21: DungeonLevelType.Normal,
        22: DungeonLevelType.Normal,
        23: DungeonLevelType.Normal,
        24: DungeonLevelType.Normal,
        25: DungeonLevelType.Heal,
        26: DungeonLevelType.Normal,
        27: DungeonLevelType.Normal,
        28: DungeonLevelType.Normal,
        29: DungeonLevelType.Normal,
        30: DungeonLevelType.Boss,
        31: DungeonLevelType.Normal,
        32: DungeonLevelType.Normal,
        33: DungeonLevelType.Normal,
        34: DungeonLevelType.Normal,
        35: DungeonLevelType.Heal,
        36: DungeonLevelType.Normal,
        37: DungeonLevelType.Normal,
        38: DungeonLevelType.Normal,
        39: DungeonLevelType.Normal,
        40: DungeonLevelType.FinalBoss,
    }

    levels_type_30 = { # 30 levels pattern
        0: DungeonLevelType.Intro,
        1: DungeonLevelType.Normal,
        2: DungeonLevelType.Normal,
        3: DungeonLevelType.Normal,
        4: DungeonLevelType.Normal,
        5: DungeonLevelType.Heal,
        6: DungeonLevelType.Normal,
        7: DungeonLevelType.Normal,
        8: DungeonLevelType.Normal,
        9: DungeonLevelType.Normal,
        10: DungeonLevelType.Boss,
        11: DungeonLevelType.Normal,
        12: DungeonLevelType.Normal,
        13: DungeonLevelType.Normal,
        14: DungeonLevelType.Normal,
        15: DungeonLevelType.Heal,
        16: DungeonLevelType.Normal,
        17: DungeonLevelType.Normal,
        18: DungeonLevelType.Normal,
        19: DungeonLevelType.Normal,
        20: DungeonLevelType.Boss,
        21: DungeonLevelType.Normal,
        22: DungeonLevelType.Normal,
        23: DungeonLevelType.Normal,
        24: DungeonLevelType.Normal,
        25: DungeonLevelType.Heal,
        26: DungeonLevelType.Normal,
        27: DungeonLevelType.Normal,
        28: DungeonLevelType.Normal,
        29: DungeonLevelType.Normal,
        30: DungeonLevelType.FinalBoss,
    }

    levels_type_21 = { # 20 levels pattern-2; Ch18 is a special snowflake
        0: DungeonLevelType.Intro,
        1: DungeonLevelType.Normal,
        2: DungeonLevelType.Heal,
        3: DungeonLevelType.Normal,
        4: DungeonLevelType.Heal,
        5: DungeonLevelType.Boss,
        6: DungeonLevelType.Normal,
        7: DungeonLevelType.Heal,
        8: DungeonLevelType.Normal,
        9: DungeonLevelType.Heal,
        10: DungeonLevelType.Boss,
        11: DungeonLevelType.Normal,
        12: DungeonLevelType.Normal,
        13: DungeonLevelType.Normal,
        14: DungeonLevelType.Heal,
        15: DungeonLevelType.Boss,
        16: DungeonLevelType.Normal,
        17: DungeonLevelType.Normal,
        18: DungeonLevelType.Normal,
        19: DungeonLevelType.Heal,
        20: DungeonLevelType.FinalBoss,
    }

    levels_type_20 = { # 20 levels pattern
        0: DungeonLevelType.Intro,
        1: DungeonLevelType.Normal,
        2: DungeonLevelType.Heal,
        3: DungeonLevelType.Normal,
        4: DungeonLevelType.Heal,
        5: DungeonLevelType.Boss,
        6: DungeonLevelType.Normal,
        7: DungeonLevelType.Heal,
        8: DungeonLevelType.Normal,
        9: DungeonLevelType.Heal,
        10: DungeonLevelType.Boss,
        11: DungeonLevelType.Normal,
        12: DungeonLevelType.Heal,
        13: DungeonLevelType.Normal,
        14: DungeonLevelType.Heal,
        15: DungeonLevelType.Boss,
        16: DungeonLevelType.Normal,
        17: DungeonLevelType.Heal,
        18: DungeonLevelType.Normal,
        19: DungeonLevelType.Heal,
        20: DungeonLevelType.FinalBoss,
    }

    levels_type_10 = { # 10 levels pattern
        0: DungeonLevelType.Intro,
        1: DungeonLevelType.Boss,
        2: DungeonLevelType.Boss,
        3: DungeonLevelType.Boss,
        4: DungeonLevelType.Boss,
        5: DungeonLevelType.Boss,
        6: DungeonLevelType.Boss,
        7: DungeonLevelType.Boss,
        8: DungeonLevelType.Boss,
        9: DungeonLevelType.Boss,
        10: DungeonLevelType.FinalBoss,
    }

    return {
        ChapterLevelType.T50: levels_type_50,
        ChapterLevelType.T40: levels_type_40,
        ChapterLevelType.T30: levels_type_30,
        ChapterLevelType.T21: levels_type_21,
        ChapterLevelType.T20: levels_type_20,
        ChapterLevelType.T10: levels_type_10,
    }


def MaxLevelFromType(ch_lvl_tp:ChapterLevelType) -> int:
    if ch_lvl_tp == ChapterLevelType.T50:
        return 50
    elif ch_lvl_tp == ChapterLevelType.T40:
        return 40
    elif ch_lvl_tp == ChapterLevelType.T30:
        return 30
    elif ch_lvl_tp == ChapterLevelType.T21:
        return 20
    elif ch_lvl_tp == ChapterLevelType.T20:
        return 20
    elif ch_lvl_tp == ChapterLevelType.T10:
        return 10
    else:
        logging.error("UNABLE TO SET THIS CHAPTER LENGTH")
        return 0
