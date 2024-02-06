from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String

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


class Request():
    __tablename__ = "Requests"

    RequestID = Column(Integer, primary_key = True)
    Payload = Column(String)
    Timestamp = Column(String)



