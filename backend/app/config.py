from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_password: str
    database_username: str
    database_host: str
    database_name: str
    database_port: int
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    redis_host: str
    redis_port: int
    redis_username: str|None = None
    redis_password: str|None = None

    class Config:
        env_file = ".env"


settings = Settings()
