from databases import Database
from sqlalchemy import MetaData, create_engine

from src.config import settings

database = Database(settings.database_url)
metadata = MetaData()
engine = create_engine(
    settings.database_url.replace("+aiosqlite", ""),
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)


async def connect_db():
    await database.connect()


async def disconnect_db():
    await database.disconnect()

