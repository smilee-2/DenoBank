import os

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class DataBaseSettings(BaseSettings):
    """
    Установка полей для базы данных
    url - драйвер для бд
    echo - вывод в консоль запросов в бд
    """
    url: str = "postgresql+asyncpg://postgres:123@localhost:5432/postgres"
    echo: bool = True


class SettingToken(BaseSettings):
    """
    Настройка для токена
    SECRET_KEY - секретный ключ
    ALGORITHM - алгоритм шифрования
    """
    SECRET_KEY: str = str(os.getenv('SECRET_KEY'))
    ALGORITHM: str = "HS256"


class AccessToken(SettingToken):
    """access token - время действия"""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class RefreshToken(SettingToken):
    """refresh token - время действия"""
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


setting_database = DataBaseSettings()
setting_access_token = AccessToken()
setting_refresh_token = RefreshToken()
setting_check_sig = SettingToken()


engine = create_async_engine(
    url=setting_database.url,
    echo=setting_database.echo
)

session_maker = async_sessionmaker(bind=engine)

