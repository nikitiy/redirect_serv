import os

from dotenv import load_dotenv

load_dotenv()


class DBSettings:
    def __init__(self):
        self.host = os.environ["SQL_HOST"]
        self.port = os.environ["SQL_PORT"]
        self.database = os.environ["SQL_DATABASE"]
        self.user = os.environ["SQL_USER"]
        self.password = os.environ["SQL_PASSWORD"]

    @property
    def ASYNC_DATABASE_URL(self) -> str:  # noqa
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def SYNC_DATABASE_URL(self) -> str:  # noqa
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class CorsSettings:
    def __init__(self):
        self.enabled = os.environ.get("CORS_ENABLED", "true").lower() == "true"
        self.allow_origins = os.environ.get("CORS_ALLOW_ORIGINS", "*").split(",")
        self.allow_credentials = (
            os.environ.get("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
        )
        self.allow_methods = os.environ.get("CORS_ALLOW_METHODS", "*").split(",")
        self.allow_headers = os.environ.get("CORS_ALLOW_HEADERS", "*").split(",")


class BaseSettings:
    def __init__(self):
        self.guest_serv_domain = os.environ.get("GUEST_SERV_DOMAIN", "localhost")


db_settings = DBSettings()
cors_settings = CorsSettings()
base_settings = BaseSettings()
