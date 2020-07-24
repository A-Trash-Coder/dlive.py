from .enums import PartnerStatus, BanStatus
from . import tiny_models
import datetime

class User:
    """Represents a user registered on DLive

    Attributes
    ----------
    username: str
        The users unique username
    displayname: str
        The users display name, most
        likely the username with a capitalization
        differences
    avatar_url: str
        Url to the users avatar image
    partner_status: dlive.PartnerStatus
        The status of their DLive partnership
    created_at: datetime
        When the users account was created
    wallet: dlive.Wallet
        The users wallet
    is_subscribeable: bool
        Whether the user can be subscribed to
    ban_status: dlive.BanStatus
        The users ban status
    is_deactivated: bool
        Whether the users account is deactivated
    offline_image: str
        The users offline cover art
    mention: str
        The users name in mention form
    is_verified_partner: bool
        Whether the user is a verified partner
    is_global_partner: bool
        Whether the user is a global partner
    is_affliate: bool
        Whether the user is an affliate
    is_global_partner_suspended: bool
        Whether the users global partner is a suspended status
    is_account_suspended: bool
        Whether the users account is suspended
    is_stream_banned: bool
        Whether the person is banned from streaming
    """
    def __init__(self, data):
        self.username = data["username"]
        self.displayname = data["displayname"]
        self.avatar_url = data["avatar"]
        self.partner_status = PartnerStatus[data["partnerStatus"].lower()]
        self.created_at = datetime.datetime.utcfromtimestamp(int(data["createdAt"][:-3]))
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
    def mention(self):
        return f"@{self.displayname}"

    @property
    def is_verified_partner(self):
        return self.partner_status == PartnerStatus.verified_partner

    @property
    def is_global_partner(self):
        return self.partner_status == PartnerStatus.global_partner

    @property
    def is_affiliate(self):
        return self.partner_status == PartnerStatus.affiliate

    @property
    def is_global_partner_suspended(self):
        return self.partner_status == PartnerStatus.global_partner_suspended

    @property
    def is_account_suspended(self):
        return self.ban_status == BanStatus.account_suspended

    @property
    def is_stream_banned(self):
        return self.ban_status == BanStatus.ban_from_streaming