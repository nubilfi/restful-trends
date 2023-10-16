from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int
    scheduler_redis_host: str
    scheduler_redis_port: int
    scheduler_redis_db: int
    app_host: str
    app_port: str
    development_mode: str
    debug: bool
    sentry_dsn: str
    ttl_cache: int
    openai_api_key: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings() # type: ignore
