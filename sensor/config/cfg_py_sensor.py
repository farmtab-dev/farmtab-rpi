import os
ARDUINO_BRAUD_RATE = 9600         #BRAUD RATE for arduino Code
PUB_DATA_INTERVAL_IN_SEC = 3600000         # Waiting time before next publish
STORE_DATA_INTERVAL_IN_SEC = 300         # Waiting time before next storage
CTRL_INTERVAL_IN_SEC =  2       # Activation time duration
CHECK_INTERVAL_IN_SEC = 100       # Delay to check threshold 
CURR_PUMP_STAT = {
    "WATER":False,
    "FER":False
}

PUMP_CTRL_TYPE = "USB" # USB, PI_USB, GPIO
# sudo nano /boot/config.txt https://www.raspberrypi.org/documentation/configuration/config-txt/gpio.md
# gpio=5,6,22=op,dl
PUMP_PIN = {
    'pinW': 22,    # 3 (WiringPin)  - WATER (Nearest to casing)
    'pinA': 5,     # 21 (WiringPin) - A fertilizer (Middle)
    'pinB': 6,     # 22 (WiringPin) - B fertilizer 
    'all': [5,6,22]
}

#=====================================#  !IMPORTANT : Serial Number is unique globally
#  RASPBERRY PI Serial Number CONFIG  #
#=====================================#
SEN_SERIAL = os.environ.get('FARMTAB_SERIAL', "")

SEND_DATA_HOUR = [0, 3, 6, 9, 12, 15, 18, 21]

# Threshold 
DEFAULT_THRESHOLD = {
    'min': {
        'temperature': 0,
        'ph': 0,
        'ec': 0,
        'tds': 0,
        'orp': 0
    },
    'max': {
        'temperature': 100,
        'ph': 14,
        'ec': 100,
        'tds': 100,
        'orp': 100
    }
}

THRESHOLD_DICT = {
    "shelf_id": '',
    "thres_temp_min": 0,
    "thres_temp_max": 100,
    "thres_ph_min": 0,
    "thres_ph_max": 14,
    "thres_ec_min": 0,
    "thres_ec_max": 100,
    "thres_orp_min": 0,
    "thres_orp_max": 100
    # "orp_min": 400,
    # "orp_max": 500
}
# https://scienceinhydroponics.com/2017/03/what-is-an-orp-meter-and-why-is-it-useful-in-hydroponics.html
# THRESHOLD_OBJ_LIST = {
#     "temp_min": 20,
#     "temp_max": 25,
#     "ph_min": 6,
#     "ph_max": 6.5,
#     # "ph_min": 8,
#     # "ph_max": 8.5,
#     "ec_min": 0,
#     "ec_max": 0,
#     "orp_min": 300,
#     "orp_max": 500
#     # "orp_min": 400,
#     # "orp_max": 500
# }

VARIABLE_ID = {
     'gateway_id' : '@GATEWAY@',
     'control_id' : '@CTRL_ID@',
     'package' : '@PACKAGE@',
     'action' : '@ACTION@'
}