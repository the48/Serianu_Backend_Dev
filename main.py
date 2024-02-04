import uvicorn
from fastapi import FastAPI

# from core.public_api.location import *
# from core.public_api.weather import *
# from core.public_api.timezone import *
# from core.public_api.news import *
# from core.public_api.map import *

from core.public_api.location import fetch_data
from core.public_api.weather import fetch_data


app = FastAPI()

# change the schema name

@app.get("/")
async def everyDayWeBufferin():
    return {"readme" : "hireme4success2024"}

# path parameter

# print(fetch_data("balozi+estate")) # url encode
@app.get("/location")
async def get_location_coordinates(location : str):
    return location.fetch_data(location)


@app.get("/weather")
async def get_location_weather(coordinates : tuple):
    return weather.fetch_data(coordinates) # hit the endpoint with coordinates returned


@app.get("/timezone")
async def get_location_local_time(coordinates : tuple):
    return timezone.fetch_data(coordinates) # hit the endpoint with coordinates returned


@app.get("/news")
async def get_location_news(location : str):
    return news.fetch_data(location) # hit the endpoint with coordinates returned


# @app.get("/maparea/{coordinates}")
# async def get_location_map_area(coordinates : tuple(str, str)):
#     return "" # hit the endpoint with coordinates returned


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)