from dotenv import dotenv_values
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

config = dotenv_values(".env")


class DatabaseService:
    database_url: str
    engine: Engine

    def __init__(self):
        self.database_url = self._get_env_var("DATABASE_URL")
        self.engine = create_engine(self.database_url)

    def _get_env_var(self, key: str, default: str = "") -> str:
        value = config.get(key)

        if not value:
            if not default:
                raise ValueError(f"{key} is not set")

            value = default

        return value

    def session(self):
        session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

        return session()
