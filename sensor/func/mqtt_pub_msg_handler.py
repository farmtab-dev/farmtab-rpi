from config.cfg_py_mqtt_topic import PUB_CLOUD_TOPIC, PI_TUNING_HEADER
from config.cfg_py_serial import SEN_SERIAL
from func.farmtab_data_retrieval import prepare_sensor_data_obj_main, get_prev_data
from func.farmtab_py_msg_prep import prepare_usb_notification_message_obj, prepare_thres_notification_message_obj
from func.farmtab_py_pump_control import activate_usb_port, deactivate_usb_port, control_pump_via_gpio
from func.h_datetime_func import get_curr_datetime,get_curr_datetime_without_format, get_time_difference_in_sec
from func.h_pymongo_func import insert_item
from func.h_api_func import resync_cloud_thres_info
import os
import asyncio
#=================#
# MQTT PUB Syntax #
#=================#
def mqtt_pub_msg(client, topic, msg):
    client.publish(topic, msg, 0)
    print(topic)
    print(msg)

def get_store_sensor_data(client, pub_time_dict, curr_pump_stat, arduino_input):
    data_obj, data_str = prepare_sensor_data_obj_main(SEN_SERIAL, curr_pump_stat, arduino_input)
    # FOR STORING MESSAGE
    if (pub_time_dict["last_store"] is not None):
        curr_time = get_curr_datetime()
        time_elapse = get_time_difference_in_sec(pub_time_dict["last_store"], curr_time)

        if (time_elapse < pub_time_dict["store_interval"]):
            return data_obj

    pub_time_dict["last_store"] = get_curr_datetime()
    data_obj["data_datetime"]= get_curr_datetime_without_format()
    insert_item('sensor_data', [data_obj], "[ sensor_data ] col")
    return data_obj

def pub_sensor_data(client):
    #mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_data'], data_str)
    print("HELLO - "+get_curr_datetime())
    #mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_data'], data_str)
    all_data = get_prev_data()
    sum=0
    print (sum)
    if (len(all_data)>0):
        sum=0
        for data in all_data:
            sum+=data['temp']

    print ("CALCULATE SUM")
    print (sum)

    #return data_obj

#=======================================#
# Publish only after specified interval #
#=======================================#
def get_pub_sensor_data(client, pub_time_dict, curr_pump_stat, arduino_input):
    # Convert Sensor Data
    data_obj, data_str = prepare_sensor_data_obj_main(SEN_SERIAL, curr_pump_stat, arduino_input)

    # FOR PUBLISH MESSAGE
    if (pub_time_dict["last_pub"] is not None):
        curr_time = get_curr_datetime()
        time_elapse = get_time_difference_in_sec(pub_time_dict["last_pub"], curr_time)

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
    is_tuning_topic, cmd_action = perform_checks_on_mqtt_topic(client, mqtt_topic)
    if (is_tuning_topic):
        curr_parameters = parameter_tuning(client, mqtt_msg_str, cmd_action, curr_parameters)
    else:
        # print("Cannot take action on Unknown topic : "+ str(mqtt_topic))
        print("Update Pump Stats")
        curr_parameters = update_pump_status(client, mqtt_msg_str, curr_parameters)

    return curr_parameters

#============================#
#  PERFORM CHECK : On Topic  #
#============================#
def perform_checks_on_mqtt_topic(client, mqtt_topic):
    if(mqtt_topic.startswith(PI_TUNING_HEADER)):
        topic_tokens = mqtt_topic.split("/")
        cmd_action = topic_tokens[-1]
        print (cmd_action)
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
        tune_res = resync_cloud_thres_info(curr_parameters["threshold"]["shelf_id"], curr_parameters["threshold"])
        if(tune_res):
            msg_str = prepare_thres_notification_message_obj(get_curr_datetime(), SEN_SERIAL, "thres_success")
        else:
            msg_str = prepare_thres_notification_message_obj(get_curr_datetime(), SEN_SERIAL, "thres_fail")
        mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(msg_str))
    #--------#
    #  Etc.  #
    #--------#
    else:
        print("Unknown Command : " + mqtt_msg_str)
        mqtt_pub_msg(client, PUB_CLOUD_TOPIC["pub_tune"], "Unknown action")
        return curr_parameters
        # return False  # Indicate nothing is done
    
    mqtt_pub_msg(client, PUB_CLOUD_TOPIC["pub_tune"], "Modified "+ cmd_action)
    return curr_parameters
    
def update_pump_status(client, mqtt_msg_str, curr_parameters):
    generate_msg = False
    #-----------#
    #  Interval #
    #-----------#
    if (mqtt_msg_str == "on"):
        print("Activate USB")
        cmd_output = activate_usb_port()
        print (cmd_output)
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
        cmd_output = deactivate_usb_port()
        print (cmd_output)
        if (cmd_output == ''):
            curr_parameters["pump"]["stat"] = False
            generate_msg = True
            print("Pump is OFF")
        else:
            curr_parameters["pump"]["stat"] = False
            print("Pump is already OFF")
    if (generate_msg):
        pump_msg = prepare_usb_notification_message_obj(curr_parameters["pump"]["stat"])
        mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(pump_msg))

    return curr_parameters
    
