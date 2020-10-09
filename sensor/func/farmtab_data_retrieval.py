#!/usr/bin/env python
import os

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
        "co2": sensor_data["co2"],
        "air_temperature": sensor_data["air_temperature"],
        "humidity": sensor_data["humidity"],
        "fertilizer": sensor_data["fertilizer"],
        "water": sensor_data["water"] 
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
        "co2":-1,
        "air_temperature":-1,
        "humidity":-1,
        "fertilizer": -1,
        "water": -1
    }

    i = 0
    for t in data_tokens:
        if ("@" in t):
            d = t.split("@")
            if (d[1]=="inf" or d[1]=="nan"):
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
            elif (d[0]=="CO2"):
                res["co2"] = float(d[1])
            elif (d[0]=="TEMP_DHT"):
                res["air_temperature"] = float(d[1])
            elif (d[0]=="HUM_DHT"):
                res["humidity"] = float(d[1])
            elif (d[0]=="WLVL1" or d[0]=="W_FER"):
                res["fertilizer"] = float(d[1])
            elif (d[0]=="WLVL2" or d[0]=="W_WATER"):
                res["water"] = float(d[1])

    print(res)
    return res, encode_obj_to_json(res)

#https://stackoverflow.com/questions/37474784/query-datetime-with-pymongo
def get_prev_data():
    item_query = {'data_datetime':{'$lt':get_curr_datetime_without_format(), '$gt':get_curr_datetime_without_format() - datetime.timedelta(hours=3)}}
    # field_restrict = {
    #     'data_datetime': 1,
    # }
    sort_by = "img_datetime"
    res = find_all_by_query("sensor_data","prev_sensor_data", item_query)
    return res
