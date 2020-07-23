from .enums import PartnerStatus, Ban
from . import tiny_models
import datetime

class User:
    def __init__(self, data):
        self.username = data["username"]
        self.displayname = data["displayname"]
        self.avatar_url = data["avatar"]
        self.partner_status = PartnerStatus[data["partnerStatus"].lower()]
        self.created_at = datetime.datetime.utcfromtimestamp(int(data["createdAt"][:-3]))
        self.wallet = tiny_models.Wallet(data["wallet"])
        self.is_subscribeable: bool = data["canSubscribe"]
        self.ban_status = Ban[data["banStatus"].lower()]
        self.is_deactivated: bool = data["deactivated"]
        self.offline_image = data["offlineImage"]

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
        return self.ban_status == Ban.account_suspended

    @property
    def is_stream_banned(self):
        return self.ban_status == Ban.ban_from_streaming