from pydantic import BaseModel
from pydantic_settings import BaseSettings


class AppConfig(BaseModel):
    """Конфигурационный класс для приложения FastAPI."""

    app_host: str
    app_port: str


class DbConfig(BaseModel):
    """Конфигурационный класс для БД Postgres."""

    db_host: str
    database: str
    db_user: str
    db_password: str
    db_port: str


class BaseConfig(BaseSettings):
    """
    Основной конфигурационный класс
    для подгрузки значений из переменных окружения.
    """

    app: AppConfig
    db: DbConfig

    class Config:
        env_nested_delimiter = '__'


base_config: BaseConfig = BaseConfig(
    _env_file='infra/config.env',
    _env_file_encoding='utf-8'
)
