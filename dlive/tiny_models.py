from .enums import TreasureChestState

class Wallet:
    def __init__(self, data):
        self.balance: int = data["balance"]
        self.total_earnings = data["totalEarning"]

class Language:
    def __init__(self, data):
        self.code = data["code"]
        self.name = data["language"]

class Category:
    def __init__(self, data):
        self.title = data["title"]
        self.image_url = data["imgUrl"]
        self.cover_image_url = data["coverImgUrl"]
        
class TreasureChest:
    def __init__(self, data):
        self.value = data["value"]
        self.state = TreasureChestState[data["state"].lower()]

class StreamTemplateInput:
    def __init__(self, data):
        self.title = data["title"]
        self.age_restriction: bool = data["ageRestriction"]
        self.thumbanil_url = data["thumbnailUrl"]
        self.disable_alert: bool = data["disableAlert"]
        self.category_id: int = data["categoryID"]
        self.language_id: int = data["languageID"]