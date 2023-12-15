from pathlib import Path
from sys import path

from pydantic.fields import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(path[0]) / ".env", env_file_encoding="utf-8", extra="allow"
    )

    debug: bool = False

    db_url: str = Field(default_factory=str)
    faceplusplus_api_key: str = Field(default_factory=str)
    faceplusplus_api_secret: str = Field(default_factory=str)
