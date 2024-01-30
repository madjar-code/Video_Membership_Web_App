import os
from functools import lru_cache
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'


class Settings(BaseSettings):
    keyspace: str = Field(..., alias='ASTRADB_KEYSPACE')
    db_client_id: str = Field(..., alias='ASTRADB_CLIENT_ID')
    db_client_secret: str = Field(..., alias='ASTRADB_CLIENT_SECRET')

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_settings():
    return Settings()
