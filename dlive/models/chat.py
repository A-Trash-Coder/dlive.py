from ..enums import ChatMode
from .livestream import Livestream
from .tiny_models import TreasureChest
from .user import User


class Chat:
    """Represents a DLive chat room.

    Attributes
    ----------
    name: :class:`str`
        The chats name (Owner's name)
    about: str
        The chats description
    livestream: :class:`~dlive.models.Livestream` [Optional]
        Returns a Livestream object which 
        gives information on the current livestream
        or None if one is not occuring
    livestream_hosting: Optional[:class:`~dlive.Livestream`]
        Returns a Livestream object which 
        gives information on the current 
        livestream the user is hosting or
        None if one is not occuring
    followers: :class:`int`
        The total amount of followers the chat has
    chat_mode: :class:`~dlive.enums.ChatMode`
        The type of chat mode the chat is in
    chat_interval: :class:`int`
        The interval in which users can speak
    treasure_chest: :class:`~dlive.enums.TreasureChest~
        Treasue Chest object containing details
        about it, the amount, etc.
    owner: :class:`~dlive.models.User`
        The owner of a chat
    """

    def __init__(self, bot, data, name):
        self.name = name.lower()
        self.about = data["about"]
        self.livestream = Livestream(
            data["livestream"]) if data["livestream"] is not None else None
        self.livestream_hosting = Livestream(
            data["hostingLivestream"]) if data["hostingLivestream"] is not None else None
        self.followers: int = data["followers"]["totalCount"]
        self.chat_mode = ChatMode[data["chatMode"].lower()]
        self.chat_interval: int = data["chatInterval"]
        self.treasure_chest = TreasureChest(data=data["treasureChest"])
        self._bot = bot

    def __str__(self):
        return self.name

    def __eq__(self, other_chat):
        return isinstance(other_chat, Chat) and other_chat.name == self.name

    def __ne__(self, other_chat):
        return not self.__eq__(other_chat)

    async def owner(self) -> User:
        """Returns the owner of a chat.

        Returns
        -------
        :class:`~dlive.models.User`
        """
        return await self._bot.get_user(self.name)

    async def send(self, content):
        """Sends a message to a DLive chat.

        Parameters
        ----------
        content: :class:`str`
            What to send to the chat
        """
        await self._bot.http.send_message(self, content)

    async def add_moderator(self, user: User):
        """Adds someone as a chat moderator.

        Parameters
        ----------
        user: :class:`~dlive.User`
            The user to make a moderator
        """
        await self._bot.http.add_moderator(self, user)

    async def remove_moderator(self, user: User):
        """Removes someone as a chat moderator.

        Parameters
        ----------
        user: :class:`~dlive.models.User`
            The user to remove as a moderator
        """
        await self._bot.http.remove_moderator(self, user)

    async def ban(self, user: User):
        """Bans someone from the chat.

        Parameters
        ----------
        user: :class:`~dlive.models.User`
            The user to ban
        """
        await self._bot.http.ban_user(self, user)

    async def unban(self, user: User):
        """Un-Bans someone from the chat.

        Parameters
        ----------
        user: :class:`~dlive.models.User`
            The user to un-ban
        """
        await self._bot.http.unban_user(self, user)

    async def set_chat_interval(self, seconds: int):
        """Sets the chat interval.

        Parameters
        ----------
        seconds: :class:`int`
            The amount of seconds to set the chat
            interval to
        """
        await self._bot.http.set_chat_interval(self, seconds)

    async def add_filter_word(self, word):
        """Adds a word to filter in chat.

        Parameters
        ----------
        word: :class:`str`
            The word to add
        """
        await self._bot.http.add_filter_word(self, word)

    async def delete_filter_word(self, word):
        """Deletes a word from the chat filter list.

        Parameters
        ----------
        word: :class:`str`
            The word to remove
        """
        await self._bot.http.delete_filter_word(self, word)

    async def ban_emote(self, emote):
        """Bans an emote in chat.

        Parameters
        ----------
        emote: :class:`str`
            The emote to ban
        """
        await self._bot.http.ban_emote(self, emote)

    async def unban_emote(self, emote):
        """Un-Bans an emote in chat.

        Parameters
        ----------
        emote: :class:`str`
            The emote to un-ban
        """
        await self._bot.http.unban_emote(self, emote)

    async def timeout_user(self, user: User, duration: int):
        """Times out a user for a specified duration.

        Parameters
        ----------
        user: :class:`~dlive.models.User`
            The user to timeout
        duration: :class:`int`
            The amount of minutes to timeout the user
        """
        await self._bot.http.timeout_user(self, user, duration)

    async def untimeout_user(self, user: User):
        """Un-Times out a user.

        Parameters
        ----------
        user: :class:`~dlive.models.User`
            The user to un-timeout
        """
        await self._bot.http.timeout_user(self, user, 0)