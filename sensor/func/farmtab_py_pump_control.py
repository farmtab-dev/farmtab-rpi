# https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
import subprocess
import os
import RPi.GPIO as GPIO
from config.cfg_py_sensor import PUMP_PIN, PUMP_CTRL_TYPE
from func.h_datetime_func import get_curr_datetime


def pump_ctrl(pump_type, action):
    if(PUMP_CTRL_TYPE=="USB"):
        control_pump_via_usb(pump_type, action)
    elif(PUMP_CTRL_TYPE=="GPIO"):
        control_pump_via_gpio(pump_type, action)
    elif(pump_type == "PI_USB"):
        if(action=="ON"): 
            return activate_usb_port()
        elif(action=="OFF"): 
            return deactivate_usb_port()

#================#
# PI USB control #
#================#
def activate_usb_port():
    #os.system("sudo echo '1-1' > '/sys/bus/usb/drivers/usb/bind'")
    return subprocess.getoutput("sudo echo '1-1' > '/sys/bus/usb/drivers/usb/bind'")

def deactivate_usb_port():
    #os.system("sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'")
    return subprocess.getoutput("sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'")

#=========================#
# GPIO control with relay #
#=========================#
def control_pump_via_gpio(pump_type, action):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    if (pump_type == "RESET"):
        GPIO.setup(PUMP_PIN["pinA"],GPIO.OUT)
        GPIO.setup(PUMP_PIN["pinB"],GPIO.OUT)
        GPIO.setup(PUMP_PIN["pinW"],GPIO.OUT)
        GPIO.cleanup(PUMP_PIN["all"])
        print(" >>> Off all pumps - "+str(get_curr_datetime()))
    elif (pump_type == "WATER"):
        GPIO.setup(PUMP_PIN["pinW"],GPIO.OUT)
        if (action == "ON"):
            print ("ON WATER_PUMP - "+str(get_curr_datetime()))
            GPIO.output(PUMP_PIN["pinW"],GPIO.LOW)
        else:
            print ("OFF WATER_PUMP - "+str((get_curr_datetime())))
            GPIO.cleanup(PUMP_PIN["pinW"])
    elif (pump_type == "FER"):
        GPIO.setup(PUMP_PIN["pinA"],GPIO.OUT)
        GPIO.setup(PUMP_PIN["pinB"],GPIO.OUT)
        if (action == "ON"):
            print ("ON FERTILILZER_PUMP - "+str(get_curr_datetime()))
            GPIO.output(PUMP_PIN["pinA"],GPIO.LOW)
            GPIO.output(PUMP_PIN["pinB"],GPIO.LOW)
        else:
            print ("OFF FERTILILZER_PUMP - "+str(get_curr_datetime()))
            GPIO.cleanup([PUMP_PIN["pinA"], PUMP_PIN["pinB"]])

#==============================#
# GPIO control with USB module #
#==============================#
def control_pump_via_usb(pump_type, action):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    if (pump_type == "RESET"):
        GPIO.setup(PUMP_PIN["pinA"],GPIO.OUT)
        GPIO.setup(PUMP_PIN["pinB"],GPIO.OUT)
        GPIO.setup(PUMP_PIN["pinW"],GPIO.OUT)
        GPIO.output(PUMP_PIN["pinA"],GPIO.LOW)
        GPIO.output(PUMP_PIN["pinB"],GPIO.LOW)
        GPIO.output(PUMP_PIN["pinW"],GPIO.LOW)
        GPIO.cleanup(PUMP_PIN["all"])
        print(" >>> Off all pumps - "+str(get_curr_datetime()))
    elif (pump_type == "WATER"):
        GPIO.setup(PUMP_PIN["pinW"],GPIO.OUT)
        if (action == "ON"):
            print ("ON WATER_PUMP - "+str(get_curr_datetime()))
            GPIO.output(PUMP_PIN["pinW"],GPIO.HIGH)
        else:
            print ("OFF WATER_PUMP - "+str((get_curr_datetime())))
            GPIO.output(PUMP_PIN["pinW"],GPIO.LOW)
            GPIO.cleanup([PUMP_PIN["pinW"]])
    elif (pump_type == "FER"):
        GPIO.setup(PUMP_PIN["pinA"],GPIO.OUT)
        GPIO.setup(PUMP_PIN["pinB"],GPIO.OUT)
        if (action == "ON"):
            print ("ON FERTILILZER_PUMP - "+str(get_curr_datetime()))
            GPIO.output(PUMP_PIN["pinA"],GPIO.HIGH)
            GPIO.output(PUMP_PIN["pinB"],GPIO.HIGH)
        else:
            print ("OFF FERTILILZER_PUMP - "+str(get_curr_datetime()))
            GPIO.output(PUMP_PIN["pinA"],GPIO.LOW)
            GPIO.output(PUMP_PIN["pinB"],GPIO.LOW)
            GPIO.cleanup([PUMP_PIN["pinA"], PUMP_PIN["pinB"]])
