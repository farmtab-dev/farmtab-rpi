#!/usr/bin/env python
import os
from config.cfg_py_sensor import SEN_SERIAL
from func.h_conversion_func import encode_obj_to_json
from func.h_datetime_func import get_curr_datetime

MSG_VAR = {
    'serial': '@SERIAL@',
    'img_problem': "@IMG_PROB@",
}
MSG_TITLE = {
    'pump_on': "Pump is ON",
    'pump_off': "Pump is OFF",
    'fer_pump_on': "Fertilizer Pump is ON.",
    'fer_pump_off': "Fertilizer Pump is OFF.",
    'water_pump_on': "Water Pump is ON.",
    'water_pump_off': "Water Pump is OFF.",
    'fer_wlvl': "Fertilizer level is LOW.",
    'water_wlvl': "Water level is LOW.",
    'img_problem': MSG_VAR["img_problem"],
    'motion': "Motion detected",
    'thres_success': "Updated threshold record in Raspberry Pi",
    'thres_fail': "Fail to update threshold. Please try again",
}
# For message filtering in APP
MSG_ABOUT = {  
    'dev_prob': "sensor", 
    'read_prob': 'sensor',
    'pump' : 'dev_ctrl',
    'image': 'img',
    'thres_success': 'thres',
    'thres_fail': 'thres',
    'fer_wlvl': 'fertilizer',
    'water_wlvl': 'water',
    'fer_pump': 'fertilizer',
    'water_pump': 'water',

    #'auto_act': 'Auto Activation', 
    #'man_act': 'Manual Activation',
}

MSG_LOC = "@SITE@, @SHELF@ - " + SEN_SERIAL  # Identify by serial

MSG_SEVERITY = {
    'pump': 'info',
    'img_problem': 'critical',
    'motion': 'critical',
    'thres_success': 'critical',
    'thres_fail': 'critical',
    'low_wlvl':'critical',
    
}

#----------------#
#  NOTIFICATION  # ==> Sensor Data
#----------------#
def prepare_thres_notification_message_obj(data_rec_time, sensor_serial, problem_str, shelf_id):
    res = {
        "serial_number": sensor_serial,
        'shelf_id': shelf_id,
        "msg_datetime": data_rec_time,
        "msg_title": MSG_TITLE[problem_str],
        "msg_about": MSG_ABOUT[problem_str],
        "msg_location": MSG_LOC,
        "msg_severity": MSG_SEVERITY[problem_str],
    }

    return encode_obj_to_json(res)

#----------------#
#  NOTIFICATION  # ==> Image Processing
#----------------#
def prepare_img_notification_message_obj(img_captured_time, cam_serial, problem_str):

    if (problem_str != 'motion'):
        msg_title = MSG_TITLE[problem_str]
    else:
        msg_title = MSG_TITLE[problem_str].replace(MSG_VAR['img_problem'], str(problem_str))

    res = {
        "serial_number": cam_serial,
        "msg_datetime": img_captured_time,
        "msg_title": msg_title,
        "msg_about": MSG_ABOUT['image'],
        "msg_location": MSG_LOC,
        "msg_severity": MSG_SEVERITY[problem_str],
    }

    return encode_obj_to_json(res)

#----------------#
#  NOTIFICATION  # ==> USB
#----------------#
def prepare_usb_notification_message_obj(is_pump_on, shelf_id):

    if (is_pump_on):
        msg_title = MSG_TITLE["pump_on"]
    else:
        msg_title = MSG_TITLE["pump_off"]

    res = {
        "serial_number": SEN_SERIAL,
        'shelf_id': shelf_id,
        "msg_datetime": get_curr_datetime(),
        "msg_title": msg_title,
        "msg_about": MSG_ABOUT['pump'],
        "msg_location": MSG_LOC,
        "msg_severity": MSG_SEVERITY['pump'],
    }

    return encode_obj_to_json(res)


def prepare_low_water_notification_message_obj(pump_type, shelf_id):

    res = {
        "serial_number": SEN_SERIAL,
        'shelf_id': shelf_id,
        "msg_datetime": get_curr_datetime(),
        "msg_title": MSG_TITLE[pump_type+ '_wlvl'],
        "msg_about": MSG_ABOUT[pump_type+ '_wlvl'],
        "msg_location": MSG_LOC,
        "msg_severity": MSG_SEVERITY['low_wlvl'],
    }

    return encode_obj_to_json(res)

def prepare_gpio_pump_notification_message_obj(pump_type, action, shelf_id):

    res = {
        "serial_number": SEN_SERIAL,
        'shelf_id': shelf_id,
        "msg_datetime": get_curr_datetime(),
        "msg_title": MSG_TITLE[pump_type+ '_pump_'+action],
        "msg_about": MSG_ABOUT[pump_type+'_pump'],
        "msg_location": MSG_LOC,
        "msg_severity": MSG_SEVERITY['pump'],
    }

    return encode_obj_to_json(res)
