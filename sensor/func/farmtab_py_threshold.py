from func.farmtab_py_pump_control import activate_usb_port, deactivate_usb_port, control_pump_via_gpio
from func.h_datetime_func import get_curr_datetime, get_time_difference_in_sec
from func.farmtab_py_msg_prep import prepare_low_water_notification_message_obj, prepare_gpio_pump_notification_message_obj
from config.cfg_py_mqtt_topic import PUB_CLOUD_TOPIC
import time

def mqtt_pub_msg(client, topic, msg):
    client.publish(topic, msg, 0)
    print(topic)
    print(msg)

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
    print("SUCCESS update threshold - "+ str(thres_obj))


#==========================#
#  Check THRESHOLD  #
#==========================#       
def check_threshold(client, ctrl_time_dict, curr_pump_dict, thres_dict, data):
    print ("\nCHECK_THRES ==> "+
           "PH:" + str(data["ph"]) + "("+str(thres_dict["thres_ph_min"]) +"-"+ str(thres_dict["thres_ph_max"])+") \t"+
           "EC:" + str(data["ec"]) + "("+str(thres_dict["thres_ec_min"]) +"-"+ str(thres_dict["thres_ec_max"])+")")
    # if (ctrl_time_dict["last_check"] is not None):
    #     # Check for last check duration
    #     curr_time = get_curr_datetime()
    #     time_elapse = get_time_difference_in_sec(ctrl_time_dict["last_check"], curr_time)
    #     if (time_elapse < ctrl_time_dict["check_interval"]):
    #         print ("    Delay checks for " + str(time_elapse))
    #         return 

    # ctrl_time_dict["last_check"] = get_curr_datetime()
    shelf_id = thres_dict["shelf_id"]
    if (data["ph"] <= thres_dict["thres_ph_min"] or data["ec"] <= thres_dict["thres_ec_min"] ):
        if (int(data["wlvl1"])==0):
            print("\nALERT Cannot trigger fertilizer pump")
            msg_str = prepare_low_water_notification_message_obj("fer", shelf_id)
            mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(msg_str))
            return
        else:
            msg_str = prepare_gpio_pump_notification_message_obj("fer", "on", shelf_id)
            mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(msg_str))
            control_pump_via_gpio("FER", "ON")
            time.sleep(ctrl_time_dict["ctrl_interval"])
            control_pump_via_gpio("FER", "OFF")
            msg_str = prepare_gpio_pump_notification_message_obj("fer", "off", shelf_id)
            mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(msg_str))
        
    elif (data["ph"] >=thres_dict["thres_ph_max"] or data["ec"] >=thres_dict["thres_ec_max"]):
        if (int(data["wlvl2"])==0):
            print("\nALERT Cannot trigger water pump")
            msg_str = prepare_low_water_notification_message_obj("fer", shelf_id)
            mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(msg_str))
            return
        else:
            msg_str = prepare_gpio_pump_notification_message_obj("water", "on", shelf_id)
            mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(msg_str))
            control_pump_via_gpio("WATER", "ON")
            time.sleep(ctrl_time_dict["ctrl_interval"])
            control_pump_via_gpio("WATER", "OFF")
            msg_str = prepare_gpio_pump_notification_message_obj("water", "off", shelf_id)
            mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_msg'], str(msg_str))
            
    
