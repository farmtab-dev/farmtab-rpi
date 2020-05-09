#================#
#  INSTALLATION 
#================#
#  https://docs.opencv.org/3.4/d2/de6/tutorial_py_setup_in_ubuntu.html
#  https://stackoverflow.com/questions/26505958/why-cant-python-import-image-from-pil
#--https://stackoverflow.com/questions/38087558/import-error-no-module-named-skimage-----------------------------------------
#  https://stackoverflow.com/questions/36404042/importerror-no-module-named-sklearn-python
import cv2  # sudo apt-get install python-opencv
import base64
import numpy as np


# from matplotlib import pyplot as plt
ALL_FONTS = [cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_PLAIN, cv2.FONT_HERSHEY_DUPLEX, 
             cv2.FONT_HERSHEY_COMPLEX, cv2.FONT_HERSHEY_TRIPLEX, cv2.FONT_HERSHEY_COMPLEX_SMALL, 
             cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, cv2.FONT_HERSHEY_SCRIPT_COMPLEX]
BGR_FLAGS = ['COLOR_BGR2HSV', 'COLOR_BGR2HSV_FULL', 'COLOR_BGR2LAB',
             'COLOR_BGR2LUV', 'COLOR_BGR2Lab', 'COLOR_BGR2Luv',
             'COLOR_BGR2RGB']

P_UL,P_UR,P_BL, P_BR = (2, 12), (500, 12), (13, 685), (538, 385)
SAMPLE_COLOR = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "black": (0,0,0),
    "yellow": (30, 109, 155),
    "yellow_lower": (23, 41, 133),
    "yellow_upper": (40, 150, 255)
}
HSV_GREEN_LOWER_BOUND = np.array([30, 0, 0])
HSV_GREEN_UPPER_BOUND = np.array([90, 255, 255])
RES_DIRPATH = 'result/'
RES_FILENAME = 'cropped_img'
MAX_WIDTH_BOUND = 35
MAX_HEIGHT_BOUND = 35
IDEAL_BROWN = [15,255,150]
BROWN_LOWER_BOUND = (15,255,150)

#==============#
#  READ IMAGE  #--> OpenCV by default reads images in BGR format
#==============#
def read_img(img_path, imread_flag):
    if (imread_flag==None):
        target_img = cv2.imread(img_path)
    else:
        target_img = cv2.imread(img_path, cv2[imread_flag])

    # print("Image size (Row, Column, Channels) : " + str(target_img.shape))
    return target_img


#===============#
#   SAVE IMAGE  #
#===============#
def save_img(filename, dirpath, target_img):
    #print (type(target_img))
    #if (str(type(target_img)) != "<class 'numpy.ndarray'>"):
        #target_img = cv2.UMat(target_img)
        #target_img = np.ndarray(target_img)
    cv2.imwrite(dirpath + filename+'.png', target_img)
    # print ("Successful save image --> " + filename+".png" )

#====================#
#  DECODE OR ENCODE  # ---> https://stackoverflow.com/questions/16214190/how-to-convert-base64-string-to-image/16214280
#====================# ---> https://stackoverflow.com/questions/40928205/python-opencv-image-to-byte-string-for-json-transfer
def decode_buffer_to_img(buffer_str):
    imgdata = base64.b64decode(buffer_str)           # Decode from base64
    jpg_as_np = np.frombuffer(imgdata, dtype=np.uint8)  # Convert to np
    return cv2.imdecode(jpg_as_np, flags=1)  # Ready for processing

def encode_img_to_base64(target_img):
    retval, buffer = cv2.imencode('.jpg', target_img)
    return base64.b64encode(buffer)   # Convert to base64 encoding and show start of data


#==================#
#  GET IMAGE SIZE  #  --> HEIGHT, WIDTH
#==================#
def get_img_height_width(target_img):
    height, width = target_img.shape[:2] # Get first 2 element
    return height, width
def get_img_row_col_bands(target_img):
    return target_img.shape

def get_img_rect_start_end_point(x,y,w,h):
    return {"start" : (x,y), "end": (x+w, y+h)}


#======================#
#  TRANFORM -  ROTATE  #
#======================#
def rotate_img(target_img,degree):
    rows, cols = get_img_height_width(target_img)

    M = cv2.getRotationMatrix2D((cols/2, rows/2), degree, 1)
    dst = cv2.warpAffine(target_img, M, (cols, rows))
    return dst
