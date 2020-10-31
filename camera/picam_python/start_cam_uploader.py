#!/usr/bin/env python3
# pip3 install -r requirements.txt
from time import sleep
import schedule  # https://pypi.org/project/schedule/
import datetime
import os
import tinys3


# import yaml  # pip install pyyaml https://github.com/yaml/pyyaml/issues/291
# import boto3

# # client = boto3.client('kinesisvideo')
# s3_client = boto3.client('s3')
from config.cfg_py_camera import CAM_SERIAL, SEND_IMG_HOUR, TIME_INTERVAL, DEBUG, S3_CFG, FILE_CFG, IMG_CFG, TOTAL_CAM, CAM_SLOT_OBJ, CAM_SLOT_LIST, CAM_NEED_ROTATE, CAP_TIMEOUT
from .h_cam_handler import uploadAllToS3


# verify image folder exists and create if it does not
if not os.path.exists(FILE_CFG["dirpath"]):
    os.makedirs(FILE_CFG["dirpath"])


print("Total Camera :", TOTAL_CAM, " => ", CAM_SLOT_OBJ)


def main():

    schedule.every().hour.at(":00").do(uploadAllToS3)

    while True:
        schedule.run_pending()
        sleep(TIME_INTERVAL["chg_cam"])


main()
