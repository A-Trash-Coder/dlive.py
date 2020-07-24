import datetime

class Message:
    """Represents a message sent to a chat
    
    Attributes
    ----------
    chat: dlive.Chat
        The chat the message belongs to
    type: str
        The type of message sent
    id: str
        The id of the message
    content: str
        What the message contained
    created_at: datetime
        When the message was sent
    author: dlive.User
        Who sent the message
    """
    def __init__(self, bot, data, chat, author):
        self.chat = chat
        self._data = data
        self._bot = bot
        self.type = data["type"]
        self.id: int = data["id"]
        self.content = data["content"]
        self.created_at = datetime.datetime.utcfromtimestamp(int(data["createdAt"][:-9]))
        self.author = author

    def __str__(self):
        return self.content
        
    async def delete(self):
        """Deletes the message from the chat
        """
        chat = await self._bot.get_chat(self._data["sender"]["username"])
        return await self._bot.http.delete_chat_message(chat, self.id)