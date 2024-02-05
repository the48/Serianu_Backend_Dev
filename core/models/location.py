from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "location"

    location = Column(String)
    latitude = Column(String)
    longtitude = Column(String)