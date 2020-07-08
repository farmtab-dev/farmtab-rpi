#!/usr/bin/env python
import os

from func.h_rand_func import get_rand_num_between
from func.h_datetime_func import get_curr_datetime_in_utc, get_curr_datetime, get_curr_datetime_without_format
from func.h_conversion_func import encode_obj_to_json
from func.h_pymongo_func import find_all_by_query
import datetime
#======================#
#  GET SENSOR READING  #
#======================#
def prepare_pub_sensor_data(sensor_data):
    res = {
        "data_datetime": get_curr_datetime(),
        "temp": sensor_data["temp"],
        "ph": sensor_data["ph"],
        "ec": sensor_data["ec"],  
        "orp": sensor_data["orp"],
        "tds": sensor_data["tds"],
        "wlvl1": sensor_data["wlvl1"],
        "wlvl2": sensor_data["wlvl2"] 
    }
    return encode_obj_to_json(res)

def prepare_sensor_data_obj_main(serial_number, curr_pump_stat, arduino_input):
    data_tokens = arduino_input.decode('utf-8').split("#")
    # data_tokens = arduino_input.split("#")   #For Debugging - Dummy string

    res = {
        "data_datetime": get_curr_datetime(),
        "serial_number": serial_number,
        "waterPumpStat": curr_pump_stat["WATER"],
        "ferPumpStat": curr_pump_stat["FER"],
        "pumpStat":curr_pump_stat["WATER"] or curr_pump_stat["FER"],
        "temp": -1,
        "ph": -1,
        "ec": -1,  # Temporary reading
        "orp": -1,
        "tds": -1,
        "wlvl1": -1,
        "wlvl2": -1
    }

    i = 0
    for t in data_tokens:
        if ("@" in t):
            d = t.split("@")
            if (d[1]=="inf"):
                continue
            if (d[0]=="TEMP"):
                res["temp"] = float(d[1])
            elif (d[0]=="PH"):
                res["ph"] = float(d[1])
            elif (d[0]=="EC"):
                res["ec"] = float(d[1])
            elif (d[0]=="ORP"):
                res["orp"] = float(d[1])
            elif (d[0]=="TDS"):
                res["tds"] = float(d[1])
            elif (d[0]=="WLVL1"):
                res["wlvl1"] = float(d[1])
            elif (d[0]=="WLVL2"):
                res["wlvl2"] = float(d[1])

    print(res)
    return res, encode_obj_to_json(res)

#https://stackoverflow.com/questions/37474784/query-datetime-with-pymongo
def get_prev_data():
    item_query = {'data_datetime':{'$lt':get_curr_datetime_without_format(), '$gt':get_curr_datetime_without_format() - datetime.timedelta(hours=1)}}
    # field_restrict = {
    #     'serial_number': 1,
    #     'plant_id': 1,
    #     'img_base64string':  1,
    #     'img_need_rotate':  1,
    #     'img_datetime':  1,  #tmep
    # }
    sort_by = "img_datetime"
    res = find_all_by_query("sensor_data","prev_sensor_data", item_query)
    return res