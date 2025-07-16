from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerData(BaseModel):
    chat_id: int
    init_message: str


class BotSettings(BaseSettings):
    TOKEN: str
    model_config = SettingsConfigDict(env_prefix='BOT_')


class AppSettings(BaseSettings):
    URL: str
    model_config = SettingsConfigDict(env_prefix='APP_')