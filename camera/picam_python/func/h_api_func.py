# https://www.digitalocean.com/community/tutorials/how-to-use-web-apis-in-python-3
# https://realpython.com/api-integration-in-python/

import requests
import json
import os

HEADERS = {'Content-Type': 'application/json'}


def _url(path):
    API_SERVER_URL = os.environ.get('API_SERVER_URL', None)
    return API_SERVER_URL + "/" + path


def get_dev_type(serial):
    res = api_post('serial/info', {'serial': serial})
    return None if res == None else res['data']["device_type"]


#-----------------#
#  GET RestAPI    #
#-----------------#
def api_get(path):
    res = requests.get(_url(path), headers=HEADERS)
    return response_handler(res, path)

#------------------#
#  POST RestAPI    #
#------------------#


def api_post(path, content):
    res = requests.post(_url(path), headers=HEADERS,  json=content)
    return response_handler(res, path)


def response_handler(res, api_path):
    res_json = json.loads(res.content.decode('utf-8'))
    if res.status_code == 200:
        print(res_json['message'])
        return res_json
    elif res.status_code >= 500:
        print('[!] [{0}] Server Error'.format(res.status_code))
    elif res.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(
            res.status_code, api_path))
    elif res.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(res.status_code))
    elif res.status_code == 400:
        print('[!] [{0}] Bad Request'.format(res.status_code))
    elif res.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(res.status_code))
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(
            res.status_code, res.content))
    print(res_json['message'])
    return None
