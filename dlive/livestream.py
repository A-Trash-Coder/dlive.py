import datetime
from . import tiny_models

class Livestream:
    def __init__(self, data):
        self.is_nsfw: bool= data["ageRestriction"]
        self.thumbnail_url = data["thumbnailUrl"]
        self.gift_alert_disabled: bool = data["disableAlert"]
        self.title = data["title"]
        self.created_at = datetime.datetime.utcfromtimestamp(int(data["createdAt"][:-3]))
        self.dontation_amount_recieved: int = data["totalReward"]
        self.current_viewers: int = data["watchingCount"]
        self.language = tiny_models.Language(data["language"])
        self.category = tiny_models.Category(data["category"])
        self.views: int = data["view"]