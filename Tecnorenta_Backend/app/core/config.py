from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Tecnorenta API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "supersecretkey_cambiar_en_produccion"
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/tecnorenta"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
