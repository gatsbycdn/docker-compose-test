import requests
import json
import os

print(os.environ['yourownbearer'])

def get_config():
    api = "http://v2caddy:2019/config/"
    res = requests.get(api)
    js = json.loads(res.text)
    print(js)

get_config()
