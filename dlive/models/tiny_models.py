from ..enums import TreasureChestState


class Wallet:
    """Represents a users wallet.

    Attributes
    ----------
    balance: int
        Amount in the wallet
    total_earnings: int
        Total amount of what the user has earned
    """

    def __init__(self, data):
        self.balance: int = data["balance"]
        self.total_earnings = data["totalEarning"]


class Language:
    """Represents a DLive language used for streams.

    Attributes
    ----------
    code: :class:`str`
        The language ISO code
    name: :class:`str`
        The name of the language
    """

    def __init__(self, data):
        self.code = data["code"]
        self.name = data["language"]

    def __str__(self) -> str:
        return self.name


class Category:
    """Represents a DLive stream category.

    Attributes
    ----------
    title: :class:`str`
        The name of the category
    image_url: :class:`str`
        The categories cover art
    cover_image_url: :class:`str`
        Categoriess banner art
    """

    def __init__(self, data):
        self.title = data["title"]
        self.image_url = data["imgUrl"]
        self.cover_image_url = data["coverImgUrl"]

    def __str__(self) -> str:
        return self.title


class TreasureChest:
    """Represents a chats Treasure Chest.

    Attributes
    ----------
    value: :class:`int`
        The value of the chest
    state: :class:`dlive.enums.TreasureChestState`
        The state of the chest
    """

    def __init__(self, data):
        self.value = data["value"]
        self.state = TreasureChestState[data["state"].lower()]