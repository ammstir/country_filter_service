import os

from databases import Database

__all__ = ["db"]

database_url = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
)
db = Database(database_url)
