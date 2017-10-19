import requests
import urllib
import json
import yaml
from Models.Cropped import Cropped

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

BASE_URL = cfg['judge']['baseUrl']
username = cfg['judge']['user']
password = cfg['judge']['password']

def authenticate():
    url = BASE_URL + '/api/login'
    payload = { 'username': username, 'password': password }
    payload = urllib.parse.urlencode(payload)
    headers = {
        'content-type': "application/x-www-form-urlencoded"
        }

    try:
        response = requests.request("POST", url, data=payload, headers=headers)

        if response.status_code is 200:
            return response.cookies['sessionid']
        return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def post_odlc(sessionid, image):
    try:
        url = BASE_URL + '/api/odlcs'
        payload = { "type": "standard", "latitude": 0, "longitude": 0, "orientation": image.orientation, "shape": image.shape, "background_color": image.background_color, "alphanumeric": image.alphanumeric, "alphanumeric_color": image.alphanumeric_color }
        cookie = {'sessionid': sessionid}
        headers = {
            'content-type': "application/json",
            }

        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, cookies=cookie)
        return response.status_code

    except requests.exceptions.RequestException as e:
        print(e)
        return 400



