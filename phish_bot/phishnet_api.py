import os
import json
import requests

api_key = os.environ.get('PHISHNET_API_KEY')

class PhishNetAPI:
    
    def __init__(self):
        self.api_key = api_key

    def get_all_jamcharts() -> str:
        phishnet_endpoint = f'https://api.phish.net/v3/jamcharts/all'

        payload = {
            'apikey': api_key,
        }

        response = requests.get(
            url=phishnet_endpoint,
            params=payload
        )
        
        parsed = json.loads(response.text)
        json_obj = json.dumps(parsed, indent=4)
        
        return json_obj