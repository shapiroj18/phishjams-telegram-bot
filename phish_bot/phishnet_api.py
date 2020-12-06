import os
import json
import requests

api_key = os.environ.get("PHISHNET_API_KEY")


class PhishNetAPI:
    def __init__(self):
        self.api_key = api_key

    def get_all_jamcharts(self):
        phishnet_endpoint = "https://api.phish.net/v3/jamcharts/all"

        payload = {
            "apikey": api_key,
        }

        response = requests.get(url=phishnet_endpoint, params=payload)

        return response.json()

    def get_jamchart_songs(self):
        response = self.get_all_jamcharts()

        all_jamchart_songs = []
        for item in response["response"]["data"]:
            all_jamchart_songs.append(item["song"].lower())

        return all_jamchart_songs

    def get_show_url(self, date):
        phishnet_endpoint = "https://api.phish.net/v3//setlists/get"

        payload = {"apikey": api_key, "showdate": date}

        response = requests.get(url=phishnet_endpoint, params=payload)

        return response.json()["response"]["data"][0]["url"]
