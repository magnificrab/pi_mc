import json
import random
import time
import requests
#import timeit
import io
import pdb

#TODO: how to replace localhost with the host that is serving the test?
#TODO: a lot of the client code is duplicated here. 
def admin_forbidden():
    sesh = requests.Session()
    pi_url = 'http://localhost:5000/pi/api/v0.0/documentation'
    resp = sesh.get(pi_url)
    sesh.close()
    if resp.status_code == 403:
        return True
    else:
        return False

#TODO: deal with staydead if re-implemented
def admin_kill():
    sesh = requests.Session()
    pi_url = 'http://localhost:5000/pi/api/v0.0/admin/kill'
    resp = sesh.get(pi_url)
    sesh.close()
    if resp.status_code == 204:
        return True
    else:
        return False

def admin_status():
    sesh = requests.Session()
    pi_url = 'http://localhost:5000/pi/api/v0.0/admin/status'
    resp = sesh.get(pi_url)
    sesh.close()
    if resp.status_code == 200:
        return True
    else:
        return False

def admin_stats(pic_expected=0):
    sesh = requests.Session()
    pi_url = 'http://localhost:5000/pi/api/v0.0/admin/stats'
    resp = sesh.get(pi_url)
    r = resp.json()
    sesh.close()
    if resp.status_code == 200 and pic_expected == r['pic']:
        return True
    else:
        return False

def pi_call(sesh=None):
    req_params = {'x': random.random(), 'y': random.random()}
    pi_url = 'http://localhost:5000/pi/api/v0.0/pi_in_circle'
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

    sesh.close()
    print('pi = ', 4 * (ct/attempts))

def bulk_pi_coord(calls=10, reqpc=1000): #requests per call
    ct = 0

    sesh = requests.Session()
    for j in range(calls):
        req_data = []
        for i in range(reqpc):
            req_params = {'x': random.random(), 'y': random.random()}
            req_data.append(req_params)

        #req_data = io.StringIO(json.dumps(req_data))
        req_data = io.BytesIO(bytes(json.dumps(req_data),encoding='utf-8'))
        pi_url = 'http://localhost:5000/pi/api/v0.0/bulk_pic'
        resp = sesh.post(pi_url, data=req_data)  #TODO: handle non 200 returns
        if resp.status_code != 200:
            raise ValueError('Server return code not 200 {}'.format(resp.status_code))
        #lresp = json.loads(resp.json())
        #TODO: look into this further .. is this really working?
        lresp = resp.json()
        for i in lresp:
            if (i):
                ct += 1
    sesh.close()

    return 4 * (ct/(calls*reqpc))

if __name__ == '__main__':
    #pi_coord(1000)
    #print(timeit.timeit(pi_coord, number=1))
    #print('10,000 requests in secs:', timeit.timeit(bulk_pi_coord, number=1))
    print('Error: this module should not be called as main. Call integration_test instead.')
    print('       To test the service directly, use test_circle_svc.')
