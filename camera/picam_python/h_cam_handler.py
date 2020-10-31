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
from func.h_img_join_func import get4X4ImgMerged
from func.h_arducam_func import changeCam, captureImg
from config.cfg_py_camera import CAM_SERIAL, SEND_IMG_HOUR, TIME_INTERVAL, DEBUG, S3_CFG, FILE_CFG, IMG_CFG, TOTAL_CAM, CAM_SLOT_OBJ, CAM_SLOT_LIST, CAM_NEED_ROTATE, CAP_TIMEOUT

CAM_POSITION = "left_cam"


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


def getCombinedDesc():
    res_str = ""
    for x in CAM_SLOT_LIST:
        res_str += CAM_SLOT_OBJ[x]
    return res_str


def getCamFilepath(cindex):
    return FILE_CFG["dirpath"] + '/' + CAM_SLOT_LIST[cindex].upper() + "_" + CAM_POSITION + FILE_CFG["imgfile_ext"] if cindex < len(CAM_SLOT_LIST) else "NONE"


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
        return
    print("INFO - UPLOADING to S3 ", timeNow())
    # for x in CAM_SLOT_LIST:
    #     f = FILE_CFG["dirpath"] + '/'+ x + FILE_CFG["imgfile_ext"]
    for i in range(len(CAM_SLOT_LIST)):
        camLvl = CAM_SLOT_LIST[i]
        uploadToS3(getCamFilepath(i), camLvl.upper(), CAM_SLOT_OBJ[camLvl])

    fp = get4X4ImgMerged(img_cfg=IMG_CFG, file_cfg={
        "dirpath": FILE_CFG["dirpath"],
        "fpA": getCamFilepath(0), "fpB": getCamFilepath(1), "fpC": getCamFilepath(2), "fpD": getCamFilepath(3)})
    uploadToS3(fp, "COMBINED", getCombinedDesc())
    print("SUCCESS - DONE UPLOADED")


def printDebug(msg):
    if DEBUG == True:
        print("\t [debug] ", str(msg))