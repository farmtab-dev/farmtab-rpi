var FARMTAB_SERIAL = process.env.FARMTAB_SERIAL || ""; // TO_CHANGE

var config = {};

/******************
 *  TOPIC CONFIG  *
 ******************/
config.main = {
    // Raspberry Pi <===> Cloud
    P2C_HEADER: "p2c/",
    C2P_HEADER: "c2p/",
    // Self
    P2P_HEADER: "p2p/"
};

/*------------------* 
 * VIDEO + USB SCRIPT : Pub msg : Motion detect, USB on/off 
 *------------------*/
config.topic = {
    // IF PUBLISH : SPECIFIC ID. IF SUBSCRIBE : USE #  #PUB || SUB
    SENSOR_DATA_HEADER: config.main.S2G_HEADER + "data/", // SENSOR : +ID || GATEWAY : #
    SENSOR_CMD_HEADER: config.main.G2S_HEADER + "cmd/", // GATEWAY : +DEV_ID || SENSOR : +ID
    SENSOR_CMD_REPLY_HEADER: config.main.S2G_HEADER + "reply/", // SENSOR : +ID || GATEWAY : #

    CLOUD_DATA_HEADER: config.main.G2C_HEADER + "data/", // GATEWAY : +ID  || CLOUD : #
    CLOUD_IMG_HEADER: config.main.G2C_HEADER + "img/", // GATEWAY : +ID  || CLOUD : #
    NOTIFICATION_HEADER: config.main.G2C_HEADER + "msg/", // GATEWAY : IOT_ID/+PK  || CLOUD : #

    // Cloud Command
    CLOUD_CMD_HEADER: config.main.C2P_HEADER + "cmd/", // CLOUD : + IOT_ID/action | GATEWAY : + IOT_ID/#
    CLOUD_CMD_REPLY_HEADER: config.main.P2C_HEADER + "reply/", // GATEWAY : + IOT_ID/DEV_ID | CLOUD : #
};

// CLOUD - Subscribe topic - To Gateway
config.sub = {
    SUB_CLOUD_CMD: config.topic.CLOUD_CMD_HEADER + FARMTAB_SERIAL,

    SUB_GATEWAY_DATA: config.topic.CLOUD_DATA_HEADER + "#", // GATEWAY_ID
    SUB_GATEWAY_IMG: config.topic.CLOUD_IMG_HEADER + "#", // GATEWAY_ID / CM_ID
    SUB_GATEWAY_MSG: config.topic.NOTIFICATION_HEADER + "#", // GATEWAY_ID / Package ID
    SUB_GATEWAY_CMD_REPLY: config.topic.CLOUD_CMD_REPLY_HEADER + "#", // GATEWAY_ID / DEV_ID
    SUB_SELF_WORKER: config.topic.SELF_CMD_HEADER + config.PI_LEVEL,
    // SUB_SELF_COMMANDER: config.topic.SELF_CMD_REPLY_HEADER+"#",
};

config.pub = {
    PUB_CLOUD_CMD_REPLY: config.topic.CLOUD_CMD_REPLY_HEADER + FARMTAB_SERIAL, // GATEWAY_ID / DEV_ID

    PUB_SELF_CMD_REPLY: config.topic.SELF_CMD_REPLY_HEADER + config.PI_LEVEL, // GATEWAY_ID / DEV_ID
    PUB_SELF_CMD: config.topic.SELF_CMD_REPLY_HEADER + config.PI_LEVEL, // GATEWAY_ID / DEV_ID
};
/*******************
 *  EXPORT CONFIG
 ********************/
module.exports = config;