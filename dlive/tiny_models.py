from .enums import TreasureChestState

class Wallet:
    def __init__(self, data):
        """Represents a users wallet

        Attributes
        ----------
        balance: int
            Amount in the wallet
        total_earnings: int
            Total amount of what the user has earned
        """
        self.balance: int = data["balance"]
        self.total_earnings = data["totalEarning"]

class Language:
    """Represents a DLive language used for streams

    Attributes
    ----------
    code: str
        The language ISO code
    name: str
        The name of the language
    """
    def __init__(self, data):
        self.code = data["code"]
        self.name = data["language"]

    def __str__(self):
        return self.name

class Category:
    """Represents a DLive stream category
    
    Attributes
    ----------
    title: str
        The name of the category
    image_url: str
        The categories cover art
    cover_imaage_url: str
        Categoriess banner art
    """
    def __init__(self, data):
        self.title = data["title"]
        self.image_url = data["imgUrl"]
        self.cover_image_url = data["coverImgUrl"]
    
    def __str__(self):
        return self.title
        
class TreasureChest:
    def __init__(self, data):
        """Represents a chats Treasure Chest

        Attributes
        ----------
        value: int
            The value of the chest
        state: dlive.TreasureChestState
            The state of the chest
        """
        self.value = data["value"]
        self.state = TreasureChestState[data["state"].lower()]