import os
#=====================================#  
#  IMAGE RELATED CONFIG  # 
#=====================================#  
DEBUG=True
CAP_TIMEOUT = 20000
TIME_INTERVAL = {
    "chg_cam": os.environ.get('INTERVAL_CHG_CAM', 20),
    "cap_img": os.environ.get('INTERVAL_CAP_IMG', 20)
} 
#SEND_IMG_HOUR = [6, 9, 12, 15];
# SEND_IMG_HOUR = [5, 7, 13, 15, 21, 23];
SEND_IMG_HOUR = [7, 10, 13, 16];  # Normal
# SEND_IMG_HOUR = [0,1,2,7, 10, 13, 16];  # Normal
FILE_CFG = {
    "dirpath":  os.environ.get('ORG_NAME', 'images'),
    "imgfile_ext": '.jpg',
}
IMG_CFG= {
    "width": 320,
    "height": 240
}
image_settings= {
    "horizontal_res": 320,
    "vertical_res": 240,
    "file_name": 'test',
    "file_extension": '.jpg',
    "folder_name": 'images',
    "awb_mode": 'auto',
    "photo_interval": 60
}

#=====================================#  !IMPORTANT : Serial Number is unique globally
#  RASPBERRY PI Serial Number CONFIG  #
#=====================================#
CAM_SERIAL  = os.environ.get('FARMTAB_SERIAL', "")

#=====================================#  
#  AWS RELATED CONFIG  # 
#=====================================#  
AWS_SECRET_KEY=""
S3_CFG = {
    "access_key_id": os.environ.get('AWS_S3_ACCESS_KEY_ID', "") ,
    "secret_access_key": os.environ.get('AWS_S3_SECRET_ACCESS_KEY', ""),
    "bucket_name": os.environ.get('AWS_S3_BUCKET_NAME', "")
}


TOTAL_CAM=os.environ.get('TOTAL_CAM', "0")
CAM_NEED_ROTATE = { # TO_CHANGE: Camera rotation for (1)
    'lvl1': os.environ.get("CAM_ROTATE_LVL1","NO")=="YES",
    'lvl2': os.environ.get("CAM_ROTATE_LVL2","NO")=="YES",
    'lvl3': os.environ.get("CAM_ROTATE_LVL3","NO")=="YES",
    'lvl4': os.environ.get("CAM_ROTATE_LVL4","NO")=="YES",
}
if(TOTAL_CAM=="4" or TOTAL_CAM==4):
    CAM_SLOT_OBJ = {
        'lvl1': os.environ.get("CAM_SLOT_LVL1",""),
        'lvl2': os.environ.get("CAM_SLOT_LVL2",""),
        'lvl3': os.environ.get("CAM_SLOT_LVL3",""),
        'lvl4': os.environ.get("CAM_SLOT_LVL4",""),
    }
    CAM_SLOT_LIST = ['lvl1', 'lvl2', 'lvl3', 'lvl4']
elif(TOTAL_CAM=="3" or TOTAL_CAM==3):
    CAM_SLOT_OBJ = {
        'lvl1': os.environ.get("CAM_SLOT_LVL1",""),
        'lvl2': os.environ.get("CAM_SLOT_LVL2",""),
        'lvl3': os.environ.get("CAM_SLOT_LVL3",""),
    }
    CAM_SLOT_LIST = ['lvl1', 'lvl2', 'lvl3']
elif(TOTAL_CAM=="2" or TOTAL_CAM==2):
    CAM_SLOT_OBJ = {
        'lvl1': os.environ.get("CAM_SLOT_LVL1",""),
        'lvl2': os.environ.get("CAM_SLOT_LVL2",""),
    }
    CAM_SLOT_LIST = ['lvl1', 'lvl2']
elif(TOTAL_CAM=="1" or TOTAL_CAM==1):
    CAM_SLOT_OBJ = {
        'lvl1': os.environ.get("CAM_SLOT_LVL1",""),
    }
    CAM_SLOT_LIST = ['lvl1']
else:
    CAM_SLOT_OBJ = {}
    CAM_SLOT_LIST = []
