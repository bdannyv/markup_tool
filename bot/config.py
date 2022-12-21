from pydantic import BaseSettings


class Config(BaseSettings):
    bot_token: str


app_config = Config()
