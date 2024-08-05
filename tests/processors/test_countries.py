import json
from pathlib import Path

import pytest
from sqlalchemy import insert, select

from src.http_client.client import NotFound, ResourceError
from src.models import IsoCountries
from src.processors.countries import (
    CountryProcessor,
    InvalidIsoCodeError,
    IsoSourceError,
)

pytestmark = [pytest.mark.asyncio(scope="session")]


@pytest.fixture
def processor(http_client, db_fixture):
    return CountryProcessor(http_client, db_fixture)


def get_response_data():
    file_path = Path(__file__).parent / "data/resp_example.json"

    with file_path.open("r") as f:
        return json.loads(f.read())


async def test_fetch_countries_by_iso(processor, http_client_mock):
    http_client_mock.return_value = get_response_data()

    result = await processor.fetch_country_names_by_iso("svk")

    assert result == {
        "republik slovak",
        "sk",
        "slovak republic",
        "slovakia",
        "slovakian tasavalta",
        "slovensko",
        "slovenská republika",
        "slowakei",
        "slowakische republik",
    }


async def test_fetches_data_from_db(processor, http_client_mock, db_fixture):
    query = insert(IsoCountries).values(iso_code="svk", names=["Country1", "Country2"])
    await db_fixture.execute(query)

    result = await processor.fetch_country_names_by_iso("svk")

    http_client_mock.assert_not_awaited()
    assert result == {"Country1", "Country2"}


async def test_calls_client_if_nothing_found_in_db(
    processor, http_client_mock, db_fixture
):
    query = insert(IsoCountries).values(iso_code="rus", names=["Country1", "Country2"])
    await db_fixture.execute(query)

    http_client_mock.return_value = get_response_data()

    await processor.fetch_country_names_by_iso("svk")

    http_client_mock.assert_called_once_with("https://restcountries.com/v3.1/alpha/svk")


async def test_saves_received_info_in_db(processor, http_client_mock, db_fixture):
    query = insert(IsoCountries).values(iso_code="rus", names=["Country1", "Country2"])
    await db_fixture.execute(query)

    http_client_mock.return_value = get_response_data()

    await processor.fetch_country_names_by_iso("svk")

    db_info = await db_fixture.fetch_all(
        select(IsoCountries.iso_code, IsoCountries.names).order_by(
            IsoCountries.created_at.desc()
        )
    )
    rows = [dict(iso_code=r["iso_code"], names=sorted(r["names"])) for r in db_info]
    assert rows == [
        {
            "iso_code": "svk",
            "names": [
                "republik slovak",
                "sk",
                "slovak republic",
                "slovakia",
                "slovakian tasavalta",
                "slovensko",
                "slovenská republika",
                "slowakei",
                "slowakische republik",
            ],
        },
        {"iso_code": "rus", "names": ["Country1", "Country2"]},
    ]


async def test_raises_if_cannot_fetch_info(processor, http_client_mock):
    http_client_mock.side_effect = ResourceError

    with pytest.raises(IsoSourceError):
        await processor.fetch_country_names_by_iso("svk")


async def test_raises_if_no_match_for_iso(processor, http_client_mock):
    http_client_mock.side_effect = NotFound

    with pytest.raises(InvalidIsoCodeError):
        await processor.fetch_country_names_by_iso("svk")
