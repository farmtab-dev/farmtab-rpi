# https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
import subprocess
import os
import RPi.GPIO as GPIO
from config.cfg_farmtab_parameter import PUMP_PIN

def activate_usb_port():
    #os.system("sudo echo '1-1' > '/sys/bus/usb/drivers/usb/bind'")
    return subprocess.getoutput("sudo echo '1-1' > '/sys/bus/usb/drivers/usb/bind'")

def deactivate_usb_port():
    #os.system("sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'")
    return subprocess.getoutput("sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'")


def control_pump_via_gpio(pump_type, action):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    if (pump_type == "RESET"):
        GPIO.setup(PUMP_PIN["pinA"],GPIO.OUT)
        GPIO.setup(PUMP_PIN["pinB"],GPIO.OUT)
        GPIO.setup(PUMP_PIN["pinW"],GPIO.OUT)
        GPIO.output(PUMP_PIN["pinA"],GPIO.LOW)
        GPIO.output(PUMP_PIN["pinB"],GPIO.LOW)
        GPIO.output(PUMP_PIN["pinW"],GPIO.LOW)
    elif (pump_type == "WATER"):
        GPIO.setup(PUMP_PIN["pinW"],GPIO.OUT)
        if (action == "ON"):
            print ("ON WATER_PUMP")
            GPIO.output(PUMP_PIN["pinW"],GPIO.HIGH)
        else:
            print ("OFF WATER_PUMP")
            GPIO.output(PUMP_PIN["pinW"],GPIO.LOW)
    elif (pump_type == "FER"):
        GPIO.setup(PUMP_PIN["pinA"],GPIO.OUT)
        GPIO.setup(PUMP_PIN["pinB"],GPIO.OUT)
        if (action == "ON"):
            print ("ON FERTILILZER_PUMP")
            GPIO.output(PUMP_PIN["pinA"],GPIO.HIGH)
            GPIO.output(PUMP_PIN["pinB"],GPIO.HIGH)
        else:
            print ("OFF FERTILILZER_PUMP")
            GPIO.output(PUMP_PIN["pinA"],GPIO.LOW)
            GPIO.output(PUMP_PIN["pinB"],GPIO.LOW)