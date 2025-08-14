import requests
import json
import time
import os
from datetime import date, datetime
from dateutil.parser import parse
from utils.logger import logger_1st
import traceback


class FirstAPI:
    def __init__(self):
        self.username = os.getenv("FIRST_USERNAME")
        self.password = os.getenv("FIRST_PASSWORD")
        self.token = None
        self.expire = None

    def authenticate(self):
        auth_url = "https://api.gws-eg.com/client/session/login"
        auth_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        auth_payload = {"username": self.username, "password": self.password}
        response = requests.post(auth_url, data=json.dumps(auth_payload), headers=auth_headers)
        data = response.json()

        if response.status_code != 200:
            logger_1st.error(f"Authentication failed: {response.status_code} - {response.text}")
            self.token = None
            self.expire = None

        token = data.get('token')
        if token:
            self.token = token
            self.expire = parse(data.get('expire')).timestamp()
        else:
            logger_1st.error(f"No token found: {response.status_code} - {response.text}")
            self.token = None
            self.expire = None
        
        return self.token


    def get_headers(self):
        if self.token is None or time.time() > self.expire:
            self.authenticate()
        return {"accept": "application/json", "Authorization": f"Bearer {self.token}"}


    def make_request(self, url, method="GET", params=None, data=None, retry=True):
        headers = self.get_headers()
        try:
            response = requests.request(method, url, headers=headers, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger_1st.error(f"make_request(): {traceback.format_exc()}")
            if retry:
                time.sleep(10)
                return self.make_request(url, method, params, data, retry=False)
            else:
                return None


    def get_tracks(self):
        url = "https://api.gws-eg.com/data/tracks"
        result = self.make_request(url)
        if result:
            if "header" in result:
                result.pop("header")
            return result
        else:
            logger_1st.error(f"get_tracks(): {result}")
            return None


    def get_fofixtures(self, date: date = None, fixture_id: str = None):
        if date:
            url = f"https://api.gws-eg.com/data/fofixtures/{date.strftime('%Y-%m-%d')}"
        elif fixture_id:
            url = f"https://api.gws-eg.com/data/fofixtures/{fixture_id}"
        else:
            url = "https://api.gws-eg.com/data/fofixtures"
        result = self.make_request(url)
        if result:
            if "header" in result:
                result.pop("header")
            return result
        else:
            logger_1st.error(f"get_fofixtures(): {result}")
            return None


    def get_forace(self, fixture_id: str = None, race_nr: str = None, race_id: str = None):
        if fixture_id and race_nr:
            url = f"https://api.gws-eg.com/data/forace/{fixture_id}/{race_nr}"
        elif race_id:
            url = f"https://api.gws-eg.com/data/forace/{race_id}"
        result = self.make_request(url)
        if result:
            if "header" in result:
                result.pop("header")
            return result
        else:
            logger_1st.error(f"get_forace(): {result}")
            return None



    def get_runners(self, runner_id: str):
        url = f"https://api.gws-eg.com/data/runners/{runner_id}"
        result = self.make_request(url)
        if result:
            if "timestamp" in result:
                result.pop("timestamp")
            return result
        else:
            logger_1st.error(f"get_runners(): {result}")
            return None
    

    def get_horses(self, horse_id: str):
        url = f"https://api.gws-eg.com/data/horses/{horse_id}"
        result = self.make_request(url)
        if result:
            if "timestamp" in result:
                result.pop("timestamp")
            return result
        else:
            logger_1st.error(f"get_horses(): {result}")
            return None






