from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class DataBaseSettings(BaseSettings):
    """doc"""
    url: str = "postgresql+asyncpg://postgres:123@localhost:5432/postgres"
    echo: bool = True



setting_database = DataBaseSettings()


engine = create_async_engine(
    url=setting_database.url,
    echo=setting_database.echo
)

session_maker = async_sessionmaker(bind=engine)

