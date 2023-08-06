class HTTPError(Exception):
    pass

class InvalidTypeError(Exception):
    pass

class RateLimitError(Exception):
    pass

class ClientClosedError(Exception):
    pass
