from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


# Создаем класс настроек, где будут хранится основные параметры для подключения к базе данных.
class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str

    # Инициализация ссылки асинхронного подключения к базе данных.
    @property
    def DATABASE_URL_aiomysql(self):
        return f"mysql+aiomysql://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Инициализация ссылки синхронного подключения к базе данных.
    @property
    def DATABASE_URL_pymysql(self):
        return f"mysql+pymysql://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
