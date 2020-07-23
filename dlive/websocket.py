import json
import asyncio
import traceback
import sys
from .backoff import ExponentialBackoff
from . import errors
import websockets
from .message import Message

class WebsocketConnection:
    def __init__(self, bot, *, loop: asyncio.BaseEventLoop=None, **attrs):
        self._bot = bot
        self.loop = loop or asyncio.get_event_loop()
        self._host = "wss://graphigostream.prd.dlive.tv"
        self._websocket = None
        self._tearingdown = False

    @property
    def is_connected(self) -> bool:
        return self._websocket is not None and self._websocket.open

    async def _connect(self):
        try:
            self._websocket = await websockets.connect(self._host, timeout=30, subprotocols='graphql-ws')
        except Exception as e:
            raise errors.ConnectionError(e)

        if self.is_connected:
            self.loop.create_task(self._authenticate())

    async def _authenticate(self):
        await self._websocket.send(json.dumps({
            'type': 'connection_init',
            'payload': {},
        }))
        await self._join_stream_channels()

    async def _join_stream_channels(self):
        # TODO make sure the channel is found. If not, send an error, and log.warning()
        for channel in self._bot.channels:
            await self._websocket.send(json.dumps({
                'id': channel,
                'type': 'start',
                'payload': {
                    'variables': {
                        'streamer': f"{channel.lower()}"
                    },
                    'extensions': {},
                    'operationName': 'StreamMessageSubscription',
                    'query':
                        'subscription StreamMessageSubscription($streamer: String!) {\n  streamMessageReceived(streamer: $streamer) {\n    type\n    ... on ChatGift {\n      id\n      gift\n      amount\n      recentCount\n      expireDuration\n      ...VStreamChatSenderInfoFrag\n    }\n    ... on ChatLive {\n      type}\n    ...on ChatTimeout {\n      type\n      ...VStreamChatSenderInfoFrag\n    }\n    ... on ChatOffline {\n      type}\n    ... on ChatHost {\n      id\n      viewer\n      ...VStreamChatSenderInfoFrag\n    }\n    ... on ChatSubscription {\n      id\n      month\n      ...VStreamChatSenderInfoFrag\n    }\n    ... on ChatChangeMode {\n      mode\n    }\n    ... on ChatText {\n      id\n      content\n      ...VStreamChatSenderInfoFrag\n    }\n    ... on ChatFollow {\n      id\n      ...VStreamChatSenderInfoFrag\n    }\n    ... on ChatDelete {\n      ids\n    }\n    ... on ChatBan {\n      id\n      ...VStreamChatSenderInfoFrag\n    }\n    ... on ChatModerator {\n      id\n      ...VStreamChatSenderInfoFrag\n      add\n    }\n    ... on ChatEmoteAdd {\n      id\n      ...VStreamChatSenderInfoFrag\n      emote\n    }\n  }\n}\n\nfragment VStreamChatSenderInfoFrag on SenderInfo {\n  subscribing\n  role\n  roomRole\n  sender {\n    id\n    username\n    displayname\n    avatar\n    partnerStatus\n  }\n}\n'
                }
            }))
        await self._dispatch("ready")

    async def _dispatch(self, event: str, *args, **kwargs):
        try:
            coro = getattr(self._bot, f'{event}')
        except AttributeError:
            pass
        else:
            try:
                await coro(*args, **kwargs)
            except asyncio.CancelledError:
                pass

    async def error(self, error: Exception, data: str=None):
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def _websocket_listen(self):
        backoff = ExponentialBackoff()

        while True:
            try:
                data = json.loads(await self._websocket.recv())
            except websockets.ConnectionClosed:
                if self._tearingdown:
                    break
                retry = backoff.delay()
                await asyncio.sleep(retry)
                await self._connect()
                continue

            if data["type"] == "connection_error":
                raise errors.ConnectionError(data["payload"]["message"])
            
            await self._process_websocket_data(data)
            await self._dispatch('raw_data', data)

    async def _process_websocket_data(self, data):
        """Process data, check for ack, messages, etc. Remember if its a message to dispatch message"""
        if data['type'] == 'connection_ack':
            pass
        if data['type'] == 'ka':
            pass
        if data['type'] == 'data':
            if data["payload"]["data"]["streamMessageReceived"][0]["type"] == "Message":
                chat = await self._bot.get_chat(data["id"])
                author = await self._bot.get_user(data["payload"]["data"]["streamMessageReceived"][0]["sender"]["username"])
                return await self._dispatch('message', Message(bot=self._bot, data=data["payload"]["data"]["streamMessageReceived"][0], chat=chat, author=author))
            if data["payload"]["data"]["streamMessageReceived"][0]["type"] == "Live":
                chat = await self._bot.http.get_chat(data["id"])
                return await self._dispatch('stream_start', chat)
            if data["payload"]["data"]["streamMessageReceived"][0]["type"] == "Offline":
                chat = await self._bot.http.get_chat(data["id"])
                return await self._dispatch('stream_end', chat)
            if data["payload"]["data"]["streamMessageReceived"][0]["type"] == "Follow":
                user = await self._bot.get_user(data["payload"]["data"]["streamMessageReceived"][0]["sender"]["username"])
                chat = await self._bot.http.get_chat(data["id"])
                return await self._dispatch('follow', chat, user)
            if data["payload"]["data"]["streamMessageReceived"][0]["type"] == "Mod":
                user = await self._bot.get_user(data["payload"]["data"]["streamMessageReceived"][0]["sender"]["username"])
                chat = await self._bot.http.get_chat(data["id"])
                if data["payload"]["data"]["streamMessageReceived"][0]["roomRole"] == "Member":
                    return await self._dispatch('mod_remove', chat, user)
                if data["payload"]["data"]["streamMessageReceived"][0]["roomRole"] == "Moderator":
                    return await self._dispatch('mod_add', chat, user)
            if data["payload"]["data"]["streamMessageReceived"][0]["type"] == "Ban":
                user = await self._bot.get_user(data["payload"]["data"]["streamMessageReceived"][0]["sender"]["username"])
                chat = await self._bot.http.get_chat(data["id"])
                return await self._dispatch('ban', chat, user)
            if data["payload"]["data"]["streamMessageReceived"][0]["type"] == "Timeout":
                user = await self._bot.get_user(data["payload"]["data"]["streamMessageReceived"][0]["sender"]["username"])
                moderator = await self._bot.get_user(data["payload"]["data"]["streamMessageReceived"][0]["bannedBy"]["username"])
                chat = await self._bot.http.get_chat(data["id"])
                return await self._dispatch('user_timeout', chat, user, moderator, data["payload"]["data"]["streamMessageReceived"][0]["minute"])

        pass

    def teardown(self):
        self._tearingdown = True
        self.loop.run_until_complete(self.loop.create_task(self._websocket.close()))