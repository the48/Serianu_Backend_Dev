import requests
import json
from utils import *

api_key = "b6f686840bee4388b83d06d9fc1cd729"
endpoint = "https://api.ipgeolocation.io/timezone"


def fetch_data(coordinates : tuple):
    try:
        latitude, longitude = coordinates

        # https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,is_day,precipitation&hourly=temperature_2m
        response = requests.get(f"{endpoint}?lat={latitude}&long={longitude}&apiKey={api_key}")

        if response.status_code != 200:
            data = {"StatusCode" : "900", "Content" : f"{endpoint} sent unexpected data"}
            raise UnexpectedAPIError()

        fetched_data = json.loads(response.content)

        timezone, date, time, isDST, DST = fetched_data["timezone"], fetched_data["date"], fetched_data["time_24"], fetched_data["is_dst"], fetched_data["dst_savings"]

        content = {
            "Timezone" : timezone,
            "Date" : date,
            "Time" : time,
            "isDST" : isDST,
            "DST" : DST
        }

        data = {"StatusCode" : "200", "Content" : f"{json.dumps(content)}"}
           
    except ConnectionError as error:
        data = {"StatusCode" : "600", "Content" : f"{error}"}
    
    except Exception as error:
        data = {"StatusCode" : "400", "Content" : f"{error}"}
    
    finally:
        return data