import datetime

class Message:
    def __init__(self, bot, data, chat, author):
        self.chat = chat
        self._data = data
        self._bot = bot
        self.type = data["type"]
        self.id: int = data["id"]
        self.content = data["content"]
        self.created_at = datetime.datetime.utcfromtimestamp(int(data["createdAt"][:-9]))
        self.author = author
        
    async def delete(self):
        chat = await self._bot.get_chat(self._data["sender"]["username"])
        return await self._bot.http.delete_chat_message(chat, self.id)