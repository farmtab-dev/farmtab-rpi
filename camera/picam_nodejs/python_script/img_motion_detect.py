#https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# import the necessary packages
from py_motion_helper import read_img, save_img, rotate_img, encode_img_to_base64
from farmtab_py_msg_prep import prepare_img_notification_message_obj
from cfg_py_mqtt_topic import PUB_CLOUD_TOPIC
from cfg_py_server import MQTT_USERNAME, MQTT_PASSWORD, MQTT_SERVER, IMGFILE_DIRPATH, IMG_MOTION_DIRPATH, CAM_SERIAL

from imutils.video import VideoStream  # sudo pip install imutils
import argparse
import datetime
import imutils
import time
import cv2  # Dependencies Issue : https://github.com/amymcgovern/pyparrot/issues/34
# pip3 install opencv-python
# sudo apt-get install libatlas-base-dev
# sudo apt-get install libjasper-dev
# sudo apt-get install libqtgui4
# sudo apt-get install python3-pyqt5
# sudo apt install libqt4-test
# sudo apt-get install libatlas-base-dev libjasper-dev libqtgui4 python3-pyqt5 libqt4-test
import sys
import os

#------------------------#
#  Adjust parameter here #
#------------------------# 
FRAME_WIDTH = 640
MIN_MOTION_AREA = 1000
TOTAL_MOTION_FRAME = 10


def convertGrayscalePlusGaussianBlur(target_img):
    gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gray, (21, 21), 0)

def motion_references():
    try:
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int,
                        default=500, help="minimum area size")
        args = vars(ap.parse_args())

        # if the video argument is None, then we are reading from webcam
        if args.get("video", None) is None:
            print ("VIDEO start")
            vs = VideoStream(src=0).start()
            print (vs.read())
            time.sleep(2.0)

        # otherwise, we are reading from a video file
        else:
            vs = cv2.VideoCapture(args["video"])
            print ("READ")

        # initialize the first frame in the video stream
        firstFrame = None
        print ("BEF loop")
        # loop over the frames of the video
        i=0
        while True:
            print ("In loop")
            # grab the current frame and initialize the occupied/unoccupied
            # text
            frame = vs.read()
            frame = frame if args.get("video", None) is None else frame[1]
            text = "NORMAL"

            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if frame is None:
                print ("FRAME is NONE")
                break

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < args["min_area"]:
                    continue

                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "ALERT"

            print (str(len(cnts)))
                # draw the text and timestamp on the frame
            cv2.putText(frame, "Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            
            # show the frame and record if the user presses a key
            i+=1
            cv2.imwrite(IMG_MOTION_DIRPATH + "Security Feed"+str(i)+".png", frame)
            cv2.imwrite(IMG_MOTION_DIRPATH + "Thresh"+str(i)+".png", thresh)
            cv2.imwrite(IMG_MOTION_DIRPATH + "Frame Delta"+str(i)+".png", frameDelta)
            

        # cleanup the camera and close any open windows
        vs.stop() if args.get("video", None) is None else vs.release()
        cv2.destroyAllWindows()
    except:
        print ("ERROR")

#===========================#
#  Main Algorithm 
#===========================#
def run_motion_detection_algo(firstFrame, currFrame, currFrameColor, curr_img_captured_time, cam_serial):
    # text = "NORMAL"
    #==================================#
    # Convert to Grayscale and blur it #
    #==================================# # resize the frame, convert it to grayscale, and blur it
    #gray = convertGrayscalePlusGaussianBlur(currFrame)

    #========================================================#
    # Compute absolute difference between 1st and curr frame #
    #========================================================#
    firstFrame = imutils.resize(firstFrame, width=FRAME_WIDTH)
    currFrame = imutils.resize(currFrame, width=FRAME_WIDTH)
    currFrameColor = imutils.resize(currFrameColor, width=FRAME_WIDTH)
    frameDelta = cv2.absdiff(firstFrame, currFrame)

    #==========================================================#
    # Dilate Thresholded img; Find contours on thresholded img #
    #==========================================================#
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    has_motion = False
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < MIN_MOTION_AREA:
            continue
        
        has_motion = True
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(currFrameColor, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #text = "ALERT"

    
    # draw the text and timestamp on the frame
    #cv2.putText(frame, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if the user presses a key
    print(str(len(cnts)))
    if (has_motion):
#        dirpath = "/opt/farmtab-rpi/camera/img_motion/"
#        region_with_pre = combine_two_images(region_img, preprocess_img, False)
        msg_str = prepare_img_notification_message_obj(curr_img_captured_time, cam_serial, "motion")
        #os.system('mosquitto_pub -m "'+msg_str+'"  -t "'+PUB_CLOUD_TOPIC["pub_msg"]+'"  -u "'+MQTT_USERNAME+'" -P "'+MQTT_PASSWORD+'"')
        cmd = "mosquitto_pub -m '"+str(msg_str)+"'  -t '"+PUB_CLOUD_TOPIC["pub_msg"]+"'  -u '"+MQTT_USERNAME+"' -P '"+MQTT_PASSWORD+"' --host '"+MQTT_SERVER+"'"
        print (cmd)
        os.system(cmd)

        #motion_img_base64str = encode_img_to_base64(currFrameColor)
        
        #img_dict = prepare_motion_img(curr_img_captured_time, cam_serial, motion_img_base64str)
        #store_images(img_dict)  # Normal Storing images
        
        #save_img("motion-sample "+str(curr_img_captured_time), IMG_MOTION_DIRPATH, currFrameColor)

        #cv2.imwrite(IMG_MOTION_DIRPATH + "motion-sample "+str(curr_img_captured_time)+".png", currFrameColor)
        cv2.imwrite(IMG_MOTION_DIRPATH + "motion_detected.jpg", currFrameColor)
        print ("@MOTION@")
        #cv2.imwrite(IMG_MOTION_DIRPATH + "Thresh.png", thresh)
        #cv2.imwrite(IMG_MOTION_DIRPATH + "Frame Delta.png", frameDelta)
        exit()

def preprocess_img(target_img_path, need_rotate, need_local_save):
    curr_img = read_img(target_img_path,None)
    #--------------#
    # Rotate Image #
    #--------------#
    if (need_rotate == "true"):  # String Compare bacause passed via cmd line
        curr_img = rotate_img(curr_img, 180)

    # Prepare for subsequent step
    curr_img = convertGrayscalePlusGaussianBlur(curr_img)

    #----------------------#
    # Update IMAGE LOCALLY #
    #----------------------#
    if (need_local_save):
        #target_img_filename = target_img_path.split("/")[-1]
        #target_img_dirpath = target_img_path.replace(target_img_filename, "")
        cv2.imwrite(target_img_path, curr_img)

    return curr_img


def initialize_prev_main(target_img_path, need_rotate):
    preprocess_img(target_img_path, need_rotate, True)
    exit(0)

def motion_detection_main_with_one(prev_img_path, curr_img_path, need_rotate, curr_img_datetime, cam_serial):
    #---------------------#
    # EXTRACT PARAMS INFO #
    #---------------------#
    #target_img_filename = curr_img_path.split("/")[-1]
    #target_img_dirpath = curr_img_path.replace(target_img_filename, "")
    #cam_serial = target_img_filename.replace(".jpg", "")
    #---------------#
    # Prepare Image #
    #---------------#
    #curr_img = decode_buffer_to_img(target_image)
    prev_img = preprocess_img(prev_img_path, need_rotate, False)
    curr_img_gray = preprocess_img(curr_img_path,need_rotate, False)
    curr_img_color = read_img(curr_img_path, None)

    #--------------------------------#
    # RUN MOTION DETECTION ALGORITHM #
    #--------------------------------#
    run_motion_detection_algo(prev_img, curr_img_gray, curr_img_color,curr_img_datetime,cam_serial)


def motion_detection_main(prev_img_path, curr_img_dirpath, need_rotate, curr_img_datetime, cam_serial):
    #---------------#
    # Prepare Image #
    #---------------#
    #curr_img = decode_buffer_to_img(target_image)
    prev_img = preprocess_img(prev_img_path, need_rotate, False)
    for i in range(TOTAL_MOTION_FRAME):
        print("RUN IMG "+str(i))
        curr_img_gray = preprocess_img(IMGFILE_DIRPATH+CAM_SERIAL+"-curr"+str(i)+".jpg",need_rotate, False)
        curr_img_color = read_img(IMGFILE_DIRPATH+CAM_SERIAL+"-curr"+str(i)+".jpg", None)
        #--------------------------------#
        # RUN MOTION DETECTION ALGORITHM #
        #--------------------------------#
        run_motion_detection_algo(prev_img, curr_img_gray, curr_img_color,curr_img_datetime,cam_serial)

if __name__ == '__main__':
    #sys.stdout.flush()
    if(len(sys.argv) == 3):    # For Initialized Prev Image ==> target_img_filepath, need_rotate
        exit(0)
        #initialize_prev_main(sys.argv[1], sys.argv[2])
    elif(len(sys.argv) == 6):    # For Initialized Prev Image ==> prev_img_filepath, target_img_filepath, need_rotate,  curr_img_datetime, cam_serial
        motion_detection_main(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5])  
    else:
        print("Parameter length " + str(len(sys.argv)))
        exit(2)
