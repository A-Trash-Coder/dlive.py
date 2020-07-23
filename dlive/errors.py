class DLivePyException(BaseException):
    pass

class ConnectionError(DLivePyException):
    pass

class HttpException(DLivePyException):
    pass

class NotFound(DLivePyException):
    pass

class Forbidden(DLivePyException):
    pass