from pydantic import Field
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL") # type: ignore
    JWT_SECRET: str = Field(..., env="JWT_SECRET") # type: ignore
    JWT_ALG: str = Field(default="HS256", env="JWT_ALG") # type: ignore
    JWT_EXPIRES_MIN: int = Field(default=60*24, env="JWT_EXPIRES_MIN") # type: ignore
    PROJECT_NAME: str = "Devinote"
    ENVIRONMENT:str= Field(..., env="ENVIRONMENT") # type: ignore

    class Config:
        env_file = ".env"


settings = Settings() # type: ignore
