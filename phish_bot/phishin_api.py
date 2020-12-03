import os
import json
import requests

api_key = os.environ.get('PHISHIN_API_KEY') 

class PhishINAPI():
    
    def __init__(self):
        self.api_key = api_key

    def get_show_on_date(self):
        phishin_endpoint = 'http://phish.in/api/v1/show-on-date/:2009-10-29.json'
        
        headers = {
        'Authorization': f'Bearer {api_key}'
        }

        payload = {
            
        }

        response = requests.get(
            url=phishin_endpoint,
            headers=headers,
            params=payload
        )
        
        return response.json()