import pytest_asyncio
from src.http_client.client import HttpClient
import pytest
from unittest.mock import patch
from src.models.base import metadata
from databases import Database


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"


@pytest_asyncio.fixture(scope="function")
async def db_fixture():
    db = Database(DATABASE_URL)
    await db.connect()
    yield db
    await db.disconnect()


@pytest_asyncio.fixture(scope="session")
async def setup_tables(db_fixture):
    for table in metadata.sorted_tables:
        create_table_query = str(
            table.compile(dialect=db_fixture.connection().raw_connection().dialect)
        )
        await db_fixture.execute(create_table_query)

    try:
        yield
    finally:
        # Drop tables after tests
        for table in reversed(metadata.sorted_tables):
            drop_table_query = f"DROP TABLE IF EXISTS {table.name} CASCADE;"
            await db_fixture.execute(drop_table_query)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clear_db(db_fixture):
    for table in reversed(metadata.sorted_tables):
        truncate_table_query = f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;"
        await db_fixture.execute(truncate_table_query)


@pytest_asyncio.fixture(scope="session")
async def http_client():
    async with HttpClient() as client:
        yield client


@pytest.fixture
def http_client_mock(http_client):
    with patch.object(http_client, "get") as mock:
        yield mock
