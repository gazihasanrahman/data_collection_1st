import os
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.base import Engine
from utils.logger import get_logger

# configuration
MARIADB_HOST = os.environ.get("MARIADB_HOST", "")
MARIADB_PORT = int(os.environ.get("MARIADB_PORT", 3306))
MARIADB_USER = os.environ.get("MARIADB_USER", "")
MARIADB_PASS = os.environ.get("MARIADB_PASS", "")
MARIADB_NAME = os.environ.get("MARIADB_NAME", "")
MARIADB_PRE_PING = os.environ.get("MARIADB_PRE_PING", "True").lower() == "true"
MARIADB_POOL_SIZE = int(os.environ.get("MARIADB_POOL_SIZE", 24))
MARIADB_MAX_OVERFLOW = int(os.environ.get("MARIADB_MAX_OVERFLOW", 24))

# set the logger
database_errors = get_logger(log_name="database_errors")

Base = declarative_base()

mariadb_engine = create_engine(
    url=f"mysql+pymysql://{MARIADB_USER}:{MARIADB_PASS}@{MARIADB_HOST}:{MARIADB_PORT}/{MARIADB_NAME}",
    pool_pre_ping=MARIADB_PRE_PING,
    pool_size=MARIADB_POOL_SIZE,
    max_overflow=MARIADB_MAX_OVERFLOW,
)

@contextlib.contextmanager
def session_scope(engine: Engine = mariadb_engine, raise_error: bool = False):
    """Provide a transactional scope around a series of operations."""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        database_errors.error(e)
        if raise_error:
            raise
    finally:
        session.close()



class Mixin:
    """Mixin class for adding common methods to models."""
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

