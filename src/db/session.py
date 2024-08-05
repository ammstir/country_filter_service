from databases import Database
import os

__all__ = ["db"]

database_url = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
)
db = Database(database_url)
