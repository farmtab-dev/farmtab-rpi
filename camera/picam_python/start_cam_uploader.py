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
from h_cam_handler import uploadAllToS3, sync_cloud_cam_pos, get_curr_datetime, get_time_difference_in_sec


# verify image folder exists and create if it does not
if not os.path.exists(FILE_CFG["dirpath"]):
    os.makedirs(FILE_CFG["dirpath"])


print("Total Camera :", TOTAL_CAM, " => ", CAM_SLOT_OBJ)


def main():
    # need_resync = sync_cloud_cam_pos()
    # last_resync_check = None

    schedule.every().hour.at(":00").do(uploadAllToS3)

    while True:
        # if (need_resync):   # Check once per 300 seconds
        #     if (last_resync_check is not None):
        #         curr_time = get_curr_datetime()
        #         time_elapse = get_time_difference_in_sec(
        #             last_resync_check, curr_time)

        #         if (time_elapse < 300):
        #             continue
        #     last_resync_check = get_curr_datetime()
        #     need_resync = sync_cloud_cam_pos()
        schedule.run_pending()
        sleep(TIME_INTERVAL["chg_cam"])


main()
