from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
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



