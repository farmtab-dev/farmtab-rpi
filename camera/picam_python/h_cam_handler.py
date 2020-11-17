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
from func.h_api_func import get_dev_type
from func.h_img_join_func import get4X4ImgMerged
from func.h_arducam_func import changeCam, captureImg
from config.cfg_py_camera import CAM_SERIAL, SEND_IMG_HOUR, TIME_INTERVAL, DEBUG, S3_CFG, FILE_CFG, IMG_CFG, TOTAL_CAM, CAM_SLOT_OBJ, CAM_SLOT_LIST, CAM_NEED_ROTATE, CAP_TIMEOUT, CAM_POSITION


# verify image folder exists and create if it does not
if not os.path.exists(FILE_CFG["dirpath"]):
    os.makedirs(FILE_CFG["dirpath"])


def timeNow():
    return datetime.datetime.now()


def get_curr_datetime():
    # --> https://stackoverflow.com/questions/25837452/python-get-current-time-in-right-timezone
    utc_dt = datetime.datetime.now(datetime.timezone.utc)  # UTC time
    # local time
    return datetime.datetime.strftime(utc_dt.astimezone(), "%Y-%m-%d %H:%M:%S%z")


def get_time_difference_in_sec(time1_in_utc, time2_in_utc):
    duration = datetime.datetime.strptime(
        time2_in_utc, "%Y-%m-%d %H:%M:%S%z") - datetime.datetime.strptime(time1_in_utc, "%Y-%m-%d %H:%M:%S%z")
    return duration.total_seconds()


def getCombinedDesc():
    res_str = ""
    for x in CAM_SLOT_LIST:
        res_str += CAM_SLOT_OBJ[x]
    return res_str


def getCamFilepath(cindex):
    return FILE_CFG["dirpath"] + '/' + CAM_SLOT_LIST[cindex].upper() + "_" + CAM_POSITION + FILE_CFG["imgfile_ext"] if cindex < len(CAM_SLOT_LIST) else "NONE"


def getCamDupFilepath(cindex):
    return FILE_CFG["dirpath"] + '/' + CAM_SLOT_LIST[cindex].upper() + "_" + CAM_POSITION + "_copy" + FILE_CFG["imgfile_ext"] if cindex < len(CAM_SLOT_LIST) else "NONE"


def uploadToS3(filepath, cam_lvl, cam_slot):
    conn = tinys3.Connection(
        S3_CFG['access_key_id'], S3_CFG['secret_access_key'])
    f = open(filepath, 'rb')
    t = conn.upload(filepath, f, S3_CFG['bucket_name'],
                    headers={
        'x-amz-meta-cache-control': 'max-age=60',
        'x-amz-meta-farmtab-serial-number': CAM_SERIAL,
        'x-amz-meta-farmtab-cam-position': CAM_POSITION,
        'x-amz-meta-farmtab-cam-slot': cam_slot,
        'x-amz-meta-farmtab-cam-datetime': get_curr_datetime(),
        'x-amz-meta-farmtab-img-coordinate-code': cam_lvl
    })
    print(t)

    printDebug('Uploaded ' + filepath + ' to s3 [' + S3_CFG['bucket_name']+']')


def uploadAllToS3():
    if (timeNow().hour not in SEND_IMG_HOUR):
        print("INFO - NOT UPLOAD TIME YET - ", timeNow())
        print("Upload HOURS - ", SEND_IMG_HOUR)
        return
    print("INFO - UPLOADING to S3 ", timeNow())
    # for x in CAM_SLOT_LIST:
    #     f = FILE_CFG["dirpath"] + '/'+ x + FILE_CFG["imgfile_ext"]
    for i in range(len(CAM_SLOT_LIST)):
        camLvl = CAM_SLOT_LIST[i]
        uploadToS3(getCamDupFilepath(i), camLvl.upper(), CAM_SLOT_OBJ[camLvl])

    fp = get4X4ImgMerged(img_cfg=IMG_CFG, file_cfg={
        "dirpath": FILE_CFG["dirpath"],
        "fpA": getCamDupFilepath(0), "fpB": getCamDupFilepath(1), "fpC": getCamDupFilepath(2), "fpD": getCamDupFilepath(3)})
    uploadToS3(fp, "COMBINED", getCombinedDesc())
    print("SUCCESS - DONE UPLOADED")
    print("Upload HOURS - ", SEND_IMG_HOUR)


def printDebug(msg):
    if DEBUG == True:
        print("\t [debug] ", str(msg))


def sync_cloud_cam_pos():
    dev_type = get_dev_type(CAM_SERIAL)
    if (dev_type is None):  # Cannot get Shelf ID - Means not assigned to shelf yet
        return True
    else:
        if(dev_type == "sensor" or dev_type == "dynamic_cam"):
            return True
        elif(dev_type == "left_cam" or dev_type == "right_cam"):
            CAM_POSITION = dev_type
            return False
        else:
            return True
