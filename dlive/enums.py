from enum import Enum


class PartnerStatus(Enum):
    none = 1
    verified_partner = 2
    global_partner = 3
    global_partner_suspended = 4
    affiliate = 5


class ChatMode(Enum):
    default = 1
    subonly = 2
    followonly = 3


class BanStatus(Enum):
    no_ban = 1
    ban_from_streaming = 2
    account_suspended = 3


class TreasureChestState(Enum):
    collecting = 1
    claiming = 2