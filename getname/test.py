import requests
import json

def get_config():
    api = "http://v2caddy:2019/load"
    res = requests.get(api, headers={'Content-Type': 'text/json'})
    js = json.loads(res.text)
    print(js)

get_config()