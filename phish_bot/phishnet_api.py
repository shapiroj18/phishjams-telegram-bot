import os
import json
import random
import requests

api_key = os.environ.get("PHISHNET_API_KEY")


class PhishNetAPI:
    def __init__(self):
        self.api_key = api_key

    def get_root_endpoint(self):
        phishnet_endpoint = "https://api.phish.net/v3/"

        payload = {"apikey": api_key}

        response = requests.get(url=phishnet_endpoint, params=payload)

        return response

    def get_all_jamcharts(self):
        phishnet_endpoint = "https://api.phish.net/v3/jamcharts/all"

        payload = {
            "apikey": api_key,
        }

        response = requests.get(url=phishnet_endpoint, params=payload)

        return response.json()
    
    def get_one_jamchart(self, songid):
        phishnet_endpoint = "https://api.phish.net/v3/jamcharts/get"
        payload = {
            "apikey": api_key,
            "songid": songid
        }
        
        response = requests.get(url=phishnet_endpoint, params=payload)

        return response.json()

    def get_jamchart_song_ids(self):
        response = self.get_all_jamcharts()

        all_jamchart_songs = []
        for item in response["response"]["data"]:
            all_jamchart_songs.append(item["songid"])

        return all_jamchart_songs
    
    def get_random_jamchart(self):
        jamchart_songs = self.get_jamchart_song_ids()
        rand_id = random.choice(jamchart_songs)
        
        chart = self.get_one_jamchart(rand_id)
        song = chart['response']['data']['song']
        entries_count = len(chart['response']['data']['entries'])
        rand_date = chart['response']['data']['entries'][random.randrange(entries_count)]['showdate']
        
        return song, rand_date

    def get_show_url(self, date):
        phishnet_endpoint = "https://api.phish.net/v3//setlists/get"

        payload = {"apikey": api_key, "showdate": date}

        response = requests.get(url=phishnet_endpoint, params=payload)

        return response.json()["response"]["data"][0]["url"]
