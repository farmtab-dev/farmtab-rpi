# http://www.steves-internet-guide.com/into-mqtt-python-client/
# USING AWS IOT : https://www.balena-staging.io/docs/learn/develop/integrations/aws/ 
#!/usr/bin/env python3
import paho.mqtt.client as mqtt  # pip3 install paho-mqtt
import certifi  # pip3 install certifi
import ssl
import time
#import asyncio
#import aioschedule as schedule
#https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
import schedule  # https://pypi.org/project/schedule/
import serial
import config.cfg_py_server as CPS
import config.cfg_farmtab_parameter as CFP
from config.cfg_py_serial import SEN_SERIAL
from func.mqtt_pub_msg_handler import  get_pub_sensor_data, tune_parameter, pub_sensor_data, get_store_sensor_data
from func.farmtab_py_threshold import  check_threshold
from func.h_datetime_func import get_curr_datetime, get_time_difference_in_sec
from func.farmtab_py_pump_control import control_pump_via_gpio
from func.h_api_func import sync_cloud_thres_info
#===================#
#  MQTT On Connect  #
#===================#
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("\nSuccessful MQTT connection with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in SUBSCRIBE_TOPIC:
        client.subscribe(topic)    

#======================#
#  MQTT On Disconnect  #
#======================#
#http://www.steves-internet-guide.com/loop-python-mqtt-client/
def on_disconnect(client, userdata,rc=0):
    logging.debug("Disconnected result code "+str(rc))
    client.loop_stop()

#===================#
#  MQTT On Publish  #
#===================#
# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print("Message Published... mid: " + str(mid))


#=====================#
#  MQTT On Subscribe  #
#=====================#
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribe... mid: " + str(mid))

    if (len(SUBSCRIBE_TOPIC) == mid):
        print("Successful subscribe : " + str(SUBSCRIBE_TOPIC))

#===================#
#  MQTT On Message  #
#===================#
def on_message(client, userdata, msg):
    incoming_mqtt_msg = str(msg.payload.decode("utf-8"))  # Convert to string (unicode)
    print(msg.topic + " " + incoming_mqtt_msg)

    #----------------------------------#
    #  CHANGE PARAMETER BASED ON INPUT #
    #----------------------------------#
    curr_parameter = {"pub": PUB_TIME_DICT, "thres":CTRL_TIME_DICT, "threshold": THRESHOLD_DICT, "pump": CURR_PUMP_DICT}
    new_parameter = tune_parameter(client, msg.topic, incoming_mqtt_msg, curr_parameter)


#===============#
#  MQTT On Log  #
#===============#
def on_log(client, userdata, level, buf):
    print("log: ", buf)

#=================#
#  MAIN FUNCTION  #
#=================#
def mqtt_main(comm_with, topic_list):
    print("\nCommunicate with - "+str(comm_with))
    print("Subscribing MQTT Topic - "+str(topic_list))
    print(" >>> Off all pumps")
    control_pump_via_gpio("RESET", "OFF")


    global SUBSCRIBE_TOPIC
    global COMMUNICATE_WITH
    global PUB_TIME_DICT
    global CTRL_TIME_DICT
    global THRESHOLD_DICT
    global CURR_PUMP_DICT

    SUBSCRIBE_TOPIC = topic_list
    COMMUNICATE_WITH = comm_with
    PUB_TIME_DICT = {"pub_interval": CFP.PUB_DATA_INTERVAL_IN_SEC, 
                     "store_interval": CFP.STORE_DATA_INTERVAL_IN_SEC, 
                     "last_pub":None, "last_store":None}
    CTRL_TIME_DICT = {"check_interval": CFP.CHECK_INTERVAL_IN_SEC, 
                      "ctrl_interval": CFP.CTRL_INTERVAL_IN_SEC, 
                      "last_check":None,
                      "last_ctrl":None,
                      "ctrl_pump":None,
                      "ctrl_method":"AUTO",
                      }
    THRESHOLD_DICT = CFP.THRESHOLD_DICT
    CURR_PUMP_DICT = CFP.CURR_PUMP_STAT

    print("Total MQTT topic to subscribe : " + str(len(SUBSCRIBE_TOPIC)))
    print("Topic to subscribe : " + str(len(SUBSCRIBE_TOPIC)))

    client = mqtt.Client(client_id= "RPi_"+SEN_SERIAL+"-"+str(comm_with))

    #-----------------------------#
    # MQTT Authentication Method  #
    #-----------------------------#
    if (CPS.MQTT_ENABLE_AUTH):
        if (CPS.MQTT_AUTH_METHOD == "password"):
                client.username_pw_set(CPS.MQTT_USERNAME, password=CPS.MQTT_PASSWORD)
        

    #---------------------------#
    # Attach Callback Function  #
    #---------------------------#
    client.on_connect = on_connect  
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    # client.on_log = on_log

    #----------------------------#
    # Establish MQTT Connection  #
    #----------------------------#
    if (CPS.MQTT_SERVER_TYPE == "cloud"):
        client.connect(CPS.MQTT_CLOUD_SERVER, CPS.MQTT_PORT, CPS.MQTT_KEEPALIVE)
    else:
        client.connect(CPS.MQTT_LOCAL_SERVER, CPS.MQTT_PORT, CPS.MQTT_KEEPALIVE)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.   

    #schedule.every().hour.at(":00").do(pub_sensor_data,client)
    schedule.every().minute.at(":31").do(pub_sensor_data,client)
    #---------------#  Get ShelfID - To ensure it is assigned
    # RUN API CALLS #  Get Threshold - If not set, add one
    #---------------#
    need_resync = sync_cloud_thres_info(SEN_SERIAL, THRESHOLD_DICT) 
    last_resync_check = None
    
    #--------------------#
    # Endless Publisher  #  https://stackoverflow.com/questions/23909292/publish-a-message-every-10-seconds-mqtt
    #--------------------#
    # ser = serial.Serial('/dev/ttyACM0', CFP.ARDUINO_BRAUD_RATE)
    client.loop_start()
    while True:
        if (need_resync):
            if (last_resync_check is not None):
                curr_time = get_curr_datetime()
                time_elapse = get_time_difference_in_sec(last_resync_check, curr_time)

                if (time_elapse < 300):
                    continue
            last_resync_check = get_curr_datetime()
            need_resync = sync_cloud_thres_info(SEN_SERIAL, THRESHOLD_DICT) 
        else:
            schedule.run_pending()
        #    read_serial=ser.readline()   
            read_serial="PH@5#TEMP@25#EC@20#ORP@20"  
            
            #data = get_pub_sensor_data(client, PUB_TIME_DICT, CURR_PUMP_DICT, read_serial)
            data = get_store_sensor_data(client, PUB_TIME_DICT, CURR_PUMP_DICT, read_serial)
            check_threshold(client, CTRL_TIME_DICT, CURR_PUMP_DICT,THRESHOLD_DICT, data)
            time.sleep(50)
        
    #client.loop_forever()
    
