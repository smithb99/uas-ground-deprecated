import requests
import urllib
import json
import yaml

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

def post_odlc(sessionid):
    url = BASE_URL + '/api/odlcs'

    payload = { "type": "standard", "latitude": 38.1478, "longitude": -76.4275, "orientation": "n", "shape": "star", "background_color": "orange", "alphanumeric": "C", "alphanumeric_color": "black" }
    cookie = {'sessionid': sessionid}
    headers = {
        'content-type': "application/json",
        }

    try:
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, cookies=cookie)
        return response.status_code

    except requests.exceptions.RequestException as e:
        print(e)
        return 400


