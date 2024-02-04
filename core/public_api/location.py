import requests
import json
from .utils import *

api_key = "65be444b5a709411100311ncm1e3d73"
endpoint = "https://geocode.maps.co"


def fetch_data(location : str):
    try:
        response = requests.get(f"{endpoint}/search?q={location}&api_key={api_key}")

        if response.status_code != 200:
            data = {"StatusCode" : "900", "Content" : f"{endpoint} sent unexpected data"}
            raise UnexpectedAPIError()

        fetched_data = json.loads(response.content)
        latitude, longitude = fetched_data[0]["lat"], fetched_data[0]["lon"]

        data = {"StatusCode" : "200", "Content" : f"{latitude}, {longitude}"}

        return data
           
    except ConnectionError as error:
        data = {"StatusCode" : "600", "Content" : f"{error}"}
    
    except Exception as error:
        data = {"StatusCode" : "400", "Content" : f"{error}"}
    
    finally:
        return data
    