import json

__all__ = ["MockResponse"]


class MockResponse:
    def __init__(self, data, status):
        self.data = json.dumps(data)
        self.status = status

    async def json(self):
        return json.loads(self.data)

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
