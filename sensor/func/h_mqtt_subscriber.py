# http://www.steves-internet-guide.com/into-mqtt-python-client/
#!/usr/bin/env python3
import paho.mqtt.client as mqtt  # pip3 install paho-mqtt
from config.cfg_py_server import MQTT_USERNAME, MQTT_PASSWORD, MQTT_SERVER, MQTT_PORT, MQTT_KEEPALIVE, MQTT_ENABLE_AUTH
from config.cfg_py_serial import SEN_SERIAL
from func.mqtt_sub_msg_handler import mqtt_msg_handler_main

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

    #-------------------------------------------------------------------------#
    #  Perform checking & required action based on incoming msg & mqtt topic  #
    #-------------------------------------------------------------------------#
    mqtt_msg_handler_main(client,msg.topic,incoming_mqtt_msg)
    

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

    global SUBSCRIBE_TOPIC
    global COMMUNICATE_WITH
    SUBSCRIBE_TOPIC = topic_list
    COMMUNICATE_WITH = comm_with

    print("Total MQTT topic to subscribe : " + str(len(SUBSCRIBE_TOPIC)))
    print("Topic to subscribe : " + str(len(SUBSCRIBE_TOPIC)))

    client = mqtt.Client(client_id="RPi_"+SEN_SERIAL+"-"+str(comm_with))
    if (MQTT_ENABLE_AUTH):
        client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
    client.on_connect = on_connect  # attach function to callback
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    #client.on_log = on_log

    #----------------------------#
    # Establish MQTT Connection  #
    #----------------------------#
    client.connect(MQTT_SERVER, MQTT_PORT, MQTT_KEEPALIVE)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
