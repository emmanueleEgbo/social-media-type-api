from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL

class Settings(BaseSettings):
    db_host: str
    db_name: str
    db_user: str
    db_password: str
    db_name: str
    db_port: str
    jwt_secret_key: str
    algorithm: str
    access_token_expiry_minutes:int

    @property
    def db_url(self):
        return URL.create(
            "postgresql+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name
        )


    class Config:
        env_file=".env"

settings = Settings()
