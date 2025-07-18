from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class ServerData(BaseModel):
    chat_id: int
    init_message: str


class BotSettings(BaseSettings):
    TOKEN: str
    model_config = SettingsConfigDict(env_prefix='BOT_')


class AppSettings(BaseSettings):
    URL: str
    SERVER_URL: str
    model_config = SettingsConfigDict(env_prefix='APP_')