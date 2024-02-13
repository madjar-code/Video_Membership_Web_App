import os
from pathlib import Path
from functools import lru_cache
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'


class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    templates_dir: Path = Path(__file__).resolve().parent / 'templates'
    keyspace: str = Field(..., alias='ASTRADB_KEYSPACE')
    db_client_id: str = Field(..., alias='ASTRADB_CLIENT_ID')
    db_client_secret: str = Field(..., alias='ASTRADB_CLIENT_SECRET')
    secret_key: str = Field(..., alias='SECRET_KEY')
    jwt_algorithm: str = Field(default='HS256')
    model_config = SettingsConfigDict(env_file='.env')
    session_duration: int = Field(default=86400, alias='SESSION_DURATION')


@lru_cache
def get_settings():
    return Settings()
