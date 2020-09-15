var config = {};
config.debug = process.env.DEBUG || false;

/****************
 * FILEPATH CONFIG
 ****************/
config.dirpath = {};
config.dirpath.main = "/opt/farmtab-rpi/camera/";
config.dirpath.log = config.dirpath.main + "log/";
config.dirpath.img = config.dirpath.main + "img_temp_folder/";
config.dirpath.motion = config.dirpath.main + "img_motion/";

config.filepath = {};
config.filepath.motion_detection_script = config.dirpath.main + "img_motion_detect.py";

/****************
 *  LOG CONFIG   : https://www.npmjs.com/package/simple-node-logger 
 ****************/
config.log = {};
config.log.timestampList = {
    format1: "YYYY-MM-DD HH:mm:ss.SSS"
};
config.log.video_opts = {
    logFilePath: config.dirpath.log + "pi-video-client.log",
    timestampFormat: config.log.timestampList.format1
};
config.log.usb_opts = {
    logFilePath: config.dirpath.log + "pi-mqtt-usb.log",
    timestampFormat: config.log.timestampList.format1
};


/****************
 *  CONNECTION  *
 ****************/
config.socket_server_url = process.env.SOCKET_SERVER_URL || '';
config.udp_socket_host = process.env.UDP_SOCKET_HOST || '';
config.udp_socket_port = process.env.UDP_SOCKET_PORT || '';

/*******************
 *   MQTT CONFIG
 ********************/
config.mqtt = {};
config.mqtt.user = process.env.MQTT_USER || '';
config.mqtt.password = process.env.MQTT_PASSWORD || '';
config.mqtt.hostname = process.env.MQTT_HOSTNAME || 'localhost';
config.mqtt.port = process.env.MQTT_PORT || 1883;

/*-------------
 *  MQTT URL
 *-------------*/
config.server = {};
// MQTT URI without Authentication
config.server.mqtt_uri_without_auth = 'mqtt://' + config.mqtt.hostname + ':' + config.mqtt.port;

// MQTT URI with Authentication
config.server.mqtt_uri = "mqtt://" +
    config.mqtt.user + ":" +
    config.mqtt.password + "@" +
    config.mqtt.hostname + ":" +
    config.mqtt.port;

/*******************
 *  EXPORT CONFIG
 ********************/
module.exports = config;