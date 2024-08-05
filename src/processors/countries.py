from src.http_client import HttpClient, NotFound, ResourceError
from src.processors.exceptions import InvalidIsoCodeError, IsoSourceError
from sqlalchemy import select, insert
from src.models import IsoCountries
from databases import Database

__all__ = ["CountryProcessor"]


class CountryProcessor:
    def __init__(self, client: HttpClient, db: Database):
        self.ISO_CHECK_URL = "https://restcountries.com/v3.1/alpha/"
        self.client = client
        self.db = db

    async def fetch_country_names_by_iso(self, iso_code: str) -> set[str]:
        country_names = await self.db.execute(
            select(IsoCountries.names).where(IsoCountries.iso_code == iso_code)
        )

        if country_names:
            return set(country_names)

        names = await self._fetch_country_names_by_url(iso_code)
        await self._save_country_names(iso_code, names)

        return names

    async def _fetch_country_names_by_url(self, iso: str) -> set[str]:
        country_names = set()

        try:
            country_data = await self.client.get(self.ISO_CHECK_URL + iso)
        except NotFound as e:
            raise InvalidIsoCodeError from e
        except ResourceError as e:
            raise IsoSourceError from e

        for data in country_data:
            native_name = data["name"]["nativeName"]
            for val in native_name.values():
                country_names.add(val["official"].lower())
                country_names.add(val["common"].lower())

            for alt_spelling in data["altSpellings"]:
                country_names.add(alt_spelling.lower())

            for val in data["translations"].values():
                country_names.add(val["official"].lower())
                country_names.add(val["common"].lower())

        return country_names

    async def _save_country_names(self, iso_code: str, country_names: set[str]) -> None:
        await self.db.execute(
            insert(IsoCountries).values(iso_code=iso_code, names=list(country_names))
        )
