import RPi.GPIO as gp
import os
from time import sleep
def changeCam(cam, isInit= False):
    if (not isInit):
        gp.cleanup()
    gp.setwarnings(True)
    gp.setmode(gp.BOARD)

    gp.setup(7, gp.OUT)
    gp.setup(11, gp.OUT)
    gp.setup(12, gp.OUT)
    gp.setup(15, gp.OUT)
    gp.setup(16, gp.OUT)
    gp.setup(21, gp.OUT)
    gp.setup(22, gp.OUT)

    gp.output(11, True)
    gp.output(12, True)
    gp.output(15, True)
    gp.output(16, True)
    gp.output(21, True)
    gp.output(22, True)
    if (cam=="A"):
        print("Change to camera A")
        i2c = "i2cset -y 1 0x70 0x00 0x04"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)
    elif(cam=="B"):
        print("Change to camera B"   )
        i2c = "i2cset -y 1 0x70 0x00 0x05"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, False)
        gp.output(12, True)
    elif(cam=="C"):
        print("Change to camera C")
        i2c = "i2cset -y 1 0x70 0x00 0x06"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, True)
        gp.output(12, False)
    elif(cam=="D"):
        print("Change to camera D")
        i2c = "i2cset -y 1 0x70 0x00 0x07"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, True)
        gp.output(12, False)
    

# https://www.raspberrypi.org/forums/viewtopic.php?t=56086
#https://www.raspberrypi.org/forums/viewtopic.php?t=67175#:~:text=raspistill%20will%20exit%20after%205s,0%22%20to%20disable%20this%20timeout.
def captureImg(filepath, width, height, rotate, cam, cap_timeout):
    if (rotate):
        # cmd = "raspistill -t 0 -s -o "+ filepath + " -w " +str(width) +" -h "+ str(height)+" -rot 180"
        cmd = "raspistill -t "+str(cap_timeout)+" -o "+ filepath + " -w " +str(width) +" -h "+ str(height)+" -rot 180"
    else:
        # cmd = "raspistill  -t 0 -s -o "+ filepath + " -w " +str(width) +" -h "+ str(height)
        cmd = "raspistill  -t "+str(cap_timeout)+" -o "+ filepath + " -w " +str(width) +" -h "+ str(height)

    os.system(cmd)
    # sleep(3)
    # gp.cleanup()

