from pydantic import BaseSettings, Field


class LabelServiceURL(BaseSettings):
    host: str = Field(default='localhost')
    port: int = Field(default=8000)

    class Config:
        env_prefix = 'label_service_'


class Config(BaseSettings):
    bot_token: str
    label_service: LabelServiceURL = LabelServiceURL()


app_config = Config()
