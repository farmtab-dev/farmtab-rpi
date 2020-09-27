#!/usr/bin/env python
from datetime import datetime
from time import sleep
import os
import tinys3


import schedule  # https://pypi.org/project/schedule/
#import yaml  # pip install pyyaml https://github.com/yaml/pyyaml/issues/291
import boto3

# client = boto3.client('kinesisvideo')
s3_client = boto3.client('s3')
from func.h_img_join_func import get4X4ImgMerged
from func.h_arducam_func import changeCam, captureImg
from config.cfg_py_camera import CAM_SERIAL, SEND_IMG_HOUR,TIME_INTERVAL, DEBUG, S3_CFG,FILE_CFG, IMG_CFG, TOTAL_CAM, CAM_SLOT_OBJ, CAM_SLOT_LIST

# photo props
# image_width = cfg['image_settings']['horizontal_res']
# image_height = cfg['image_settings']['vertical_res']
# file_extension = cfg['image_settings']['file_extension']
# file_name = cfg['image_settings']['file_name']
# photo_interval = cfg['image_settings']['photo_interval'] # Interval between photo (in seconds)
# image_folder = cfg['image_settings']['folder_name']


# verify image folder exists and create if it does not
if not os.path.exists(FILE_CFG["dirpath"]):
    os.makedirs(FILE_CFG["dirpath"])


def getCamFilepath(cindex):
    return  FILE_CFG["dirpath"] + '/'+ CAM_SLOT_OBJ[CAM_SLOT_LIST[cindex]] + FILE_CFG["imgfile_ext"] if cindex <len(CAM_SLOT_LIST) else "NONE"


def uploadToS3(filepath,cam_position):
    conn = tinys3.Connection(S3_CFG['access_key_id'], S3_CFG['secret_access_key'])
    f = open(filepath, 'rb')
    t = conn.upload(filepath, f, S3_CFG['bucket_name'],
            headers={
            'x-amz-meta-cache-control': 'max-age=60',         
            'x-amz-meta-farmtab-serial-number': CAM_SERIAL,
            'x-amz-meta-farmtab-cam-position': cam_position
            })
    print (t)

    if DEBUG == True:
        print ('[debug] Uploaded ' + filepath + ' to s3 ['+ S3_CFG['bucket_name']+']')
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
#         print ('[debug] Uploaded ' + filepath + ' to s3 ['+ S3_CFG['bucket_name']+']')


def uploadAllToS3():
    if (datetime.now().hour not in SEND_IMG_HOUR):
        print("\nINFO - NOT UPLOAD TIME YET - ",datetime.now())
        return
    print ("\nINFO - UPLOADING to S3 ", datetime.now())
    for x in CAM_SLOT_LIST:  
        f = FILE_CFG["dirpath"] + '/'+ CAM_SLOT_OBJ[x] + FILE_CFG["imgfile_ext"]
        uploadToS3(f)
    
    fp = get4X4ImgMerged(FILE_CFG["dirpath"], getCamFilepath(0), getCamFilepath(1), getCamFilepath(2), getCamFilepath(3))
    uploadToS3(fp)
    print ("SUCCESS - DONE UPLOADED") 


print (TOTAL_CAM, CAM_SLOT_OBJ, CAM_SLOT_LIST)
def main():
    schedule.every().hour.at(":00").do(uploadAllToS3)
    # endlessly capture images awwyiss
    i=0
    while True:
        schedule.run_pending()

        # Set curr Camera Slot
        currCamSlot = CAM_SLOT_OBJ[CAM_SLOT_LIST[i]]
        print ("\nCurrent [ " + CAM_SLOT_LIST[i] + " ] camera - [ Slot_" + currCamSlot + " ]")

        # Build filename string
        filepath =getCamFilepath(i)


        # Change & Take Photo
        changeCam(currCamSlot)
        if DEBUG == True:
            print ("[debug] Changed cam slot")
        sleep(TIME_INTERVAL["cap_img"])
        captureImg(filepath,IMG_CFG["width"],IMG_CFG["height"] ,currCamSlot)
        if DEBUG == True:
            print ('[debug] Taking photo and saving to path ' + filepath)

        # Upload to S3
        #uploadToS3(filepath)
        
        # Cleanup
        # if os.path.exists(filepath):
        #     os.remove(filepath)

        # sleep
        i+=1
        if (i>=len(CAM_SLOT_LIST)):  
            print("Updated all camera stream - ", datetime.now())
            i=0
            # Upload ALL CAM to S3
            if (datetime.now().minute in [30]):
                fp = get4X4ImgMerged(FILE_CFG["dirpath"], getCamFilepath(0), getCamFilepath(1), getCamFilepath(2), getCamFilepath(3))
                uploadToS3(fp)

        sleep(TIME_INTERVAL["chg_cam"])

main()

