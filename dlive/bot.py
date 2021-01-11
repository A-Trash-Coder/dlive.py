import asyncio
import inspect
import traceback
from typing import Union

from .command import Command
from .errors import CommandError
from .http import HTTPSession
from .stringparser import StringParser
from .websocket import WebsocketConnection


class Bot:
    """DLive Bot for interacting with the wss and API.

    Parameters
    -----------
    command_prefix: Union[class:`list`, class:`tuple`, :class:`str`]
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
        self._aliases = {}
        self.http = HTTPSession(self.loop, self)

    async def get_user(self, username):
        """Returns a user based on the given username.

        Parameters
        -----------
        username: :class:`str`
            The user's unique name.

        Returns
        -------
        Optional[:class:`~dlive.models.User`]
            The user or ``None`` if not found.
        """
        return await self.http.get_user(username)

    async def get_chat(self, username):
        """Returns a chat based on the given name (Owner's username).

        Parameters
        ----------
        username: :class:`str`
            The chats unique name (Owner's username)

        Returns
        -------
        Optional[:class:`~dlive.models.Chat`]
            The chat or ``None`` if not found.
        """
        return await self.http.get_chat(username)

    def run(self, token=""):
        """Main blocking call that starts the bot.

        Parameters
        ----------
        token: Optional[:class:`str`]
            The authorization token used to make authorized requests
        """
        try:
            self.token = token
            loop = self.loop or asyncio.get_event_loop()

            loop.run_until_complete(self._ws._connect())
            loop.run_until_complete(self._ws._websocket_listen())
        except KeyboardInterrupt:
            pass
        finally:
            self._ws.teardown()

    def set_prefix(self, command_prefix):
        """Sets the bots prefix.

        Parameters
        ----------
        command_prefix: Union[:class:`str`, :class:`list`, :class:`tuple`]
            The prefix(es) to set as the bots prefix
        """
        if isinstance(command_prefix, (tuple, list)):
            return list(command_prefix)
        
        if isinstance(command_prefix, str):
            return [command_prefix]

    def listener(self, coroutine):
        """Adds a listener to the bot, that is called
        when a specific event occurs.

        Parameters
        ----------
        coroutine: 
            coroutine

        Raises
        ------
        TypeError:
            The function is not a coroutine
        """
        if not inspect.iscoroutinefunction(coroutine):
            raise TypeError("Listeners must be coroutines.")

        setattr(self, coroutine.__name__, coroutine)
        
        return coroutine

    def add_command(self, command):
        """Adds a command.

        Parameters
        ----------
        command: :class:`~dlive.Command`
            The command to add

        Raises
        ------
        TypeError: 
            A :class:`~dlive.Command` instance was not passed
        CommandError:
            The function was not a coroutine or a command with the name already exists
        """
        if not isinstance(command, Command):
            raise TypeError("A dlive.Command must be passed.")
        elif command.name in self.commands:
            raise CommandError(
                f"{command.name} could not be registered due to a command with that name already existing.")
        elif not inspect.iscoroutinefunction(command._callback):
            raise CommandError(
                f"{command.name} could not be registered due to its function not being a couroutine.")

        self.commands[command.name] = command

        if not command.aliases:
            return

        for alias in command.aliases:
            if alias in self.commands:
                del self.commands[command.name]
                raise CommandError(
                    f"Failed to load command <{command.name}>, a command with that name/alias already exists.")

            self._aliases[alias] = command.name

    def remove_command(self, command):
        """Removes a command.

        Parameters
        ----------
        command: :class:`~dlive.Command`
            The command to remove
        """
        if command.aliases:
            for a in command.aliases:
                self._aliases.pop(a)

        try:
            del self.commands[command.name]
        except KeyError:
            pass

    async def error(self):
        """Default error handler."""
        traceback.print_exc()

    async def command_error(self, message, error):
        """Default command error handler.

        Parameters
        ----------
        message: :class:`~dlive.models.Message`
            The message context which was used to invoke the command

        error: Exception
            The cause of the error
        """
        traceback.print_exc()

    async def message(self, message):
        """Called when a message is recieved in the websocket.

        Parameters
        ----------
        message: :class:`~dlive.models.Message`
            The message context which was sent
        """
        await self.handle_commands(message)

    async def handle_commands(self, message):
        """Handles a message and determines whether its a command,
        then calls it id needed.

        Parameters
        ----------
        message: :class:`~dlive.models.Message`
            The message context which was sent

        Raises
        ------
        CommandError: 
            The command was not registered
        """
        prefix_used = None
        for pre in self.command_prefix:
            if message.content.startswith(pre):
                prefix_used = pre
                break

        if prefix_used is None:
            return

        message.content = message.content.strip(prefix_used)
        parsed = StringParser().process_string(message.content)

        try:
            command = parsed.pop(0)
        except KeyError:
            return

        try:
            command = self._aliases[command]
        except KeyError:
            pass

        try:
            if command in self.commands:
                command = self.commands[command]
            elif command:
                raise CommandError(f"{command} is not a registered command.")
            else:
                return
        except Exception as error:
            return await self.command_error(message, error)

        message.command = command
        instance = command.instance

        try:
            message.args, message.kwargs = await command.parse_args(instance, parsed)

            if message.command._before_invoke:
                await message.command._before_invoke(instance, message)

            if instance:
                await message.command._callback(instance, message, *message.args, **message.kwargs)
            else:
                await message.command._callback(message, *message.args, **message.kwargs)
        except Exception as error:
            if message.command.on_error:
                await message.command.on_error(instance, message, error)

            await self.command_error(message, error)

        try:
            if command._after_invoke:
                await message.command._after_invoke(message)
        except Exception as error:
            await self.command_error(message, error)

    def command(self, *, name: str = None, aliases: Union[list, tuple] = None, cls=None):
        """Decorator that turns a coroutine into a Command.

        Parameters
        ----------
        name: :class:`str`
            Name of the command. Determines how the command 
            will be invoked. I.e. <prefix><name>
        aliases: Union[:class:`list`, :class:`tuple`]
            Other known names of the command
        """
        if cls and not inspect.isclass(cls):
            raise TypeError(f"cls must be of type <class> not <{type(cls)}>")

        cls = cls or Command

        def decorator(func):
            fname = name or func.__name__
            command = cls(name=fname, func=func, aliases=aliases)

            return self.add_command(command)
        
        return decorator