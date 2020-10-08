import os
SEN_SERIAL = os.environ.get('FARMTAB_SERIAL', "")

#===================#  IF PUBLISH : SPECIFY ID/Serial Num.
# MQTT TOPIC CONFIG #  IF SUBSCRIBE : USE #
#===================#
# Raspberry Pi <===> Cloud
P2C_HEADER = "p2c/"
C2P_HEADER = "c2p/"
# Self
P2P_HEADER = "p2p/"

#----------------------------------#  P2C / data/  & P2C / msg
# SENSOR DATA/CMD/CMD_REPLY HEADER #  C2P / cmd/
#----------------------------------#  P2C / reply/
SENSOR_DATA_HEADER = P2C_HEADER + "raw_data/"
NOTIFICATION_MSG_HEADER = P2C_HEADER + "msg/"
PI_CMD_HEADER = C2P_HEADER + "cmd/"
PI_CMD_REPLY_HEADER = P2C_HEADER + "reply/"

PI_SELF_CMD_HEADER = P2P_HEADER + "cmd/"

PI_TUNING_HEADER = C2P_HEADER + "tune/"
PI_TUNING_REPLY_HEADER = C2P_HEADER + "tune_reply/"

# GATEWAY : IOT_ID/+PK  || CLOUD : #
PI_ACT_STAT_HEADER = P2C_HEADER + "act_stat/"
# GATEWAY : IOT_ID/+PK  || CLOUD : #
PI_ACT_REC_HEADER = P2C_HEADER + "act_rec/"


#------------------------------#
# RASPBERRY PI - PUBLISH TOPIC #        Publish Data / Notification msg / Reply for command
#------------------------------#
PUB_SENSOR_DATA = SENSOR_DATA_HEADER + SEN_SERIAL
PUB_NOTIFICATION = NOTIFICATION_MSG_HEADER + SEN_SERIAL
PUB_CMD_REPLY = PI_CMD_REPLY_HEADER + SEN_SERIAL
PUB_PI_ACT_STAT = PI_ACT_STAT_HEADER + SEN_SERIAL
PUB_PI_ACT_REC = PI_ACT_REC_HEADER + SEN_SERIAL
PUB_CLOUD_TUNING = PI_TUNING_REPLY_HEADER + SEN_SERIAL
#--------------------------------#
# RASPBERRY PI - SUBSCRIBE TOPIC #
#--------------------------------#
SUB_CLOUD_CMD = PI_CMD_HEADER + SEN_SERIAL + "/#"
SUB_CLOUD_TUNING = PI_TUNING_HEADER + SEN_SERIAL + "/#"

# RASPBERRY PI - PUB + SUB topic
SELF_CMD = PI_SELF_CMD_HEADER + SEN_SERIAL

#========================#
# LIST of PUB/SUB topics #
#========================#
#--------------------------------#
SUB_TOPIC_LIST = {"CMD": [SUB_CLOUD_CMD], "TUNE": [SUB_CLOUD_CMD, SUB_CLOUD_TUNING]}

PUB_CLOUD_TOPIC = {"pub_data": PUB_SENSOR_DATA,
                   "pub_msg":  PUB_NOTIFICATION,
                   "pub_act_stat": PUB_PI_ACT_STAT,
                   "pub_act_rec": PI_ACT_REC_HEADER,
                   "pub_reply": PUB_CMD_REPLY,
                   "pub_tune": PUB_CLOUD_TUNING,
                   }
