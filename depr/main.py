import json
import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base

from core.public_api import location
from core.public_api import weather  
from core.public_api import timezone
from core.public_api import news
from core.public_api import country
from core.models.sql import database

# from core.models import location
# from core.schemas import database

# from sqlalchemy.orm import metadata

# app = FastAPI()

Base = declarative_base()

# change the schema name
# called periodically in sequence to push data to db
# convert all to post

# location.Base.metadata.create_all(bind=database.engine)


# @app.get("/")
def everyDayWeBufferin():
    return {"readme" : "hireme4success2024"}

# path parameter

# print(fetch_data("balozi+estate")) # url encode
# @app.get("/location/{strlocation}")
def get_location_coordinates(strlocation):
    return location.fetch_data(strlocation)

# sanitise input, no spaces
# @app.get("/weather/{strcoordinates}")
def get_location_weather(strcoordinates):
    strcoordinates = tuple(strcoordinates.split(","))
    return weather.fetch_data(strcoordinates) # hit the endpoint with coordinates returned


# @app.get("/timezone/{strcoordinates}")
def get_location_local_time(strcoordinates):
    strcoordinates = tuple(strcoordinates.split(","))
    return timezone.fetch_data(strcoordinates) # hit the endpoint with coordinates returned


# @app.get("/news/{strlocation}")
def get_location_news(strlocation):
    return news.fetch_data(strlocation) # hit the endpoint with coordinates returned


# @app.get("/country/{coordinates}")
def get_location_news(strcoordinates):
    strcoordinates = tuple(strcoordinates.split(","))
    return country.fetch_data(strcoordinates) # hit the endpoint with coordinates returned


# @app.get("/maparea/{coordinates}")
# async def get_location_map_area(coordinates : tuple(str, str)):
#     return "" # hit the endpoint with coordinates returned


def generate_data(location):
    data = get_location_coordinates(location)
    lat, lon = data["Content"].split(",") #remove whitespaces
    print(lat, lon)

#sqlalchemy push to db, run scheduled event

# generate_data("nairobi")


'''
main endpoints
1. get the latest updates in location (weather, localtime, news)
2. post a news update
3. dashboard: average of weather today idk what else
'''


def create_tables():
    Base.metadata.create_all(bind=database.engine)


def start_application():
    app = FastAPI(title='Backend_Test',version='1.1')
    create_tables()
    return app


app = start_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)