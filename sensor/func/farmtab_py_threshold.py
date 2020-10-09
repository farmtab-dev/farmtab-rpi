from func.farmtab_py_pump_control import pump_ctrl
from func.h_datetime_func import get_curr_datetime, get_time_difference_in_sec
from func.farmtab_py_msg_prep import prepare_low_water_notification_message_obj, prepare_gpio_pump_notification_message_obj
from config.cfg_py_mqtt_topic import PUB_CLOUD_TOPIC
import time


def mqtt_pub_cloud_msg(client, msg):
    client.publish(PUB_CLOUD_TOPIC['pub_msg'], str(msg), 0)
    print(PUB_CLOUD_TOPIC['pub_msg'], " ", str(msg))

def print_threshold(data, thres_dict):
    print("\nCHECK_THRES ==> " +
          "PH:" + str(data["ph"]) + "("+str(thres_dict["thres_ph_min"]) + "-" + str(thres_dict["thres_ph_max"])+") \t" +
          "EC:" + str(data["ec"]) + "("+str(thres_dict["thres_ec_min"]) + "-" + str(thres_dict["thres_ec_max"])+") \t" +
          "TDS:" + str(data["tds"]) + "("+str(thres_dict["thres_tds_min"]) + "-" + str(thres_dict["thres_tds_max"])+")")

def update_thresholds(thres_obj, new_thres):
    # TEMPERATURE
    thres_obj["thres_temp_min"] = new_thres["thres_temp_min"]
    thres_obj["thres_temp_max"] = new_thres["thres_temp_max"]
    # PH
    thres_obj["thres_ph_min"] = new_thres["thres_ph_min"]
    thres_obj["thres_ph_max"] = new_thres["thres_ph_max"]
    # EC
    thres_obj["thres_ec_min"] = new_thres["thres_ec_min"]
    thres_obj["thres_ec_max"] = new_thres["thres_ec_max"]
    # ORP
    thres_obj["thres_orp_min"] = new_thres["thres_orp_min"]
    thres_obj["thres_orp_max"] = new_thres["thres_orp_max"]
    # TDS
    thres_obj["thres_tds_min"] = new_thres["thres_tds_min"]
    thres_obj["thres_tds_max"] = new_thres["thres_tds_max"]
    print("SUCCESS update threshold - "+ str(thres_obj))

#====================#
#  CONDITION CHECKS  #
#====================#
def trigger_fertilizer(data, thres_dict):
    return data["ec"] <= thres_dict["thres_ec_min"] or data["tds"] <= thres_dict["thres_tds_min"]
def trigger_water(data, thres_dict):
    return data["ph"] <= thres_dict["thres_ph_min"] or data["ec"] >= thres_dict["thres_ec_max"] or data["tds"] >= thres_dict["thres_tds_max"]

#===================#
#  Check THRESHOLD  #
#===================#       
def check_threshold(client, ctrl_time_dict, curr_pump_dict, thres_dict, data):
    print_threshold(data, thres_dict)
    # if (ctrl_time_dict["last_check"] is not None):
    #     # Check for last check duration
    #     curr_time = get_curr_datetime()
    #     time_elapse = get_time_difference_in_sec(ctrl_time_dict["last_check"], curr_time)
    #     if (time_elapse < ctrl_time_dict["check_interval"]):
    #         print ("    Delay checks for " + str(time_elapse))
    #         return 

    # ctrl_time_dict["last_check"] = get_curr_datetime()
    shelf_id = thres_dict["shelf_id"]
    if (trigger_fertilizer(data,thres_dict)):
        if (int(data["fertilizer"])==0):
            print("\nALERT Cannot trigger fertilizer pump")
            mqtt_pub_cloud_msg(client, prepare_low_water_notification_message_obj("fer", shelf_id))
            return
        else:
            mqtt_pub_cloud_msg(client, prepare_gpio_pump_notification_message_obj("fer", "on", shelf_id))
            pump_ctrl("FER", "ON")
            time.sleep(ctrl_time_dict["ctrl_interval"])
            pump_ctrl("FER", "OFF")
            # mqtt_pub_cloud_msg(client, prepare_gpio_pump_notification_message_obj("fer", "off", shelf_id))
        
    elif (trigger_water(data,thres_dict)):
        if (int(data["water"])==0):
            print("\nALERT Cannot trigger water pump")
            mqtt_pub_cloud_msg(client,  prepare_low_water_notification_message_obj("water", shelf_id))
            return
        else:
            mqtt_pub_cloud_msg(client,  prepare_gpio_pump_notification_message_obj("water", "on", shelf_id))
            pump_ctrl("WATER", "ON")
            time.sleep(ctrl_time_dict["ctrl_interval"])
            pump_ctrl("WATER", "OFF")
            # mqtt_pub_cloud_msg(client, prepare_gpio_pump_notification_message_obj("water", "off", shelf_id))
            
    
def check_threshold_sr(client, ctrl_time_dict, curr_pump_dict, thres_dict, data):
    print_threshold(data,thres_dict)

    shelf_id = thres_dict["shelf_id"]
    if (int(data["water"]) == 0):
        print("\nLow water")
        if (int(data["fertilizer"]) == 0):
            print("\nALERT Cannot trigger water - Low water supply")
            mqtt_pub_cloud_msg(client,  prepare_low_water_notification_message_obj("water", shelf_id))
            # return  # Disabled to continue checking the threshold
        else:
            mqtt_pub_cloud_msg(client,  prepare_gpio_pump_notification_message_obj("water", "on", shelf_id))
            pump_ctrl("WATER", "ON")
            time.sleep(10)  #For squareRoot
            pump_ctrl("WATER", "OFF")

    if (trigger_fertilizer(data, thres_dict)):
        # if (int(data["fertilizer"]) == 0):
        #     print("\nALERT Cannot trigger fertilizer pump")
        #     mqtt_pub_cloud_msg(client, prepare_low_water_notification_message_obj("fer", shelf_id))
        #     return
        # else:
        mqtt_pub_cloud_msg(client, prepare_gpio_pump_notification_message_obj("fer", "on", shelf_id))
        pump_ctrl("FER", "ON")
        time.sleep(ctrl_time_dict["ctrl_interval"])
        pump_ctrl("FER", "OFF")
        # mqtt_pub_cloud_msg(client,prepare_gpio_pump_notification_message_obj("fer", "off", shelf_id))

    elif (trigger_water(data,thres_dict)):
        if (int(data["fertilizer"]) == 0):
            print("\nALERT Cannot trigger water pump")
            mqtt_pub_cloud_msg(client, prepare_low_water_notification_message_obj("water", shelf_id))
            return
        else:
            mqtt_pub_cloud_msg(client, prepare_gpio_pump_notification_message_obj("water", "on", shelf_id))
            pump_ctrl("WATER", "ON")
            time.sleep(ctrl_time_dict["ctrl_interval"])
            pump_ctrl("WATER", "OFF")
            # mqtt_pub_cloud_msg(client, prepare_gpio_pump_notification_message_obj("water", "off", shelf_id))

    
