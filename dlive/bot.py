import sys
import traceback
from typing import Union
import asyncio
from .websocket import WebsocketConnection
import inspect
from .http import HTTPSession

class Bot:
    def __init__(self, command_prefix: Union[list, tuple, str], channels: list, loop: asyncio.BaseEventLoop=None):
        self.command_prefix = self.set_prefix(command_prefix)
        self.channels = channels
        self.loop = loop or asyncio.get_event_loop()
        self._ws = WebsocketConnection(bot=self, loop=self.loop)
        self.commands = {}
        self.http = HTTPSession(self.loop, self)

    async def get_user(self, username):
        return await self.http.get_user(username)

    async def get_chat(self, username):
        return await self.http.get_chat(username)

    def run(self, token):
        self.token = token
        loop = self.loop or asyncio.get_event_loop()

        loop.run_until_complete(self._ws._connect())

        try:
            loop.run_until_complete(self._ws._websocket_listen())
        except KeyboardInterrupt:
            pass
        finally:
            self._ws.teardown()

    def set_prefix(self, command_prefix):
        if isinstance(command_prefix, (tuple, list)):
            return list(command_prefix)
        if isinstance(command_prefix, str):
            return [command_prefix]

    def listener(self, func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError('Events must be coroutines.')

        setattr(self, func.__name__, func)
        return func

    async def ready(self):
        pass

    async def stream_start(self):
        pass

    async def stream_end(self):
        pass

    async def message(self, message):
        await self.handle_command(message)

    async def error(self, error, data=None):
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def raw_data(self, data):
        pass

    async def handle_command(self, message):
        prefix_used = None
        for pre in self.command_prefix:
            if message.content.startswith(pre):
                prefix_used = pre
                break

        if prefix_used is None:
            return