from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily, Counter
from prometheus_client import start_http_server
from datetime import datetime
import requests
import time
import json

file = 'honeypot.json'

oldres = ''
diff = ''

f=open(file, 'r')
oldres = f.read()
f.close()

def log(message):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print('* ' + dt_string + ' - ' + str(message))

def update_list():
    global diff
    global oldres
    f=open(file, 'r')
    text = f.read()
    f.close()
    diff = text.replace(oldres, '')
    oldres = text

def fetch():
    locdict = {}
    ipdict = {}

    lines = diff.split('\n')
    for row in lines:
        row = row.replace('\n', '')
        if(not row.startswith('#') and row != ''):
            #log(row)
            ip = json.loads(row)['client']
            if(ip not in ipdict):
                r = requests.get('https://freegeoip.live/json/'+ip)
                asa = r.json()
                ipdict[ip] = asa['country_code']
                
                if(asa['country_code'] in locdict):
                    locdict[asa['country_code']] += 1
                else:
                    locdict[asa['country_code']] = 1
            else:
                cn = ipdict[ip]
                if(cn in locdict):
                    locdict[cn] += 1
                else:
                    locdict[cn] = 1
    #print(locdict)
    return locdict


class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        c = CounterMetricFamily('location_field', 'Help text', labels=['place', 'geohash'])    
        log('collecting')
        d = fetch()
        c.add_metric(['bar', 'gc7x'], 1)
        c.add_metric
        for en in d:
            #print(str(en) + ' ' + str(d[en]))
            c.add_metric([en, 'gc7x'], d[en])
        update_list()
        time.sleep(10)
        yield c


if __name__ == '__main__':
    start_http_server(9567)
    REGISTRY.register(CustomCollector())
    log('starting on :9567')
    while True:
        time.sleep(1)
