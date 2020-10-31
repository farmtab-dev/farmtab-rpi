#!/usr/bin/env python3
# pip3 install -r requirements.txt
import datetime
from time import sleep
import os
import tinys3


import schedule  # https://pypi.org/project/schedule/
# import yaml  # pip install pyyaml https://github.com/yaml/pyyaml/issues/291
# import boto3

# # client = boto3.client('kinesisvideo')
# s3_client = boto3.client('s3')
from config.cfg_py_camera import CAM_SERIAL, SEND_IMG_HOUR, TIME_INTERVAL, DEBUG, S3_CFG, FILE_CFG, IMG_CFG, TOTAL_CAM, CAM_SLOT_OBJ, CAM_SLOT_LIST, CAM_NEED_ROTATE, CAP_TIMEOUT

from h_cam_handler import getCamFilepath, changeCam, printDebug, captureImg, timeNow, get4X4ImgMerged, uploadAllToS3

print("Total Camera :", TOTAL_CAM, " => ", CAM_SLOT_OBJ)


def main():
    # schedule.every().hour.at(":00").do(uploadAllToS3)
    # endlessly capture images awwyiss
    i = 0
    isInit = True
    while True:
        # schedule.run_pending()

        # Set curr Camera Slot
        camLvl = CAM_SLOT_LIST[i]
        currCamSlot = CAM_SLOT_OBJ[camLvl]
        print("\nCurrent [ " + camLvl + " ] camera - [ Slot_" +
              currCamSlot + " ] - Rotate - "+str(CAM_NEED_ROTATE[camLvl]))

        # Build filename string
        filepath = getCamFilepath(i)

        # Change & Take Photo
        changeCam(currCamSlot, isInit)
        isInit = False
        printDebug("Changed cam slot")
        sleep(TIME_INTERVAL["cap_img"])
        printDebug("Start Capturing " + str(timeNow()))
        captureImg(filepath, IMG_CFG["width"], IMG_CFG["height"],
                   CAM_NEED_ROTATE[camLvl], currCamSlot, CAP_TIMEOUT)
        printDebug('Taking photo and saving to path ' +
                   filepath + " "+str(timeNow()))

        # Upload to S3
        # uploadToS3(filepath)

        # Cleanup
        # if os.path.exists(filepath):
        #     os.remove(filepath)

        # sleep
        i += 1
        if (i >= len(CAM_SLOT_LIST)):
            print("Updated all camera stream - ", timeNow())
            i = 0
            # Upload ALL CAM to S3
            if (timeNow().minute in []):
                fp = get4X4ImgMerged(img_cfg=IMG_CFG, file_cfg={
                    "dirpath": FILE_CFG["dirpath"],
                    "fpA": getCamFilepath(0), "fpB": getCamFilepath(1), "fpC": getCamFilepath(2), "fpD": getCamFilepath(3)})
                uploadAllToS3()

        sleep(TIME_INTERVAL["chg_cam"])


main()
