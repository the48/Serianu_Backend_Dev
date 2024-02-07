from pydantic import BaseModel
from sqlalchemy import Column, Boolean, String
from sqlalchemy.orm import relationship
from .Session import Base

# POST news update
class NewsUpdate(BaseModel):
    location : str
    description: str | None = None


# Auth
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    OperatorID: str | None = None


class Operator(BaseModel):
    OperatorID: str


class Request(Base):
    __tablename__ = "Requests"

    RequestID = Column(String, primary_key=True)
    Payload = Column(String)
    Timestamp = Column(String)
    Successful = Column(Boolean)

    # location = relationship("Location", back_populates="request", uselist=False)

    

class Location(Base):
    __tablename__ = "Locations"

    RequestID = Column(String, primary_key=True)
    Location = Column(String)
    Latitude = Column(String)
    Longitude = Column(String)

    # request = relationship("Requests", back_populates="Location")

class Weather(Base):
    __tablename__ = "Weather"

    RequestID = Column(String, primary_key=True)
    isDay = Column(Boolean)
    Temperature = Column(String)
    Precipitation = Column(String)