import os
#=====================#
#  CONNECTION CONFIG  #
#=====================#
API_SERVER_URL = os.environ.get('API_SERVER_URL', None)

#===============#
#  MQTT CONFIG  #
#===============#
MQTT_LOCAL_SERVER = "localhost"
MQTT_CLOUD_SERVER = os.environ.get('MQTT_HOSTNAME', None)
MQTT_SERVER_TYPE  = os.environ.get('MQTT_SERVER_TYPE', None) 
MQTT_PORT         = int(os.environ.get('MQTT_PORT', 1883))
MQTT_USERNAME     = os.environ.get('MQTT_USER', None)
MQTT_PASSWORD     = os.environ.get('MQTT_PASSWORD', None)
MQTT_AUTH_METHOD  = os.environ.get('MQTT_AUTH_METHOD', None)
MQTT_ENABLE_AUTH  = True  # Is MQTT server has setup authentication?
MQTT_KEEPALIVE    = 60

#==================#
#  MONGODB CONFIG  #
#==================#
MONGODB_COLLECTION = {
    'data': "data",
    'msg': "notification",
    'act_stat': 'act_status',
    'act_rec': 'act_record'
}

MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', None)
MONGODB_URI = os.environ.get('MONGODB_URI', None)
