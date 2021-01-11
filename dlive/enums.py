from enum import Enum


class PartnerStatus(Enum):
    """
    A :class:`~dlive.models.User`'s Partner Status.

    Attributes
    ----------
    none:
        The user is not verified.
    verified_partner:
        The user is a verified partner.
    global_partner:
        The user is a global partner.
    global_partner_suspended:
        The user's global partner status is suspended.
    affiliate:
        The user is an affiliate.
    """
    none = 1
    verified_partner = 2
    global_partner = 3
    global_partner_suspended = 4
    affiliate = 5


class ChatMode(Enum):
    """
    A :class:`~dlive.models.Chat`'s mode.

    Attributes
    ----------
    default:
        Anyone may talk in chat.
    subonly:
        Only channel subs may talk in chat.
    followonly:
        Only channel followers may talk in chat.
    """
    default = 1
    subonly = 2
    followonly = 3


class BanStatus(Enum):
    """
    A :class:`~dlive.models.User`'s ban status.

    Attributes
    ----------
    no_ban:
        The user is not banned.
    ban_from_streaming:
        The user is banned from streaming.
    account_suspended:
        The user is banned.
    """
    no_ban = 1
    ban_from_streaming = 2
    account_suspended = 3


class TreasureChestState(Enum):
    """
    A :class:`~dlive.models.Chat`'s treasure chest's state.

    Attributes
    ----------
    collecting:
        The streamer is collection for their chest.
    claiming:
        The channel users are collecting chest rewards.
    """
    collecting = 1
    claiming = 2