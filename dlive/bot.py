import asyncio
import inspect
import sys
import traceback
from typing import Union

from .http import HTTPSession
from .websocket import WebsocketConnection


class Bot:
    """DLive Bot for interacting with the wss and API

    Parameters
    ----------
    command_prefix: Union[list, tuple, str]
        The prefix for the bots commands
    channels: list
        The initial channels for the bot to connect to
    loop: asyncio.BaseEventLoop [Optional]
        The asyncio event loop to use
    """

    def __init__(self, command_prefix: Union[list, tuple, str], channels: list, loop: asyncio.BaseEventLoop = None):
        self.command_prefix = self.set_prefix(command_prefix)
        self.channels = channels
        self.loop = loop or asyncio.get_event_loop()
        self._ws = WebsocketConnection(bot=self, loop=self.loop)
        self.commands = {}
        self.http = HTTPSession(self.loop, self)

    async def get_user(self, username):
        """Returns a dlive.User based on the given
        username

        Parameters
        ----------
        username: str
            The users unique username
        """
        return await self.http.get_user(username)

    async def get_chat(self, username):
        """Returns a dlive.Chat based on the given
        name (Owner's username)

        Parameters
        ----------
        username: str
            The chats unique name (Owner's username)

        Returns
        -------
        Optional[dlive.Chat]
        """
        return await self.http.get_chat(username)

    def run(self, token):
        """Main blocking call that starts the bot

        Parameters
        ----------
        token: str
            The authorization token used to make requests
        """
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

    def listener(self, coroutine):
        """Adds a listener to the bot, that is called
        when a specific event occurs

        Raises
        ------
        TypeError:
            The function is not a coroutine

        Parameters
        ----------
        coroutine: coroutine
        """
        if not inspect.iscoroutinefunction(coroutine):
            raise TypeError('Bot listeners must be a coroutines function.')

        setattr(self, coroutine.__name__, coroutine)
        return coroutine

    async def error(self):
        """Default error handler
        """
        traceback.print_exc()

    async def handle_command(self, message):
        prefix_used = None
        for pre in self.command_prefix:
            if message.content.startswith(pre):
                prefix_used = pre
                break

        if prefix_used is None:
            return