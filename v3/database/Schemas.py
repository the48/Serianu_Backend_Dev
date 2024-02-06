from pydantic import BaseModel


class RequestBase(BaseModel):
    RequestID: str
    Payload: str
    Timestamp: str


class RequestCreate(RequestBase):
    pass


class Request(RequestBase):
    class Config:
        orm_mode = True