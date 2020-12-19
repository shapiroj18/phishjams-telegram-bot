import os
import json
import requests

api_key = os.environ.get("PHISHIN_API_KEY")


class PhishINAPI:
    def __init__(self):
        self.api_key = api_key

    def get_show_on_date(self, date):
        phishin_endpoint = f"http://phish.in/api/v1/show-on-date/:{date}.json"

        headers = {"Authorization": f"Bearer {api_key}"}

        payload = {}

        response = requests.get(url=phishin_endpoint, headers=headers, params=payload)

        return response.json()

    def get_song_url(self, song, date):

        response = self.get_show_on_date(date=date)
        if response["success"] == False:
            return 'Date was not found, please enter in "YYYY-MM-DD" format'

        else:
            show_tracks = response["data"]["tracks"]

            mp3 = f'No mp3 for the song "{song}." Was the song spelled right and played on {date}?'
            for item in show_tracks:
                if item["title"].lower() == song.lower():
                    mp3 = item["mp3"]

            return mp3
