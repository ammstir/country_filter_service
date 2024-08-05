from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.processors import (
    CountryProcessor,
    InvalidIsoCodeError,
    IsoSourceError,
)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def processor_mock():
    with patch.object(CountryProcessor, "fetch_country_names_by_iso") as processor_mock:
        yield processor_mock


def test_filter_countries(client, processor_mock):
    processor_mock.return_value = {
        "republik slovak",
        "sk",
        "slovak republic",
        "slovakia",
        "slovakian tasavalta",
        "slovensko",
        "slovenská republika",
        "slowakei",
        "slowakische republik",
        "slovaška",
        "szlovakia",
    }

    response = client.post(
        "/api/v1/match_country",
        json={
            "iso": "svk",
            "countries": [
                "iran",
                "Slowakei",
                "Vatikan",
                "Slovaška",
                "Szlovakia",
                "Belgrade",
                "España",
                "Nizozemsko",
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "iso": "svk",
        "match_count": 3,
        "matches": ["Slowakei", "Slovaška", "Szlovakia"],
    }


def test_returns_404_if_invalid_iso(client, processor_mock):
    processor_mock.side_effect = InvalidIsoCodeError

    response = client.post(
        "/api/v1/match_country",
        json={
            "iso": "svk",
            "countries": [
                "iran",
                "Slowakei",
                "Vatikan",
                "Slovaška",
                "Szlovakia",
                "Belgrade",
                "España",
                "Nizozemsko",
            ],
        },
    )

    assert response.status_code == 422
    assert response.json() == {"detail": {"error": "Invalid Iso Code"}}


def test_returns_empty_data_if_no_matches_found(client, processor_mock):
    processor_mock.side_effect = IsoSourceError

    response = client.post(
        "/api/v1/match_country",
        json={
            "iso": "svk",
            "countries": [
                "iran",
                "Slowakei",
                "Vatikan",
                "Slovaška",
                "Szlovakia",
                "Belgrade",
                "España",
                "Nizozemsko",
            ],
        },
    )

    assert response.status_code == 424
    assert response.json() == {
        "detail": {"error": "Failed to retrieve countries info."}
    }
