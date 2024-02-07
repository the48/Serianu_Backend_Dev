from pydantic import BaseModel


# Requests
class RequestBase(BaseModel):
    RequestID: str
    Payload: str
    Timestamp: str
    Successful: bool


class RequestCreate(RequestBase):

    def __str__(self):
        return str(self.Payload)
    pass

class Request(RequestBase):
    class Config:
        orm_mode = True
# Requests
        

# Locations
class LocationBase(BaseModel):
    Location: str
    Latitude: str
    Longitude: str


class LocationCreate(LocationBase):

    def  __str__(self):
        return str({"Latitude": self.Latitude, "Longitude": self.Longitude})
    pass

class Location(LocationBase):
    class Config:
        orm_mode = True

# Locations       