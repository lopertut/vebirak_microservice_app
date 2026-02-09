from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    fastapi_port: int
    fastapi_host: str
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()