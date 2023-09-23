import enum


class HealingStrategy(str, enum.Enum):
    AlwaysHeal = "always_heal"
    AlwaysPowerUp = "always_power"
    SmartHeal = "smart_heal"


class EnergyStrategy(str, enum.Enum):
    AlwaysBuy = "always_buy"
    AlwaysBuy2 = "always_buy2"
    AlwaysBuy3 = "always_buy3"
    AlwaysBuy4 = "always_buy4"
    AlwaysIgnore = "always_ignore"


class VIPSub(str, enum.Enum):
    TrueVIP = "vip_true"
    FalseVIP = "vip_false"


class BattlepassAdvSub(str, enum.Enum):
    TrueBPAdv = "bpadv_true"
    FalseBPAdv = "bpadv_false"


class ReviveIfDead(str, enum.Enum):
    TrueRevive = "revive_true"
    FalseRevive = "revive_false"
