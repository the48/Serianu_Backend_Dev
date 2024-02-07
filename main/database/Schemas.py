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
class MainRequest(BaseModel):
    Location: str    


class MainResponse(BaseModel):
    Location: str
    Latitude: str
    Longitude: str
    Temperature: str
    isDay: bool
    NewsUpdate: str
    Country: str
    LocalTime: str
#
        


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

# Weather
class WeatherBase(BaseModel):
    isDay: bool
    Temperature: str
    Precipitation: str


class WeatherCreate(WeatherBase):

    def  __str__(self):
        return str({"isDay": self.isDay, "Temperature": self.Temperature, "Precipitation": self.Precipitation})
    pass

class Weather(WeatherBase):
    class Config:
        orm_mode = True

# Weather            


# Country
        
class CountryBase(BaseModel):
    Country: str

class CountryCreate(CountryBase):

    def  __str__(self):
        return str({"Country": self.Country})
    

class Country(CountryBase):
    class Config:
        orm_mode = True

# Country   
        

# TimeZone
        
class TimezoneBase(BaseModel):
    Timezone: str
    Date : str
    Time : str
    isDST : bool
    DST : str

class TimezoneCreate(TimezoneBase):

    def  __str__(self):
        return str({"Timezone": self.Timezone, "Date": self.Date, "Time": self.Time, "isDST": self.isDST, "DST": self.DST})
    

class Timezone(TimezoneBase):
    class Config:
        orm_mode = True

# TimeZone   
        

# News
class NewsBase(BaseModel):
    Title : str
    PublishedDate : str
    Link : str

class NewsCreate(NewsBase):

    def  __str__(self):
        return str({"Title": self.Title, "PublishedDate": self.PublishedDate, "Link": self.Link})

class News(NewsBase):
    class Config:
        orm_mode = True

# News  