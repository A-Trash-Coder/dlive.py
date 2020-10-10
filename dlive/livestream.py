import datetime

from . import tiny_models


class Livestream:
    """Represents a occuring DLive Livestream

    Attributes
    ----------
    is_nsfw: bool
        Whether it is age restricted
    thumbnail_url: str
        The streams thumbnail url
    gift_alert_disabled: bool
        Whether gift alerts are disabled in the channel
    title: str
        The streams title
    created_at: datetime
        When the stream started
    donation_amount_recieved: int
        Total amount of donations recieved during the current sstream
    current_viewers: int
        Current amount of viewers watching
    language: str
        The language the stream is in
    category: str
        The streams categorized sanction
    views: int
        Total amount of view the livestream recieved
    """

    def __init__(self, data):
        self.is_x_tagged: bool = data["ageRestriction"]
        self.thumbnail_url = data["thumbnailUrl"]
        self.gift_alert_disabled: bool = data["disableAlert"]
        self.title = data["title"]
        self.created_at = datetime.datetime.utcfromtimestamp(
            int(data["createdAt"][:-3]))
        self.dontation_amount_recieved: int = data["totalReward"]
        self.current_viewers: int = data["watchingCount"]
        self.language = tiny_models.Language(data["language"])
        self.category = tiny_models.Category(data["category"])
        self.views: int = data["view"]

    def __str__(self):
        return self.title