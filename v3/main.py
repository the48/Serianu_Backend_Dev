from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from core.Configs import settings
from database.Models import NewsUpdate, Token
from fastapi import Depends, HTTPException, status
from core.Auth import *

from database import Session, Schemas, Operations

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


@app.post("/request/", response_model=Schemas.Request)
def create_request(user: Schemas.RequestCreate, db: Session = Depends(get_db)):
    return Operations.create_requestID("test", db = db, request = user)

# have to create requestid and use with this call
# create request id first, insert to requests, then add to other endpoints
# @app.post("/location/", response_model=Schemas.Location)
def create_location(location: Schemas.LocationCreate, db: Session = Depends(get_db)):
    return Operations.create_location(db = db, request = location)



@app.get("/users/{id}", response_model = Schemas.Request)
def get_request(user_id: str, db: Session = Depends(get_db)):
    request = Operations.get_requestID(db, user_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

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


def populate_db(latitude, longitude):
    try:
        # Location
        # location_data = Location.FetchData(location)

        # if location_data["StatusCode"] == "200":
        #     latitude, longitude = location_data["Content"].replace(" ", "").split(",")
        #     return Operations.create_location(db = db_conn, request = location, response = location_data)      
        # else:
        #     Operations.create_failed_request(db = db_conn, request = location, response = location_data)
        #     pass
        
        # Weather
        # weather_data = Weather.FetchData(latitude, longitude)
        request_data = {"Latitude": f"{latitude}", "Longitude": f"{longitude}"}
        # if weather_data["StatusCode"] == "200":
        #     return Operations.create_weather(db = db_conn, request = request_data, response = weather_data["Content"])
        # else:
        #     Operations.create_failed_request(db = db_conn, request = request_data, response = weather_data["Content"])
        

        # Ccountry
        country_data = Country.FetchData(latitude, longitude)
        if country_data["StatusCode"] == "200":
            return Operations.create_country(db = db_conn, request = str(request_data), response = country_data["Content"])
        else:
            Operations.create_failed_request(db = db_conn, request = request_data, response = country_data["Content"])

        

        # # get timezone
        # timezone_data = Timezone.FetchData(latitude, longitude)["Content"]
        # if timezone_data["StatusCode"] == "200":
        #     latitude, longitude = weather_data["Content"].replace(" ", "").split(",")
        # else:
        #     return # db entry failed, send request


        # # get news
        # news_data = News.FetchData(location)["Content"]
        # if news_data["StatusCode"] == "200":
        #     latitude, longitude = weather_data["Content"].replace(" ", "").split(",")
        # else:
        #     return # db entry failed, send request


    except Exception as error:
        print(error)

print(populate_db("-1.2832533", "36.8172449"))
        # use guid for req id

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 8000)