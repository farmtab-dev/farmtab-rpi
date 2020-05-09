from func.farmtab_py_pump_control import activate_usb_port, deactivate_usb_port, control_pump_via_gpio
from func.h_datetime_func import get_curr_datetime, get_time_difference_in_sec
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
    thres_obj["thres_orp_min"] = new_thres["thres_co2_min"]
    thres_obj["thres_orp_max"] = new_thres["thres_co2_max"]
    print("SUCCESS update threshold")


#==========================#
#  Check THRESHOLD  #
#==========================#
def check_threshold(client, ctrl_time_dict, curr_pump_dict, thres_dict, data):
    # Either Water / Fertilizer is activated
    if (curr_pump_dict["WATER"] or curr_pump_dict["FER"]):
        # Check for activation duration
        curr_time = get_curr_datetime()
        time_elapse = get_time_difference_in_sec(ctrl_time_dict["last_ctrl"], curr_time)
        if (time_elapse < ctrl_time_dict["ctrl_interval"]):
            print (ctrl_time_dict["ctrl_pump"] + " PUMP ON for " + str(time_elapse))
            return 
        print (curr_pump_dict)
        
        control_pump_via_gpio(ctrl_time_dict["ctrl_pump"], "OFF")
        curr_pump_dict[ctrl_time_dict["ctrl_pump"]] = False
        ctrl_time_dict["ctrl_pump"] = None
        ctrl_time_dict["last_ctrl"] = None
 

    print ("\nCHECK_THRES ==> PH:" + str(data["ph"]) + "("+str(thres_dict["thres_ph_min"]) +"-"+ str(thres_dict["thres_ph_max"])+") \t"+
           "ORP:" + str(data["orp"]) + "("+str(thres_dict["thres_orp_min"]) +"-"+ str(thres_dict["thres_orp_max"])+")")
    if (ctrl_time_dict["last_check"] is not None):
        # Check for activation duration
        curr_time = get_curr_datetime()
        time_elapse = get_time_difference_in_sec(ctrl_time_dict["last_check"], curr_time)
        if (time_elapse < ctrl_time_dict["check_interval"]):
            print ("    Delay checks for " + str(time_elapse))
            return 

    ctrl_time_dict["last_check"] = get_curr_datetime()
    if (data["ph"] <= thres_dict["thres_ph_min"] and data["orp"] <= thres_dict["thres_orp_min"] ):
        ctrl_time_dict["last_ctrl"] = get_curr_datetime()
        ctrl_time_dict["ctrl_pump"] = "FER"
        curr_pump_dict[ctrl_time_dict["ctrl_pump"]] = True
        control_pump_via_gpio(ctrl_time_dict["ctrl_pump"], "ON")
        
    elif (data["ph"] >=thres_dict["thres_ph_max"] and data["orp"] >=thres_dict["thres_orp_max"]):
        ctrl_time_dict["last_ctrl"] = get_curr_datetime()
        ctrl_time_dict["ctrl_pump"] = "WATER"
        curr_pump_dict[ctrl_time_dict["ctrl_pump"]] = True
        control_pump_via_gpio(ctrl_time_dict["ctrl_pump"], "ON")
            
    #mqtt_pub_msg(client, PUB_CLOUD_TOPIC['pub_data'], str(data))
    