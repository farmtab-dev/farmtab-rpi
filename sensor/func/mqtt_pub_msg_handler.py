from config.cfg_py_mqtt_topic import PUB_CLOUD_TOPIC, PI_TUNING_HEADER
from config.cfg_py_sensor import SEN_SERIAL, SEND_DATA_HOUR, CHECK_THRES_MINS
from func.farmtab_data_retrieval import prepare_sensor_data_obj_main, get_prev_data, prepare_pub_sensor_data
from func.farmtab_py_msg_prep import prepare_usb_notification_message_obj, prepare_thres_notification_message_obj
from func.farmtab_py_pump_control import pump_ctrl
from func.h_datetime_func import get_curr_datetime, get_curr_datetime_without_format, get_hour, get_minute, get_time_difference_in_sec
from func.h_pymongo_func import insert_item
from func.h_api_func import resync_cloud_thres_info
from func.farmtab_py_threshold import check_threshold, check_threshold_sr, check_threshold_workshop
from func.h_conversion_func import encode_obj_to_json
import os
import asyncio
#=================#
# MQTT PUB Syntax #
#=================#
def mqtt_pub_msg(client, topic, msg):
    client.publish(topic, msg, 0)
    print(topic, " ", msg)

def get_store_sensor_data(client, pub_time_dict, curr_pump_stat, arduino_input):
    data_obj, data_str = prepare_sensor_data_obj_main(
        SEN_SERIAL, curr_pump_stat, arduino_input)
    # FOR STORING MESSAGE
    if (pub_time_dict["last_store"] is not None):
        curr_time = get_curr_datetime()
        time_elapse = get_time_difference_in_sec(
            pub_time_dict["last_store"], curr_time)

        if (time_elapse < pub_time_dict["store_interval"]):
            return data_obj

    pub_time_dict["last_store"] = get_curr_datetime()
    data_obj["data_datetime"] = get_curr_datetime_without_format()
    insert_item('sensor_data', [data_obj], "[ sensor_data ] col")
    return data_obj


def check_exist_sensor(data_obj, data_type):
    if (data_type in data_obj):
        return data_obj[data_type]
    else:
        return 0

def check_thres_pub_sensor_data(APP_TYPE, client, CTRL_TIME_DICT, CURR_PUMP_DICT, THRESHOLD_DICT):
    if (APP_TYPE!="WORKSHOP"):
        if (get_hour() not in SEND_DATA_HOUR):
            print("\n\nFATAL_INFO - NOT THE TIME YET - "+get_curr_datetime())
            return

    print("\n\nINFO - "+get_curr_datetime())
    #mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_data'], data_str)
    all_data = get_prev_data()
    print(all_data)
    data_res = {
        "temp": 0,
        "ph": 0,
        "ec": 0,
        "orp": 0,
        "tds": 0,
        "co2": 0,
        "air_temperature": 0,
        "humidity": 0,
        "fertilizer": -1,
        "water": -1
    }
    # data_res = {"temp": 0, "ph": 0, "ec": 0,  "orp": 0,
    #             "tds": 0, "fertilizer": -1, "water": -1}

    if (len(all_data) > 0):
        for data in all_data:
            # data_res['temp'] += data['temp']
            # data_res['ph'] += data['ph']
            # data_res['ec'] += data['ec']
            # data_res['orp'] += data['orp']
            # data_res['tds'] += data['tds']
            data_res['temp'] += check_exist_sensor(data,'temp')
            data_res['ph'] += check_exist_sensor(data,'ph')
            data_res['ec'] += check_exist_sensor(data,'ec')
            data_res['orp'] += check_exist_sensor(data,'orp')
            data_res['tds'] += check_exist_sensor(data,'tds')
            data_res['co2'] += check_exist_sensor(data, 'co2')
            data_res['air_temperature'] += check_exist_sensor(data, 'air_temperature')
            data_res['humidity'] += check_exist_sensor(data, 'humidity')


    print("CALCULATE data_res for ", len(all_data), " data\n", data_res)
    data_res['temp'] /= len(all_data)
    data_res['ph'] /= len(all_data)
    data_res['ec'] /= len(all_data)
    data_res['orp'] /= len(all_data)
    data_res['tds'] /= len(all_data)
    data_res['co2'] /= len(all_data)
    data_res['air_temperature'] /= len(all_data)
    data_res['humidity'] /= len(all_data)
    data_res['fertilizer'] = all_data[-1]["fertilizer"]
    data_res['water'] = all_data[-1]["water"]
    print("SENSOR DATA : ", data_res)
    # if (APP_TYPE == "WORKSHOP"):
    #     if(get_minute() in CHECK_THRES_MINS):
    #         check_threshold(client, CTRL_TIME_DICT, CURR_PUMP_DICT,THRESHOLD_DICT, data_res)
    # elif (APP_TYPE == "SR"):
    if (APP_TYPE == "SR"):
        check_threshold_sr(client, CTRL_TIME_DICT,CURR_PUMP_DICT, THRESHOLD_DICT, data_res)
    elif (APP_TYPE == "WORKSHOP"):
        check_threshold_workshop(client, CTRL_TIME_DICT,CURR_PUMP_DICT, THRESHOLD_DICT, data_res)
    else:
        check_threshold(client, CTRL_TIME_DICT, CURR_PUMP_DICT,THRESHOLD_DICT, data_res)

    print(CTRL_TIME_DICT, "\n", CURR_PUMP_DICT, "\n", THRESHOLD_DICT)
    pub_data = prepare_pub_sensor_data(data_res)
    mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_data'], str(pub_data))
    # return data_obj

#=======================================#
# Publish only after specified interval #
#=======================================#
def get_pub_sensor_data(client, pub_time_dict, curr_pump_stat, arduino_input):
    # Convert Sensor Data
    data_obj, data_str = prepare_sensor_data_obj_main(SEN_SERIAL, curr_pump_stat, arduino_input)

    # FOR PUBLISH MESSAGE
    if (pub_time_dict["last_pub"] is not None):
        curr_time = get_curr_datetime()
        time_elapse = get_time_difference_in_sec(
            pub_time_dict["last_pub"], curr_time)

        if (time_elapse < pub_time_dict["pub_interval"]):
            return data_obj

    pub_time_dict["last_pub"] = get_curr_datetime()
    #mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_data'], data_str)
    return data_obj


#=================#
# Tune Parameters #
#=================#
def tune_parameter(client, mqtt_topic, mqtt_msg_str, curr_parameters):
    print("PARAMETER TUNING CHECK")
    is_tuning_topic, cmd_action = perform_checks_on_mqtt_topic(
        client, mqtt_topic)
    if (is_tuning_topic):
        curr_parameters = parameter_tuning(
            client, mqtt_msg_str, cmd_action, curr_parameters)
    else:
        # print("Cannot take action on Unknown topic : "+ str(mqtt_topic))
        print("Update Pump Stats")
        # curr_parameters = update_pump_status(client, mqtt_msg_str, curr_parameters)

    return curr_parameters

#============================#
#  PERFORM CHECK : On Topic  #
#============================#
def perform_checks_on_mqtt_topic(client, mqtt_topic):
    if(mqtt_topic.startswith(PI_TUNING_HEADER)):
        topic_tokens = mqtt_topic.split("/")
        cmd_action = topic_tokens[-1]
        print(cmd_action)
        return True, cmd_action  # Means it is a valid command
    print("Is Command")
    return False, ''

#==========================#
#  PERFORM CHECK : On Msg  #    [ Basic ]
#==========================#
def parameter_tuning(client, mqtt_msg_str, cmd_action, curr_parameters):
    #-----------#
    #  Interval #
    #-----------#
    if (cmd_action == "pub_interval"):
        curr_parameters["pub"]["pub_interval"] = int(mqtt_msg_str)
    elif (cmd_action == "store_interval"):
        curr_parameters["pub"]["store_interval"] = int(mqtt_msg_str)
    elif (cmd_action == "check_interval"):
        curr_parameters["thres"]["check_interval"] = int(mqtt_msg_str)
    elif (cmd_action == "ctrl_interval"):
        curr_parameters["thres"]["ctrl_interval"] = int(mqtt_msg_str)
    #------------#
    #  Threshold #
    #------------#
    elif (cmd_action == "threshold"):
        tune_res = resync_cloud_thres_info(
            curr_parameters["threshold"]["shelf_id"], curr_parameters["threshold"])
        # if(tune_res):
        #     msg_str = prepare_thres_notification_message_obj(get_curr_datetime(), SEN_SERIAL, "thres_success",curr_parameters["threshold"]["shelf_id"])
        # else:
        #     msg_str = prepare_thres_notification_message_obj(get_curr_datetime(), SEN_SERIAL, "thres_fail",curr_parameters["threshold"]["shelf_id"])
        # mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(msg_str))
    #--------#
    #  Etc.  #
    #--------#
    else:
        print("Unknown Command : " + mqtt_msg_str)
        mqtt_pub_msg(client, PUB_CLOUD_TOPIC["pub_tune"], "Unknown action")
        return curr_parameters
        # return False  # Indicate nothing is done

    mqtt_pub_msg(client, PUB_CLOUD_TOPIC["pub_tune"], "Modified " + cmd_action)
    return curr_parameters

# DISABLED
def update_pump_status(client, mqtt_msg_str, curr_parameters):
    generate_msg = False
    #-----------#
    #  Interval #
    #-----------#
    if (mqtt_msg_str == "on"):
        print("Activate USB")
        cmd_output = pump_ctrl("PI_USB", "ON")
        print(cmd_output)
        if (cmd_output == ''):
            curr_parameters["pump"]["stat"] = True
            generate_msg = True
            print("Pump is ON")
        else:
            curr_parameters["pump"]["stat"] = True
            print("Pump is already ON")
    #---------------#
    #  Temperature  #
    #---------------#
    elif(mqtt_msg_str == "off"):
        print("Deactivate USB")
        cmd_output = pump_ctrl("PI_USB", "OFF")
        print(cmd_output)
        if (cmd_output == ''):
            curr_parameters["pump"]["stat"] = False
            generate_msg = True
            print("Pump is OFF")
        else:
            curr_parameters["pump"]["stat"] = False
            print("Pump is already OFF")
    if (generate_msg):
        pump_msg = prepare_usb_notification_message_obj(
            curr_parameters["pump"]["stat"], curr_parameters["threshold"]["shelf_id"])
        mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(pump_msg))

    return curr_parameters
