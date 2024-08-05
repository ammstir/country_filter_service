import aiohttp
import ssl
from typing import Any
from src.http_client.exceptions import NotFound, ResourceError

__all__ = ["HttpClient"]


class HttpClient:
    session: aiohttp.ClientSession | None = None

    async def start(self) -> None:
        if self.session is None:
            self.session = aiohttp.ClientSession()

    def _get_ssl_context(self) -> ssl.SSLContext:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        return ssl_context

    async def stop(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()
        self.session = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    async def get(self, url: str) -> Any:
        async with self.session.get(url, ssl=self._get_ssl_context()) as resp:
            if not (200 <= resp.status < 300):
                if resp.status == 404 or resp.status == 400:
                    raise NotFound
                else:
                    raise ResourceError
            data = await resp.json()
            return data
