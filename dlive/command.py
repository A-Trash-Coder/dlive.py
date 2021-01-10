import inspect

from .errors import *


class Command:
    def __init__(self, name: str, func, **attrs):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("Command callback must be a coroutine.")

        self.name = name
        self._callback = func
        self._checks = []

        try:
            self._checks.extend(func.__checks__)
        except AttributeError:
            pass

        sig = inspect.signature(func)

        self.aliases = attrs.get("aliases", None)
        self.params = sig.parameters.copy()
        self.on_error = None
        self._before_invoke = None
        self._after_invoke = None
        self.instance = None

        for key, value in self.params.items():
            if isinstance(value.annotation, str):
                self.params[key] = value.replace(
                    annotation=eval(value.annotation, func.__globals__))

    async def _convert_types(self, param, parsed):
        converter = param.annotation
        if converter is param.empty:
            if param.default in (param.empty, None):
                converter = str
            else:
                converter = type(param.default)

        try:
            argument = converter(parsed)
        except Exception:
            raise BadArgument(f"Invalid argument parsed at `{param.name}` in command `{self.name}`."
                              f" Expected type {converter} got {type(parsed)}.")

        return argument

    async def parse_args(self, instance, parsed):
        iterator = iter(self.params.items())
        index = 0
        args = []
        kwargs = {}

        try:
            next(iterator)
            if instance:
                next(iterator)
        except StopIteration:
            raise CommandError("Message is a argument that is required")

        for _, param in iterator:
            index += 1
            if param.kind == param.POSITIONAL_OR_KEYWORD:
                try:
                    argument = parsed.pop(index)
                except (KeyError, IndexError):
                    if param.default is param.empty:
                        raise MissingRequiredArgument(param)
                    args.append(param.default)
                else:
                    argument = await self._convert_types(param, argument)
                    args.append(argument)

            elif param.kind == param.KEYWORD_ONLY:
                rest = " ".join(parsed.values())
                if rest.startswith(" "):
                    rest = rest.lstrip(" ")

                if rest:
                    rest = await self._convert_types(param, rest)
                elif param.default is param.empty:
                    raise MissingRequiredArgument(param)
                else:
                    rest = param.default

                kwargs[param.name] = rest
                parsed.clear()
                break

            elif param.VAR_POSITIONAL:
                args.extend(parsed.values())
                break

        if parsed:
            pass

        return args, kwargs

    def error(self, func):
        """Decorator that registers a function as an error handler."""
        if not inspect.iscoroutinefunction(func):
            raise CommandError("Command error handler must be a coroutine.")

        self.on_error = func

        return func

    def before_invoke(self, func):
        """Decorator that registers a function as something to be called
        before a command is ran.
        """
        if not inspect.iscoroutinefunction(func):
            raise CommandError("Before invoke func must be a coroutine")

        self._before_invoke = func

        return func

    def after_invoke(self, func):
        """Decorator that registers a function as something to be called
        after a command is ran.
        """
        if not inspect.iscoroutinefunction(func):
            raise CommandError("After invoke func must be a coroutine.")

        self._after_invoke = func

        return func