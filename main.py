import uvicorn
from fastapi import FastAPI

from core.public_api import location
from core.public_api import weather  
from core.public_api import timezone
from core.public_api import news
from core.public_api import country

app = FastAPI()

# change the schema name
# called periodically in sequence to push data to db
# convert all to post

@app.get("/")
async def everyDayWeBufferin():
    return {"readme" : "hireme4success2024"}

# path parameter

# print(fetch_data("balozi+estate")) # url encode
@app.get("/location/{strlocation}")
async def get_location_coordinates(strlocation : str):
    return location.fetch_data(strlocation)


@app.get("/weather/{strcoordinates}")
async def get_location_weather(strcoordinates : str):
    strcoordinates = tuple(strcoordinates.split(","))
    return weather.fetch_data(strcoordinates) # hit the endpoint with coordinates returned


@app.get("/timezone/{strcoordinates}")
async def get_location_local_time(strcoordinates : str):
    return timezone.fetch_data(strcoordinates) # hit the endpoint with coordinates returned


@app.get("/news/{strlocation}")
async def get_location_news(strlocation : str):
    return news.fetch_data(strlocation) # hit the endpoint with coordinates returned

@app.get("/news/{strlocation}")
async def get_location_news(strlocation : str):
    return country.fetch_data(strlocation) # hit the endpoint with coordinates returned


# @app.get("/maparea/{coordinates}")
# async def get_location_map_area(coordinates : tuple(str, str)):
#     return "" # hit the endpoint with coordinates returned


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)