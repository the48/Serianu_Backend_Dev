import requests
import json
from .utils import *

# api_key = "65be444b5a709411100311ncm1e3d73"
endpoint = "https://api.open-meteo.com/v1/forecast"


def fetch_data(coordinates : tuple):
    try:
        latitude, longitude = coordinates

        # https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,is_day,precipitation&hourly=temperature_2m
        response = requests.get(f"{endpoint}?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,precipitation")

        if response.status_code != 200:
            data = {"StatusCode" : "900", "Content" : f"{endpoint} sent unexpected data"}
            raise UnexpectedAPIError()

        fetched_data = json.loads(response.content)
        # temperature, isDay, precipitation = fetched_data["temperature_2m"], fetched_data["is_day"], fetched_data["precipitation"]

        isDay, temperature, precipitation = (
            bool(fetched_data['current']['is_day']),
            f"{fetched_data['current']['temperature_2m']}C",
            f"{fetched_data['current']['precipitation']}mm"
        )

        content = {
            "isDay" : isDay,
            "Temperature" : temperature,
            "Precipitation" : precipitation
        }

        data = {"StatusCode" : "200", "Content" : f"{json.dumps(content)}"}
           
    except ConnectionError as error:
        data = {"StatusCode" : "600", "Content" : f"{error}"}
    
    except Exception as error:
        data = {"StatusCode" : "400", "Content" : f"{error}"}
    
    finally:
        return data