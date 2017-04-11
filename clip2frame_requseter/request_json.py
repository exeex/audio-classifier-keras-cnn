import requests
import json


def request_json(url):
    r= requests.get("http://140.109.21.234:35007/_process_link?youtube_link="+url)
    return json.loads(r.text)