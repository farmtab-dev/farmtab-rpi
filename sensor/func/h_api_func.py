# https://www.digitalocean.com/community/tutorials/how-to-use-web-apis-in-python-3
# https://realpython.com/api-integration-in-python/

import requests
import json
from config.cfg_py_server import API_SERVER_URL
from config.cfg_farmtab_parameter import DEFAULT_THRESHOLD
from func.farmtab_py_threshold import update_thresholds
#headers = {'Content-Type': 'application/json',
#           'Authorization': 'Bearer {0}'.format(api_token)}
HEADERS = { 'Content-Type': 'application/json' }
def _url(path):
    return API_SERVER_URL + "/" + path

# def get_threshold():
#     resp = requests.get(_url('threshold/')).get_tasks()
#     if resp.status_code != 200:
#         raise ApiError('Cannot fetch all tasks: {}'.format(resp.status_code))
#     for item in resp.json():
#         print('{} {}'.format(item['id'], item['summary']))
#     return resp.json()

#---------------#  Get ShelfID - To ensure it is assigned
# RUN API CALLS #  Get Threshold - If not set, add one
#---------------#
# SHELF_ID = get_shelf_id(CPS.SEN_SERIAL)
# if (SHELF_ID!=None):  # Cannot get Shelf ID - Means not assigned to shelf yet
#     threshold = get_threshold(SHELF_ID)
#     if (threshold==None):  # No Default threshold
#         set_default_threshold(SHELF_ID)
#     else:
#         update_thresholds(THRESHOLD_DICT, threshold)
def sync_cloud_thres_info(serial, thres_dict):
    shelf_id = get_shelf_id(serial)
    if (shelf_id==None):  # Cannot get Shelf ID - Means not assigned to shelf yet
        return True
    else:  
        threshold = get_threshold(shelf_id)
        thres_dict["shelf_id"]=shelf_id
        if (threshold==None):  # No Default threshold
            set_default_threshold(shelf_id)
        else:
            update_thresholds(thres_dict, threshold)
        return False


def resync_cloud_thres_info(shelf_id, thres_dict):
    threshold = get_threshold(shelf_id)
    if (threshold!=None):
        update_thresholds(thres_dict, threshold)
        return True
    else:
        return False

def get_shelf_id(serial):
    res = api_post('serial/shelf', {'serial': serial})
    return None if res==None else res['data']["assigned_shelf"]


def get_threshold(shelf_id):
    res = api_post('shelf/get_threshold', {'shelf_id': shelf_id})
    return None if res==None else res['data']

def set_default_threshold(shelf_id):
    content = {
       'shelf_id': shelf_id,
       'threshold': DEFAULT_THRESHOLD
    }
    res = api_post('shelf/set_threshold', content)

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
    res = requests.post(_url(path),headers=HEADERS,  json=content)
    return response_handler(res, path)

def response_handler(res, api_path):
    res_json = json.loads(res.content.decode('utf-8'))
    if res.status_code == 200:
        print(res_json['message'])
        return res_json
    elif res.status_code >= 500:
        print('[!] [{0}] Server Error'.format(res.status_code))    
    elif res.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(res.status_code,api_path))
    elif res.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(res.status_code))
    elif res.status_code == 400:
        print('[!] [{0}] Bad Request'.format(res.status_code))
    elif res.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(res.status_code))
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(res.status_code, res.content))
    print(res_json['message'])
    return None