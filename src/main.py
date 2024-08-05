from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import countries_router
from src.db import db
from src.http_client import http_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    await http_client.start()
    yield
    await db.disconnect()
    await http_client.stop()


app = FastAPI(
    title="Country Filter Service",
    description="API to filter countries based on ISO codes and return corresponding country names in various languages.",
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
)

app.include_router(countries_router, prefix="/api/v1")
