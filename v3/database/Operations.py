import datetime
import uuid
import json
from sqlalchemy.orm import Session

from . import Models, Schemas

def get_requestID(db: Session, requestID: str):
    return db.query(Models.Request).filter(Models.Request.RequestID == requestID).first()


def generate_requestID():
    return uuid.uuid4().hex


def create_requestID(uuid, db: Session, request: Schemas.RequestCreate):
    request = Models.Request(RequestID = uuid, Payload = str(request), Successful = True, Timestamp = str(datetime.datetime.now().replace(microsecond = 0))
)

    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def create_location(db: Session, request : str, response: Schemas.LocationCreate):
    requestID = generate_requestID()

    create_requestID(requestID, db, request)

    latitude, longitude = response["Content"].replace(" ", "").split(",")

    location = Models.Location(
        RequestID = requestID,
        Location = request,
        Latitude = latitude,
        Longitude = longitude
    )

    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def create_failed_request(db: Session, request : str, response: Schemas.RequestCreate):
    requestID = generate_requestID()

    # create_requestID(requestID, db, request)
    request = Models.Request(RequestID = requestID, Payload = str(request), Successful = False, Timestamp = str(datetime.datetime.now().replace(microsecond = 0)))
        
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

# return Operations.create_weather(db = db_conn, request = str.join(latitude, longitude), response = weather_data)

def create_weather(db: Session, request : str, response: Schemas.WeatherCreate):
    requestID = generate_requestID()

    create_requestID(requestID, db, str(request))

    data = json.loads(response)

    location = Models.Weather(
        RequestID = requestID,
        isDay = data["isDay"],
        Temperature = data["Temperature"],
        Precipitation = data["Precipitation"]
    )

    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def create_country(db: Session, request : str, response: Schemas.WeatherCreate):
    requestID = generate_requestID()

    create_requestID(requestID, db, str(request))

    data = json.loads(response)

    location = Models.Country(
        RequestID = requestID,
        Country = data["Country"]
    )

    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def create_timezone(db: Session, request : str, response: Schemas.WeatherCreate):
    requestID = generate_requestID()

    create_requestID(requestID, db, str(request))

    data = json.loads(response)

    location = Models.Timezone(
        RequestID = requestID,
        Timezone = data["Timezone"],
        Date = data["Date"],
        Time = data["Time"],
        isDST = data["isDST"],
        DST = data["DST"]
    )

    db.add(location)
    db.commit()
    db.refresh(location)
    return location