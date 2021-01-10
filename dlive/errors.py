class DLivePyException(BaseException):
    pass


class ConnectionError(DLivePyException):
    pass


class HttpException(DLivePyException):
    pass


class Forbidden(DLivePyException):
    pass


class CommandError(DLivePyException):
    pass


class MissingRequiredArgument(DLivePyException):
    pass


class BadArgument(DLivePyException):
    pass


class RequiresAuthorization(DLivePyException):
    pass