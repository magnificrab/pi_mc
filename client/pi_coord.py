import json
import random
import requests
import timeit
import io
import pdb

def pi_call(sesh=None):
    req_params = {'x': random.random(), 'y': random.random()}
    pi_url = 'http://192.168.1.7:5000/pi/api/v0.0/pi_in_circle'
    resp = sesh.get(pi_url, params=req_params)
    #resp = requests.get(pi_url, req_params)
    respd = resp.json().split(' ')[3]
    if respd == 'True':
        return True
    return False

def pi_coord(attempts = 10):
    ct = 0

    sesh = requests.Session()
    for i in range(attempts):
        if pi_call(sesh):
        #if pi_call():
            ct += 1

    print('pi = ', 4 * (ct/attempts))

def bulk_pi_coord(calls=1000, reqpc=10): #requests per call
    ct = 0

    sesh = requests.Session()
    for j in range(calls):
        req_data = []
        for i in range(reqpc):
            req_params = {'x': random.random(), 'y': random.random()}
            req_data.append(req_params)

        #req_data = io.StringIO(json.dumps(req_data))
        req_data = io.BytesIO(bytes(json.dumps(req_data),encoding='utf-8'))
        pi_url = 'http://192.168.1.7:5000/pi/api/v0.0/bulk_pic'
        #resp = requests.post(pi_url, data=req_data)
        resp = sesh.post(pi_url, data=req_data)  #TODO: handle non 200 returns
        if resp.status_code != 200:
            raise ValueError('Server return code not 200 {}'.format(resp.status_code))
        #lresp = json.loads(resp.json())
        #TODO: look into this further .. is this really working?
        lresp = resp.json()
        for i in lresp:
            if (i):
                ct += 1

    print('pi = ', 4 * (ct/(calls*reqpc))) 

if __name__ == '__main__':
    #pi_coord(1000)
    #print(timeit.timeit(pi_coord, number=1))
    print('10,000 requests in secs:', timeit.timeit(bulk_pi_coord, number=1))
