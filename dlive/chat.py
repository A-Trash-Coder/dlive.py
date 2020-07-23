from os import name
from .enums import ChatMode
from .livestream import Livestream
from .user import User 
from .tiny_models import TreasureChest

class Chat:
    def __init__(self, bot, data, name):
        self.name = name.lower()
        self.about = data["about"]
        self.livestream = Livestream(data["livestream"]) if data["livestream"] is not None else None
        self.livestream_hosting = Livestream(data["hostingLivestream"]) if data["hostingLivestream"] is not None else None
        self.followers: int = data["followers"]["totalCount"]
        self.chat_mode = ChatMode[data["chatMode"].lower()]
        self.chat_interval: int = data["chatInterval"]
        self.treasure_chest = TreasureChest(data=data["treasureChest"])
        self._bot = bot

    async def send(self, content):
        await self._bot.http.send_message(self, content)

    async def add_moderator(self, user: User):
        await self._bot.http.add_moderator(self, user)

    async def remove_moderator(self, user: User):
        await self._bot.http.remove_moderator(self, user)

    async def ban(self, user: User): 
        await self._bot.http.ban_user(self, user)

    async def unban(self, user: User):
        await self._bot.http.unban_user(self, user)

    async def set_chat_interval(self, seconds: int):
        await self._bot.http.set_chat_interval(self, seconds)

    async def add_filter_word(self, word):
        await self._bot.http.add_filter_word(self, word)

    async def delete_filter_word(self, word):
        await self._bot.http.delete_filter_word(self, word)

    async def ban_emote(self, emote):
        await self._bot.http.ban_emote(self, emote)

    async def unban_emote(self, emote):
        await self._bot.http.unban_emote(self, emote)

    async def timeout_user(self, user: User, duration: int):
        await self._bot.http.timeout_user(self, user, duration)

    async def untimeout_user(self, user: User):
        await self._bot.http.timeout_user(self, user, 0)