from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    declarative_base,
)


class Config:
    ENGINE = create_engine("sqlite+pysqlite:///mydb.db", echo=True)
    SESSION = sessionmaker(ENGINE)
    BASE = declarative_base()
