class AuthError(Exception):
    pass

class HTTPError(Exception):
    pass

class InvalidTypeError(Exception):
    pass

class InvalidVersionError(Exception):
    pass

class MethodNotSupported(Exception):
    pass

class RateLimitError(Exception):
    pass

class ClientClosedError(Exception):
    pass
