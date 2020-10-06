#!/usr/bin/env python3
#### pip3 install -r requirements.txt
import datetime
from time import sleep
import os
import tinys3


import schedule  # https://pypi.org/project/schedule/
#import yaml  # pip install pyyaml https://github.com/yaml/pyyaml/issues/291
# import boto3

# # client = boto3.client('kinesisvideo')
# s3_client = boto3.client('s3')
from func.h_img_join_func import get4X4ImgMerged
from func.h_arducam_func import changeCam, captureImg
from config.cfg_py_camera import CAM_SERIAL, SEND_IMG_HOUR, TIME_INTERVAL, DEBUG, S3_CFG, FILE_CFG, IMG_CFG, TOTAL_CAM, CAM_SLOT_OBJ, CAM_SLOT_LIST, CAM_NEED_ROTATE, CAP_TIMEOUT

# photo props
# image_width = cfg['image_settings']['horizontal_res']
# image_height = cfg['image_settings']['vertical_res']
# file_extension = cfg['image_settings']['file_extension']
# file_name = cfg['image_settings']['file_name']
# photo_interval = cfg['image_settings']['photo_interval'] # Interval between photo (in seconds)
# image_folder = cfg['image_settings']['folder_name']

CAM_POSITION = "left_cam"


# verify image folder exists and create if it does not
if not os.path.exists(FILE_CFG["dirpath"]):
    os.makedirs(FILE_CFG["dirpath"])


def get_curr_datetime():
    # --> https://stackoverflow.com/questions/25837452/python-get-current-time-in-right-timezone
    utc_dt = datetime.datetime.now(datetime.timezone.utc)  # UTC time
    # local time
    return datetime.datetime.strftime(utc_dt.astimezone(), "%Y-%m-%d %H:%M:%S%z")

def getCombinedDesc():
    res_str =""
    for x in CAM_SLOT_LIST:
        res_str+= CAM_SLOT_OBJ[x]
    return res_str

def getCamFilepath(cindex):
    return  FILE_CFG["dirpath"] + '/'+ CAM_SLOT_LIST[cindex].upper() + FILE_CFG["imgfile_ext"] if cindex < len(CAM_SLOT_LIST) else "NONE"


def uploadToS3(filepath,cam_lvl, cam_slot):
    conn = tinys3.Connection(S3_CFG['access_key_id'], S3_CFG['secret_access_key'])
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
    print (t)

    if DEBUG == True:
        print ('\t [debug] Uploaded ' + filepath + ' to s3 ['+ S3_CFG['bucket_name']+']')
# def uploadToS3(filepath):
#     conn = tinys3.Connection(S3_CFG['access_key_id'], S3_CFG['secret_access_key'])
#     f = open(filepath, 'rb')
#     t = conn.upload(filepath, f, S3_CFG['bucket_name'],
#             headers={
#             'x-amz-meta-cache-control': 'max-age=60',
#             'farmtab_serial_number ': os.environ.get('FARMTAB_SERIAL', "") , 
#             })
#     print (t)

#     if DEBUG == True:
#         print ('\t [debug] Uploaded ' + filepath + ' to s3 ['+ S3_CFG['bucket_name']+']')


def uploadAllToS3():
    if (datetime.datetime.now().hour not in SEND_IMG_HOUR):
        print("INFO - NOT UPLOAD TIME YET - ",datetime.datetime.now())
        return
    print ("INFO - UPLOADING to S3 ", datetime.datetime.now())
    # for x in CAM_SLOT_LIST:  
    #     f = FILE_CFG["dirpath"] + '/'+ x + FILE_CFG["imgfile_ext"] 
    for i in range(len(CAM_SLOT_LIST)):
        camLvl = CAM_SLOT_LIST[i]
        uploadToS3(getCamFilepath(i),camLvl.upper(), CAM_SLOT_OBJ[camLvl])
    
    fp = get4X4ImgMerged(img_cfg=IMG_CFG, file_cfg={
        "dirpath": FILE_CFG["dirpath"],
        "fpA": getCamFilepath(0), "fpB":getCamFilepath(1), "fpC":getCamFilepath(2), "fpD":getCamFilepath(3)})
    uploadToS3(fp, "COMBINED", getCombinedDesc())
    print ("SUCCESS - DONE UPLOADED") 


print ("Total Camera :", TOTAL_CAM, " => ",CAM_SLOT_OBJ)
def main():
    schedule.every().hour.at(":00").do(uploadAllToS3)
    # endlessly capture images awwyiss
    i=0
    while True:
        schedule.run_pending()

        # Set curr Camera Slot
        camLvl = CAM_SLOT_LIST[i]
        currCamSlot = CAM_SLOT_OBJ[camLvl]
        print ("\nCurrent [ " + camLvl + " ] camera - [ Slot_" + currCamSlot + " ] - Rotate - "+str(CAM_NEED_ROTATE[camLvl]))

        # Build filename string
        filepath =getCamFilepath(i)


        # Change & Take Photo
        changeCam(currCamSlot)
        if DEBUG == True:
            print ("\t [debug] Changed cam slot")
        sleep(TIME_INTERVAL["cap_img"])
        captureImg(filepath,IMG_CFG["width"],IMG_CFG["height"], CAM_NEED_ROTATE[camLvl] ,currCamSlot, CAP_TIMEOUT)
        if DEBUG == True:
            print ('\t [debug] Taking photo and saving to path ' + filepath)

        # Upload to S3
        #uploadToS3(filepath)
        
        # Cleanup
        # if os.path.exists(filepath):
        #     os.remove(filepath)

        # sleep
        i+=1
        if (i>=len(CAM_SLOT_LIST)):  
            print("Updated all camera stream - ", datetime.datetime.now())
            i=0
            # Upload ALL CAM to S3
            if (datetime.datetime.now().minute in []):
                fp = get4X4ImgMerged(img_cfg=IMG_CFG, file_cfg={
                "dirpath": FILE_CFG["dirpath"],
                "fpA": getCamFilepath(0), "fpB":getCamFilepath(1), "fpC":getCamFilepath(2), "fpD":getCamFilepath(3)})
                uploadAllToS3()

        sleep(TIME_INTERVAL["chg_cam"])

main()

