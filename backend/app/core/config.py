from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://lending_user:lending_password@localhost:5432/lending_platform"
    )

settings = Settings()