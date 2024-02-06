from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.Configs import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_STR

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)