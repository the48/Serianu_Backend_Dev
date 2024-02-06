from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from core.Configs import settings
from database.Models import NewsUpdate, Token
from fastapi import Depends, HTTPException, status
from core.Auth import *

from .database import *


from data_source import Location, Weather, Country, News, Timezone

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = settings.PROJECT_NAME, version = settings.PROJECT_VERSION)

# v1 ?
# Only want the legit endpoints here, data fetch later
@app.get("/")
async def root():
    return {"message": "Hello World"} #hireme4success


@app.get("/updates/")
async def FetchUpdate(token: str = Depends(oauth2_scheme)):
    return {"message": "Updates endpoint"} # send to controller


@app.post("/news/")
async def PostUpdate(update : NewsUpdate = Depends(oauth2_scheme)):
    update_data = update.dict()

    update_data.location
    update_data.description # send to controller

    return update


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes = settings.JWT_VALIDITY)

    access_token = create_access_token(
        data={"sub": user},
        expires_delta = access_token_expires
    )

    return Token(access_token = access_token, token_type = "bearer")


def populate_db(location):
    try:
        location_data = Location.FetchData(location)
        if weather_data["StatusCode"] == "200":
            latitude, longitude = location_data["Content"].replace(" ", "").split(",")
            # send to db
        else:
            return # db entry failed, send request
        

        # get weather
        weather_data = Weather.FetchData(latitude, longitude)["Content"]
        if weather_data["StatusCode"] == "200":
            latitude, longitude = weather_data["Content"].replace(" ", "").split(",")
        else:
            return # db entry failed, send request
        

        # get country
        country_data = Country.FetchData(latitude, longitude)["Content"]
        if country_data["StatusCode"] == "200":
            latitude, longitude = weather_data["Content"].replace(" ", "").split(",")
        else:
            return # db entry failed, send request
        

        # get timezone
        timezone_data = Timezone.FetchData(latitude, longitude)["Content"]
        if timezone_data["StatusCode"] == "200":
            latitude, longitude = weather_data["Content"].replace(" ", "").split(",")
        else:
            return # db entry failed, send request


        # get news
        news_data = News.FetchData(location)["Content"]
        if news_data["StatusCode"] == "200":
            latitude, longitude = weather_data["Content"].replace(" ", "").split(",")
        else:
            return # db entry failed, send request


    except Exception as error:
        print(error)


# print(populate_db("nairobi"))
models.

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)