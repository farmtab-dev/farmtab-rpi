#!/usr/bin/env python3
# http://www.steves-internet-guide.com/into-mqtt-python-client/
# USING AWS IOT : https://www.balena-staging.io/docs/learn/develop/integrations/aws/ 
import paho.mqtt.client as mqtt  # pip3 install paho-mqtt
import certifi  # pip3 install certifi
import ssl
import time
#import asyncio
#import aioschedule as schedule
#https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
import schedule  # https://pypi.org/project/schedule/
import serial  # https://pyserial.readthedocs.io/en/latest/shortintro.html
import config.cfg_py_server as CPS
import config.cfg_py_sensor as CFP
from func.mqtt_pub_msg_handler import  get_pub_sensor_data, tune_parameter, check_thres_pub_sensor_data, get_store_sensor_data
from func.h_datetime_func import get_curr_datetime, get_time_difference_in_sec
from func.farmtab_py_pump_control import control_pump_via_gpio
from func.h_api_func import sync_cloud_thres_info
from func.h_conversion_func import encode_obj_to_json

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

#--------------------------#
#  MQTT On Connect - Local #
#--------------------------#
# The callback for when the client receives a CONNACK response from the server.
def on_local_connect(l_client, userdata, flags, rc):
    print("\nSuccessful MQTT local connection with result code "+str(rc))

    l_client.subscribe("/local/req_data/#")    # For sample data request
    l_client.subscribe("/local/calibrate/#")   # For calibrate sensor 
    # l_client.subscribe("/local/sensor_cmd/#")   # For calibrate sensor - Delay

#======================#
#  MQTT On Disconnect  #
#======================#
#http://www.steves-internet-guide.com/loop-python-mqtt-client/
def on_disconnect(client, userdata,rc=0):
    print("Disconnected result code "+str(rc))
    client.loop_stop()
#-----------------------------#
#  MQTT On Disconnect - Local #
#-----------------------------#
def on_local_disconnect(l_client, userdata,rc=0):
    print("Disconnected result code "+str(rc))
    l_client.loop_stop()

#===================#
#  MQTT On Publish  #
#===================#
# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, mid):
    print("Message Published... mid: " + str(mid))

#--------------------------#
#  MQTT On Publish - Local #
#--------------------------#
def on_local_publish(l_client, userdata, mid):
    print("Message Published locally... mid: " + str(mid))


#=====================#
#  MQTT On Subscribe  #
#=====================#
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribe... mid: " + str(mid))

    if (len(SUBSCRIBE_TOPIC) == mid):
        print("Successful subscribe : " + str(SUBSCRIBE_TOPIC))

#----------------------------#
#  MQTT On Subscribe - Local #
#----------------------------#
def on_local_subscribe(l_client, userdata, mid, granted_qos):
    print("Subscribe... mid: " + str(mid))


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


#----------------------------#
#  MQTT On Subscribe - Local #
#----------------------------#
def on_local_message(l_client, userdata, msg):
    incoming_mqtt_msg = str(msg.payload.decode("utf-8"))  # Convert to string (unicode)
    print(msg.topic + " " + incoming_mqtt_msg)

    mqtt_topic_token = msg.topic.split("/")
    if (mqtt_topic_token[2] == 'req_data'):   # REQUEST SAMPLE DATA
        temp = READ_SERIAL["data"].decode('utf-8')
        pub_sample_data = { 
            "socket":mqtt_topic_token[-1], 
            "disconnect":incoming_mqtt_msg, 
            "sensor":temp
            }
        pub_sample_data = encode_obj_to_json(pub_sample_data)
        l_client.publish("/local/res_data", str(pub_sample_data), 0)
    elif (mqtt_topic_token[2] == 'calibrate'):   # CALIBRATE
        print("Calibrate message ", incoming_mqtt_msg)
        if (mqtt_topic_token[-1] == C_SOCKET["sid"] or C_SOCKET["sid"]==""):
            C_SOCKET["sid"] = mqtt_topic_token[-1]  # Update the SOCKET ID
            if (incoming_mqtt_msg=="INIT"):  # Handle initial request 
                pub_calibration_msg(l_client,mqtt_topic_token[-1],False, "INIT_CALIBRATION", "Established connection for calibration")
                print("\nCALIBRATION => Init command")
            elif (incoming_mqtt_msg=="CLOSE"):  # Handle initial request 
                C_SOCKET["sid"] = ""
                print("\nCALIBRATION => Close calibration")
            else:
                # https://pyserial.readthedocs.io/en/latest/shortintro.html
                # https://stackoverflow.com/questions/53260841/sending-serial-data-to-arduino-using-python-script
                SER.write(incoming_mqtt_msg.encode()) 
                print("\nCALIBRATION => Write command ", incoming_mqtt_msg.encode())
        else:
            pub_calibration_msg(l_client,mqtt_topic_token[-1], True,"DUP_CALIBRATION","Another instance is calibrating.")
    # elif (mqtt_topic_token[2] == 'sensor_cmd'):   # CALIBRATE CMD
    #     # https://pyserial.readthedocs.io/en/latest/shortintro.html
    #     # https://stackoverflow.com/questions/53260841/sending-serial-data-to-arduino-using-python-script
    #     SER.write(incoming_mqtt_msg.encode()) 
    #     print("\nCALIBRATION => Write command ", incoming_mqtt_msg.encode())

#===============#
#  MQTT On Log  #
#===============#
def on_log(client, userdata, level, buf):
    print("log: ", buf)

#===============#
#  READ SERIAL  #
#===============#
def pub_calibration_msg(l_client,socket, disconnect, c_stat, c_msg):
    pub_sample_data = { 
            "socket":socket, 
            "disconnect": disconnect, 
            "c_stat": c_stat,
            "c_msg": c_msg,
    }
    print("Publish locally")
    pub_sample_data = encode_obj_to_json(pub_sample_data)
    l_client.publish("/local/res_calibrate", str(pub_sample_data), 0)

def readSerialAndPub(client, l_client):
    read_serial=SER.readline()   
    READ_SERIAL["data"] = read_serial
    print("ARDUINO ==> ", READ_SERIAL["data"])
    #read_serial="PH@5#TEMP@25#EC@20"  
    # Check whether it is valid data before proceed to PROCESS + STORE
    s = READ_SERIAL["data"].decode('utf-8')
    if ("#" in s):
        data = get_store_sensor_data(client, PUB_TIME_DICT, CURR_PUMP_DICT, READ_SERIAL["data"])
    
    if (C_SOCKET["sid"]!=""):
        pub_calibration_msg(l_client,C_SOCKET["sid"], False, "REPLY_CALIBRATION", s)

#=================#
#  MAIN FUNCTION  #
#=================#
def mqtt_main(comm_with, topic_list):
    print("\nCommunicate with - "+str(comm_with))
    print("Subscribing MQTT Topic - "+str(topic_list))
    control_pump_via_gpio("RESET", "OFF")


    global SUBSCRIBE_TOPIC
    global COMMUNICATE_WITH
    global PUB_TIME_DICT
    global CTRL_TIME_DICT
    global THRESHOLD_DICT
    global CURR_PUMP_DICT
    global READ_SERIAL
    global SER
    global C_SOCKET

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

    client = mqtt.Client(client_id= "RPi_"+CFP.SEN_SERIAL+"-"+str(comm_with))
    l_client = mqtt.Client(client_id= "RPi_"+CFP.SEN_SERIAL+"- local")

    #-----------------------------#
    # MQTT Authentication Method  #
    #-----------------------------#
    if (CPS.MQTT_ENABLE_AUTH):
        if (CPS.MQTT_AUTH_METHOD == "password"):
                client.username_pw_set(CPS.MQTT_USERNAME, password=CPS.MQTT_PASSWORD)
        

    #----------------------------------#
    # Attach Callback Function - CLOUD #
    #----------------------------------#
    client.on_connect   = on_connect  
    client.on_message   = on_message
    client.on_publish   = on_publish
    client.on_subscribe = on_subscribe
    # client.on_log = on_log
    #----------------------------------#
    # Attach Callback Function - LOCAL #
    #----------------------------------#
    l_client.on_connect   = on_local_connect  
    l_client.on_message   = on_local_message
    l_client.on_publish   = on_local_publish
    l_client.on_subscribe = on_local_subscribe

    #----------------------------#
    # Establish MQTT Connection  #
    #----------------------------#
    client.connect(CPS.MQTT_CLOUD_SERVER, CPS.MQTT_PORT, CPS.MQTT_KEEPALIVE)
    l_client.connect(CPS.MQTT_LOCAL_SERVER, CPS.MQTT_PORT, CPS.MQTT_KEEPALIVE)
    # if (CPS.MQTT_SERVER_TYPE == "cloud"):
    #     client.connect(CPS.MQTT_CLOUD_SERVER, CPS.MQTT_PORT, CPS.MQTT_KEEPALIVE)
    # else:
    #     client.connect(CPS.MQTT_LOCAL_SERVER, CPS.MQTT_PORT, CPS.MQTT_KEEPALIVE)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.   

    schedule.every().hour.at(":00").do(check_thres_pub_sensor_data,client, CTRL_TIME_DICT, CURR_PUMP_DICT,THRESHOLD_DICT)
    # schedule.every().minute.at(":30").do(check_thres_pub_sensor_data,client, CTRL_TIME_DICT, CURR_PUMP_DICT,THRESHOLD_DICT) # For debugging
    #---------------#  Get ShelfID - To ensure it is assigned
    # RUN API CALLS #  Get Threshold - If not set, add one
    #---------------#
    need_resync = sync_cloud_thres_info(CFP.SEN_SERIAL, THRESHOLD_DICT) 
    last_resync_check = None
    
    #--------------------#
    # Endless Publisher  #  https://stackoverflow.com/questions/23909292/publish-a-message-every-10-seconds-mqtt
    #--------------------#
    SER = serial.Serial('/dev/ttyACM0', CFP.ARDUINO_BRAUD_RATE)
    C_SOCKET = {"sid": ""}
    client.loop_start()
    l_client.loop_start()
    read_serial = ""
    READ_SERIAL = { "data":read_serial }
    while True:
        readSerialAndPub(client, l_client)
        schedule.run_pending()
        #data = get_pub_sensor_data(client, PUB_TIME_DICT, CURR_PUMP_DICT, read_serial)
        
        # check_threshold(client, CTRL_TIME_DICT, CURR_PUMP_DICT,THRESHOLD_DICT, data)
        if (need_resync):   # Check once per 300 seconds
            if (last_resync_check is not None):
                curr_time = get_curr_datetime()
                time_elapse = get_time_difference_in_sec(last_resync_check, curr_time)

                if (time_elapse < 300): 
                    continue
            last_resync_check = get_curr_datetime()
            need_resync = sync_cloud_thres_info(CFP.SEN_SERIAL, THRESHOLD_DICT) 
        # else:
        #     # schedule.run_pending()
                        
        #     #data = get_pub_sensor_data(client, PUB_TIME_DICT, CURR_PUMP_DICT, read_serial)
        #     data = get_store_sensor_data(client, PUB_TIME_DICT, CURR_PUMP_DICT, read_serial)
        #     check_threshold(client, CTRL_TIME_DICT, CURR_PUMP_DICT,THRESHOLD_DICT, data)
        #     time.sleep(50)
        
    #client.loop_forever()
    
