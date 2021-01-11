import datetime

from ..enums import BanStatus, PartnerStatus
from . import tiny_models


class User:
    """Represents a user registered on DLive

    Attributes
    ----------
    username: :class:`str`
        The users unique username
    displayname: :class:`str`
        The users display name, most
        likely the username with a capitalization
        differences
    avatar_url: :class:`str`
        Url to the users avatar image
    partner_status: :class:`dlive.enums.PartnerStatus`
        The status of their DLive partnership
    created_at: :class:`datetime`
        When the users account was created
    wallet: :class:`models.tiny_model.Wallet`
        The users wallet
    is_subscribeable: :class:`bool`
        Whether the user can be subscribed to
    ban_status: :class:`dlive.enums.BanStatus`
        The users ban status
    is_deactivated: :class:`bool`
        Whether the users account is deactivated
    offline_image: :class:`str`
        The users offline cover art
    mention: :class:`str`
        The users name in mention form
    is_verified_partner: :class:`bool`
        Whether the user is a verified partner
    is_global_partner: :class:`bool`
        Whether the user is a global partner
    is_affliate: :class:`bool`
        Whether the user is an affliate
    is_global_partner_suspended: :class:`bool`
        Whether the users global partner is a suspended status
    is_account_suspended: :class:`bool`
        Whether the users account is suspended
    is_stream_banned: :class:`bool`
        Whether the person is banned from streaming
    """

    def __init__(self, data):
        self.username = data["username"]
        self.displayname = data["displayname"]
        self.avatar_url = data["avatar"]
        self.partner_status = PartnerStatus[data["partnerStatus"].lower()]
        self.created_at = datetime.datetime.utcfromtimestamp(
            int(data["createdAt"][:-3]))
        self.wallet = tiny_models.Wallet(data["wallet"])
        self.is_subscribeable: bool = data["canSubscribe"]
        self.ban_status = BanStatus[data["banStatus"].lower()]
        self.is_deactivated: bool = data["deactivated"]
        self.offline_image = data["offlineImage"]

    def __str__(self):
        return self.displayname

    def __eq__(self, other_user):
        return isinstance(other_user, User) and other_user.username == self.username

    def __ne__(self, other_user):
        return not self.__eq__(other_user)

    @property
    def mention(self) -> str:
        """A string formatted to mention a user."""
        return f"@{self.displayname}"

    @property
    def is_verified_partner(self) -> bool:
        """Whether the user is a verified partner on DLive."""
        return self.partner_status == PartnerStatus.verified_partner

    @property
    def is_global_partner(self) -> bool:
        """Whether the user is a global partner on DLive."""
        return self.partner_status == PartnerStatus.global_partner

    @property
    def is_affiliate(self) -> bool:
        """Whether the user is a DLive affiliate."""
        return self.partner_status == PartnerStatus.affiliate

    @property
    def is_global_partner_suspended(self) -> bool:
        """Whether the user's global partner status is suspended."""
        return self.partner_status == PartnerStatus.global_partner_suspended

    @property
    def is_account_suspended(self) -> bool:
        """Whether the user's account is suspended."""
        return self.ban_status == BanStatus.account_suspended

    @property
    def is_stream_banned(self) -> bool:
        """Whether the user is banned from streaming."""
        return self.ban_status == BanStatus.ban_from_streaming