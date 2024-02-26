from typing import Any
import sqlalchemy

from sqlalchemy.orm import declarative_base, exc, sessionmaker

try:
    from twelve_factor_app_framework.configs.config import Config
    from config import config, user_app
except ImportError:
    from app.twelve_factor_app_framework.configs.config import Config
    from app.config import config, user_app


def database_url():
    host = config.get_string(Config.DATABASE_HOST)
    port = config.get_string(Config.DATABASE_PORT)
    user = config.get_string(Config.DATABASE_USER)
    password = config.get_string(Config.DATABASE_PASSWORD)
    database = config.get_string(Config.DATABASE_NAME)
    database_engine = config.get_string(Config.DATABASE_ENGINE)
    return f"{database_engine}://{user}:{password}@{host}:{port}/{database}"


class Engine:
    host = config.get_string(Config.DATABASE_HOST)
    port = config.get_string(Config.DATABASE_PORT)
    user = config.get_string(Config.DATABASE_USER)
    password = config.get_string(Config.DATABASE_PASSWORD)
    database = config.get_string(Config.DATABASE_NAME)
    database_engine = config.get_string(Config.DATABASE_ENGINE)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return sqlalchemy.create_engine(
            database_url(),
            connect_args=dict(connect_timeout=10),
        )


user_app.config["SQLALCHEMY_DATABASE_URI"] = database_url()

Base = declarative_base()
session_maker = sessionmaker(bind=Engine()())
