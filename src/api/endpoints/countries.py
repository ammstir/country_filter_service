from src.api.schemas import CountryResponse, CountryRequest
from src.processors import InvalidIsoCodeError, CountryProcessor, IsoSourceError
from src.http_client import http_client, HttpClient
from fastapi import Depends, APIRouter, HTTPException
from databases import Database
from src.db import db

router = APIRouter()


@router.post(
    "/match_country",
    response_model=CountryResponse,
    responses={
        200: {"description": "Successful Response", "model": CountryResponse},
        400: {"description": "Bad Request"},
        422: {"description": "Invalid Iso Code"},
        424: {"description": "Failed to retrieve countries info."},
        500: {"description": "Internal Server Error"},
    },
)
async def match_countries(
    request: CountryRequest,
    client: HttpClient = Depends(lambda: http_client),
    db: Database = Depends(lambda: db),
):
    """
    Matches countries by ISO code and return matched names.

    - **iso**: An ISO code.
    - **countries**: A list of countries in different languages.
    """
    processor = CountryProcessor(client, db)
    try:
        country_names = await processor.fetch_country_names_by_iso(request.iso)
    except InvalidIsoCodeError:
        raise HTTPException(
            status_code=422,
            detail={"error": "Invalid Iso Code"},
        )
    except IsoSourceError:
        raise HTTPException(
            status_code=424,
            detail={"error": "Failed to retrieve countries info."},
        )

    matches = []

    for country in request.countries:
        if country.lower() in country_names:
            matches.append(country)

    return CountryResponse(iso=request.iso, matches=matches, match_count=len(matches))
