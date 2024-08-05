from pydantic import BaseModel

__all__ = ["CountryResponse", "CountryRequest"]


class CountryRequest(BaseModel):
    iso: str
    countries: list[str]


class CountryResponse(BaseModel):
    iso: str
    match_count: int
    matches: list[str]
