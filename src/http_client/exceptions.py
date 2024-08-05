class HttpClientError(Exception):
    pass


class NotFound(HttpClientError):
    pass


class ResourceError(HttpClientError):
    pass
