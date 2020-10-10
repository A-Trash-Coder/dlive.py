import aiohttp

from .chat import Chat
from .errors import HttpException
from .message import Message
from .user import User


class HTTPSession:
    BASE = 'https://api.twitch.tv/helix'

    def __init__(self, loop, bot):
        self._bot = bot
        self._session = aiohttp.ClientSession(loop=loop)
        self.BASE = "https://graphigo.prd.dlive.tv/"

    async def _request(self, json, method="POST", headers={}):
        async with self._session.request(url=self.BASE, method=method, json=json, headers=headers) as response:
            response_json = await response.json()
            try:
                return response_json["data"]
            except KeyError:
                if response.status == 422:
                    raise HttpException(
                        f"Status code: {response.status} | {response_json['errors'][0]['message']}")

    async def get_user(self, username):
        query = {"query": "query{userByDisplayName(displayname: \"user_var\"){username displayname avatar partnerStatus createdAt wallet{balance totalEarning} canSubscribe banStatus deactivated offlineImage}}".replace(
            "user_var", username)}
        user_json = await self._request(json=query)
        if user_json["userByDisplayName"] is None:
            return None
        return User(data=user_json["userByDisplayName"])

    async def get_chat(self, username):
        query = {"query": "query{userByDisplayName(displayname: \"user_var\"){treasureChest{value state} chatInterval chatMode followers{totalCount} hostingLivestream{id permlink ageRestriction thumbnailUrl disableAlert title createdAt totalReward watchingCount language{code language} category{title imgUrl coverImgUrl} view} livestream{id permlink ageRestriction thumbnailUrl disableAlert title createdAt totalReward watchingCount language{code language} category{title imgUrl coverImgUrl} view} about}}".replace("user_var", username)}
        chat_json = await self._request(json=query)
        if chat_json["userByDisplayName"] is None:
            return None
        return Chat(bot=self._bot, data=chat_json["userByDisplayName"], name=username)

    async def send_message(self, chat: Chat, content):
        streamer = await chat.owner()
        json = {"operationName": "SendStreamChatMessage", "variables": {"input": {"streamer": streamer.username, "message": content, "roomRole": "Member", "subscribing": True,
                                                                                  "emojis": []}}, "extensions": {"persistedQuery": {"version": 1, "sha256Hash": "848cbe91a57458ed402716e7b57b7a128c3b5a8385a6ebe14d9deff8d1eda73c"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def add_moderator(self, chat: Chat, user: User):
        json = {"operationName": "AddModerator", "variables": {"username": f"{user.username}", "streamer": f"{chat.name}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "062727612e825ec7e8307b176f7a60fb71bb205eb4cd432020af9c476362471f"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def remove_moderator(self, chat: Chat, user: User):
        json = {"operationName": "RemoveModerator", "variables": {"username": f"{user.username}", "streamer": f"{chat.name}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "6ab7beae3484aede4fc88a2052908ada86474fcabc6f29b7859b71443753b0da"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def message_delete(self, chat: Chat, message: Message):
        json = {"operationName": "DeleteChat", "variables": {"streamer": f"{chat.name}", "id": f"{message.id}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "7ae6f96161b89d9831dcf217f11f67c1edf5bb311d8819101345ed8eb38f6ed9"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def ban_user(self, chat: Chat, user: User):
        json = {"operationName": "BanStreamChatUser", "variables": {"streamer": f"{chat.name}", "username": f"{user.username}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "4eaeb20cba25dddc95df6f2acf8018b09a4a699cde468d1e8075d99bb00bacc4"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def unban_user(self, chat: Chat, user: User):
        json = {"operationName": "UnbanStreamChatUser", "variables": {"streamer": f"{chat.name}", "username": f"{user.username}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "574e9a8db47ff719844359964d6108320e4d35f0378d7f983651d87b315d4008"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def set_chat_interval(self, chat: Chat, seconds: int):
        json = {"operationName": "SetChatInterval", "variables": {"streamer": f"{chat.name}", "seconds": seconds}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "353fa9498a47532deb97680ea72647cba960ab1a90bda4cdf78da7b2d4d3e4b0"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def add_filter_word(self, chat: Chat, word):
        json = {"operationName": "AddFilterWord", "variables": {"streamer": f"{chat.name}", "word": f"{word}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "569b22423f4c76fa26a07f9870774e8074642824b460fd2c48000afeddc674e5"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def delete_filter_word(self, chat: Chat, word):
        json = {"operationName": "DeleteFilterWord", "variables": {"streamer": f"{chat.name}", "word": f"{word}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "c20ecdc121e8f97bc10dba4c6734c34c20d5e54a419c2fb1cd09637017e4b3f9"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def ban_emote(self, chat: Chat, emote):
        json = {"operationName": "EmoteBan", "variables": {"emoteStr": f"{emote}", "streamer": f"{chat.name}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "ba0c6a172eb57160fc681d477e65015275103ec023b60299943203ea75384fa8"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def unban_emote(self, chat: Chat, emote):
        json = {"operationName": "EmoteUnban", "variables": {"emoteStr": f"{emote}", "streamer": f"{chat.name}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "0f979b4572a803fa47aab50681cb0e9f79724dd78db1c10ac2cc0b169573c201"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def timeout_user(self, chat: Chat, user: User, duration: int):
        json = {"operationName": "UserTimeoutSet", "variables": {"streamer": f"{chat.name}", "username": f"{user.username}", "duration": duration},
                "extensions": {"persistedQuery": {"version": 1, "sha256Hash": "89453f238a70a36bedaa2cb24ef75d8bdef09506dc5b17ba471530ce4c73254b"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)

    async def delete_chat_message(self, chat: Chat, id):
        json = {"operationName": "DeleteChat", "variables": {"streamer": f"{chat.name}", "id": f"{id}"}, "extensions": {
            "persistedQuery": {"version": 1, "sha256Hash": "7ae6f96161b89d9831dcf217f11f67c1edf5bb311d8819101345ed8eb38f6ed9"}}}
        headers = {"Authorization": self._bot.token}
        await self._request(json=json, headers=headers)