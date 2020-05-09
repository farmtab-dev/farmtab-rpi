import os
#=====================================#  !IMPORTANT : Serial Number is unique globally
#  RASPBERRY PI Serial Number CONFIG  #  https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5
#=====================================#
SEN_SERIAL   = os.environ.get('SENSOR_SERIAL', None)
CAM_SERIAL  = os.environ.get('CAMERA_SERIAL', None)
