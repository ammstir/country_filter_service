from .client import HttpClient
from .exceptions import NotFound, ResourceError

__all__ = ["HttpClient", "http_client", "NotFound", "ResourceError"]

http_client = HttpClient()
