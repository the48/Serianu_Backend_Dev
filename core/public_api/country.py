import requests
import json
from .utils import *

api_key = "ekgwCVrXcVcTvUf2umm7BQ==JR27iaVgRROBamda"
endpoint = "https://api.api-ninjas.com/v1/reversegeocoding"

headers = {
    "X-Api-Key" : api_key
}


def fetch_data(coordinates : tuple):
    try:
        latitude, longitude = coordinates

        response = requests.get(f"{endpoint}?lat={latitude}&lon={longitude}&apiKey={api_key}", headers=headers)

        if response.status_code != 200:
            data = {"StatusCode" : "900", "Content" : f"{endpoint} sent unexpected data"}
            raise UnexpectedAPIError()

        fetched_data = json.loads(response.content)

        country = fetched_data[0]["state"]    
        content = {
            "Country" : country
        }

        data = {"StatusCode" : "200", "Content" : f"{json.dumps(content)}"}
           
    except ConnectionError as error:
        data = {"StatusCode" : "600", "Content" : f"{error}"}
    
    except Exception as error:
        data = {"StatusCode" : "400", "Content" : f"{error}"}
    
    finally:
        return data