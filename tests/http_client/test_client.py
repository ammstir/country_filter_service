import pytest
from tests.helpers import MockResponse
from src.http_client import NotFound, ResourceError
from unittest.mock import patch, ANY
from aiohttp import ClientSession

pytestmark = [pytest.mark.asyncio]


@pytest.fixture
def http_mock(http_client):
    with patch.object(ClientSession, "get") as mock:
        yield mock


async def test_get_calls_as_expected(http_client, http_mock):
    http_mock.return_value = MockResponse(status=200, data={})

    await http_client.get("https://example.com")

    http_mock.assert_called_with("https://example.com", ssl=ANY)


@pytest.mark.parametrize("status_code", [200, 201])
async def test_get_returns_responce_content(http_client, http_mock, status_code):
    http_mock.return_value = MockResponse(status=status_code, data={"some": "data"})

    result = await http_client.get("https://example.com")

    assert result == {"some": "data"}


@pytest.mark.parametrize(
    "status_code, expected_error",
    [(400, NotFound), (404, NotFound), (500, ResourceError)],
)
async def test_get_raises_on_error(http_client, http_mock, status_code, expected_error):
    http_mock.return_value = MockResponse(status=status_code, data={})

    with pytest.raises(expected_error):
        await http_client.get("https://example.com")
