import json
import time
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from core.Configs import settings
from database.Models import Newss, Token

from fastapi import Depends, HTTPException, status
from core.Auth import *

from database import Session, Schemas, Operations, Models

from data_source import Location, Weather, Country, News, Timezone

Session.Base.metadata.create_all(bind=Session.engine)

def get_db():
    db = Session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_conn = Session.SessionLocal()

app = FastAPI(title = settings.PROJECT_NAME, version = settings.PROJECT_VERSION)


# @app.post("/request/", response_model=Schemas.Request)
def create_request(user: Schemas.RequestCreate, db: Session = Depends(get_db)):
    return Operations.create_requestID("test", db = db, request = user)


# @app.post("/location/", response_model=Schemas.Location)
def create_location(location: Schemas.LocationCreate, db: Session = Depends(get_db)):
    return Operations.create_location(db = db, request = location)


@app.get("/events", description = "Get Latest News Updates")
def get_updates(db: Session = Depends(get_db), r : str = Depends(oauth2_scheme)):
    request = Operations.get_updates(db)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


# @app.get("/users/{id}", response_model = Schemas.Request, description = "testing")
def get_request(user_id: str, db: Session = Depends(get_db)):
    request = Operations.get_requestID(db, user_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


# v1
@app.get("/")
async def root():
    return {"message": "aGlyZW1lNHN1Y2Nlc3MyMDI0QEhSIA=="}


# @app.get("/updates/")
# async def FetchUpdate(token: str = Depends(oauth2_scheme)):
#     return {"message": "Updates endpoint"} # send to controller


@app.post("/events/", description = "Post News Update")
async def PostNewsUpdate(update: Schemas.News = Depends(oauth2_scheme), db: Session = Depends(get_db)): # = Depends(oauth2_scheme)
    request_id = Operations.generate_requestID()
    update = Newss(RequestID = request_id, Title = update.Title, PublishedDate = update.PublishedDate, Link = update.Link)

    db.add(update)
    db.commit()
    db.refresh(update)
    return update


@app.post("/token", description = "Generate JWT")
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


@app.get("/dashboard/{location}", response_model = Schemas.MainResponse, description="Aggregates all the data")
async def get_all_data(location: str, db: Session = Depends(get_db), r : str = Depends(oauth2_scheme)):
    if location is None:
        raise HTTPException(status_code = 404, detail="Location not found")

    # build response
    coordinates = db.query(Models.Request).filter(Models.Request.RequestID == Models.Country.RequestID).with_entities(Models.Request.Payload).first()

    coordinates = json.loads(coordinates[0].replace("'", '"'))
    latitude, longitude = coordinates["Latitude"], coordinates["Longitude"]

    weather_request = db.query(Models.Request).filter(Models.Request.Payload == str(coordinates)).with_entities(Models.Request.RequestID).first()[0]

    isDay = db.query(Models.Weather).filter(Models.Weather.RequestID == weather_request).with_entities(Models.Weather.isDay).first()

    if isDay is None: isDay = False

    temperature = db.query(Models.Weather).filter(Models.Weather.RequestID == weather_request).with_entities(Models.Weather.Temperature).first()

    if temperature is None: temperature = ""

    country_coordinates = db.query(Models.Country).filter(Models.Country.RequestID == Models.Request.RequestID).with_entities(Models.Request.Payload).first()
    
    country_coordinates = json.loads(country_coordinates[0].replace("'", '"'))
    country_latitude, country_longitude = country_coordinates["Latitude"], country_coordinates["Longitude"]

    country = db.query(Models.Location).filter(Models.Location.Latitude == country_latitude).filter(Models.Location.Longitude == country_longitude).with_entities(Models.Location.Location).first()[0]

    coordinates = db.query(Models.Request).filter(Models.Request.RequestID == Models.Timezone.RequestID).with_entities(Models.Request.Payload).first()

    coordinates = json.loads(coordinates[0].replace("'", '"'))
    latitude, longitude = coordinates["Latitude"], coordinates["Longitude"]

    timezone_request = db.query(Models.Request).filter(Models.Request.Payload == str(coordinates)).with_entities(Models.Request.RequestID).first()[0]

    localtime = db.query(Models.Timezone).filter(Models.Timezone.RequestID == timezone_request).with_entities(Models.Timezone.Time).first()[0]

    if localtime is None: localtime = ""

    news_request = db.query(Models.Request).filter(Models.Request.Payload == str(location)).with_entities(Models.Request.RequestID).first()[0]

    title = db.query(Models.Newss).filter(Models.Newss.RequestID == news_request).with_entities(Models.Newss.Title).first()


    Schemas.MainResponse.Location = location
    Schemas.MainResponse.Latitude = latitude
    Schemas.MainResponse.Longitude = longitude
    Schemas.MainResponse.Country = country
    Schemas.MainResponse.LocalTime = localtime
    Schemas.MainResponse.NewsUpdate = title
    Schemas.MainResponse.Temperature = temperature
    Schemas.MainResponse.isDay = isDay

    return Schemas.MainResponse


def populate_db(location):
    try:
        # Location
        location_data = Location.FetchData(location)

        if location_data["StatusCode"] == "200":
            latitude, longitude = location_data["Content"].replace(" ", "").split(",")
            Operations.create_location(db = db_conn, request = location, response = location_data)      
        else:
            Operations.create_failed_request(db = db_conn, request = location, response = location_data)
            pass
        
        # Weather
        weather_data = Weather.FetchData(latitude, longitude)
        request_data = {"Latitude": f"{latitude}", "Longitude": f"{longitude}"}
        if weather_data["StatusCode"] == "200":
            Operations.create_weather(db = db_conn, request = request_data, response = weather_data["Content"])
        else:
            Operations.create_failed_request(db = db_conn, request = request_data, response = weather_data["Content"])
        

        # Country
        country_data = Country.FetchData(latitude, longitude)
        if country_data["StatusCode"] == "200":
            Operations.create_country(db = db_conn, request = str(request_data), response = country_data["Content"])
        else:
            Operations.create_failed_request(db = db_conn, request = request_data, response = country_data["Content"])

        # Timezone
        timezone_data = Timezone.FetchData(latitude, longitude)
        if timezone_data["StatusCode"] == "200":
            Operations.create_timezone(db = db_conn, request = str(request_data), response = timezone_data["Content"])
        else:
            Operations.create_failed_request(db = db_conn, request = location, response = timezone_data)

        # News
        news_data = News.FetchData(location)
        if news_data["StatusCode"] == "200":
            Operations.create_news(db = db_conn, request = str(location), response = news_data["Content"])
        else:
            Operations.create_failed_request(db = db_conn, request = location, response = news_data)

    except Exception as error:
        print(error)

def task_populate_db():
    populate_db("Mombasa")
    time.sleep(5000)
    populate_db("Nairobi")

task_populate_db()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)
    