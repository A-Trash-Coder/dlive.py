class DLivePyException(BaseException):
    pass

class ConnectionError(DLivePyException):
    pass

class HttpException(DLivePyException):
    pass