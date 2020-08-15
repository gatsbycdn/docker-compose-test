import requests
import json
import time
import random
import string
from sys import argv
script, yourownbearer, yourownzoneid, vmesspath, vlesspath = argv

def ip_generate_site():
    api_url = "http://ip-api.com/json/"
    status_check = 0
    while status_check != "success":
        time.sleep(1)
        r = requests.get(api_url)
        js = json.loads(r.text)
        # print(js)
        status_check = js['status']
    ip_addr = js["query"]
    ip_country = js["countryCode"]
    ip_city = js["city"].replace(' ', '')
    ip_string = ip_addr.replace('.','-')
    ip_isp = js["isp"].split(" ")[0]
    ip_isp = ip_isp.translate(str.maketrans('','','-:.,')) # remove useless str
    ip_random = str(random.choice(string.ascii_lowercase)) + str(random.randint(100,999))
    formatter = "{}-{}-{}-{}-{}"
    sitename = formatter.format(ip_string,ip_isp,ip_country,ip_city,ip_random).lower()
    nameandip = { 'sitename': sitename, 'ip': 'ip_addr'}
    return nameandip

nameandip = ip_generate_site()
hostname = nameandip['sitename'] + '.gatsbycdn.com'
print(hostname)

headers = {'Content-Type': 'application/json'}
headers['Authorization'] = 'Bearer {}'.format(yourownbearer)

print(headers)
zone_id = ''.format(yourownzoneid)
print(zone_id)

def add_dns_record(dns_zone_id, name, ip_content):
    params = """
    {
    "type":"A",
    "name":"oldname",
    "content":"oldcontent",
    "ttl": 120,
    "priority": 10,
    "proxied": false}"""
    params = params.replace('oldname', name)
    params = params.replace('oldcontent', ip_content)
    dns_api_url = f"https://api.cloudflare.com/client/v4/zones/{dns_zone_id}/dns_records"
    r = requests.put(dns_api_url, data = params, headers = headers)
    js = json.loads(r.text)
    print(js)
    return js

add_dns_record(zone_id, nameandip['sitename'], nameandip['ip'])

Caddyfile = """
EXAMPLE.COM {

    root * /var/www/html
    # php_fastcgi localhost:9000
    # When using php-fpm listening via a unix socket:
    # php_fastcgi unix//run/php/phpPHPVERSION-fpm.sock
    file_server
    @websockets {
        path /vmesspath
        header Connection *Upgrade*
        header Upgrade websocket
    }
    reverse_proxy @websockets localhost:18551

    @vless {
        path /vlesspath
        header Connection *Upgrade*
        header Upgrade websocket
    }
    reverse_proxy @vless localhost:18550

    tls {
        protocols tls1.2 tls1.3
        ciphers TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256
    }

    # HSTS (63072000 seconds)
    header / Strict-Transport-Security "max-age=63072000"

}
"""

Caddyfile = Caddyfile.replace("EXAMPLE.COM", hostname)
Caddyfile = Caddyfile.replace("vmesspath", vmesspath)
Caddyfile = Caddyfile.replace("vlesspath", vlesspath)

def reload_caddy(data):
    api = "http://localhost:2019/load"
    res = requests.post(api, headers={'Content-Type': 'text/caddyfile'}, data=data)
    js = json.loads(res.text)
    print(js)

reload_caddy(Caddyfile)