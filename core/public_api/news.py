import requests
import json
from utils import *


# https://newsapi.org/v2/everything?q=bitcoin&apiKey=


api_key = "507f3b24e60347ee8c79882a88c6bedb"
endpoint = "https://newsapi.org/v2/everything"


def fetch_data(location : str):
    try:
        response = requests.get(f"{endpoint}?q={location}&apiKey={api_key}&pageSize=1")

        if response.status_code != 200:
            data = {"StatusCode" : "900", "Content" : f"{endpoint} sent unexpected data"}
            raise UnexpectedAPIError()

        fetched_data = json.loads(response.content)

        # nothing {"status":"ok","totalResults":0,"articles":[]}
        if fetched_data["totalResults"] == 0 and len(fetched_data["articles"]) == 0:
            data = {"StatusCode" : "200", "Content" : f"Looks like there's nothing trending in {location} currently"}

        else:
            title, published_date, url = fetched_data["articles"][0]["title"], fetched_data["articles"][0]["publishedAt"], fetched_data["articles"][0]["url"]

            content = {
                "Title" : title,
                "PublishedDate" : published_date,
                "Link" : url
            }

            data = {"StatusCode" : "200", "Content" : f"{json.dumps(content)}"}

           
    except ConnectionError as error:
        data = {"StatusCode" : "600", "Content" : f"{error}"}
    
    except Exception as error:
        data = {"StatusCode" : "400", "Content" : f"{error}"}
    
    finally:
        return data
    

# # print(fetch_data("nairobi"))
# print(fetch_data("dsfjhsgkjkskdj"))