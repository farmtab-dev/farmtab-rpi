#!/usr/bin/env python3

# pm2 start /opt/farmtab-rpi/sensor/start_pi_arduino_publisher.py --interpreter=python3 --cron "0 * * * *"
import paho.mqtt.client as mqtt
from func.h_mqtt_publisher_ver2 import mqtt_main
from config.cfg_py_mqtt_topic import SUB_TOPIC_LIST
from config.cfg_py_serial import SEN_SERIAL

comm_with = "Cloud <==> " + SEN_SERIAL
topic_list = SUB_TOPIC_LIST["TUNE"]

mqtt_main(comm_with, topic_list)