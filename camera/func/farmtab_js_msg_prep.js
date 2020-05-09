var MQTT_TOPIC_CONFIG = require("../config/cfg_js_mqtt_topics");

var msg = {};
/* 
"msg_title": MSG_TITLE[problem_str],
    "msg_about": String,
    "msg_location": String,
    "msg_severity": String, */
msg.MSG_TITLE = {
    'success_command': "USB Device is activated",
    'error_command': "USB Device has been activated",
    'unknown_topic': "Unknown Topic",
    'unknown_message': "Unknown Command",
};
msg.MSG_ABOUT = {

};
msg.MSG_LOCATION = "@SITE@, @SHELF@ - @SERIAL@", // Identify by serial

    msg.MSG_SEVERITY = {
        'sensor_disconnect': "error",
        'sensor_temp_high': "warning",
        'sensor_humid_low': "warning",
        'sensor_moisture_low': "warning",
        'sensor_ph_high': "warning",
        'sensor_irr_water_low': "warning",
        'sensor_fer_water_low': "warning",
        'irrigation_act': "info",
        'fertigation_act': "info",
        'irrigation_deact': "info",
        'fertigation_deact': "info",
    }

MSG_REPLACE_CONTENT = {
    all_var: ['@SITE@', '@SHELF@', '@PLANT@'],
    '@SITE@': 'site',
    '@SHELF@': 'shelf',
    '@PLANT@': 'plant',
};

MSG_VARIABLE = {
    'time': "@TIME@",
    'serial_code_loc': "@SERIAL@#@SITE@ @SHELF@ @LEVEL@ --> @SERIAL@", // # Identify by serial
    'wl_id_loc': "@SERIAL@#@SITE@ @SHELF@ --> @SERIAL@", // # Identify by serial
    'irr_fer_id_loc': "@CTRL_ID@#@SITE@ @SHELF@", //  # ACT_CODE
    'about': {
        'dev_prob': "Device Problem",
        'read_prob': 'Reading Problem',
        'auto_act': 'Auto Activation',
        'man_act': 'Manual Activation'
    }
    // #"#@DEV_ID@#@SHELF@ @LEVEL@ --> @DEV_ID@#"
}

msg.CTRL_RES_CODE = {
    unknown: "-1",
    success_act: "A1",
    error_act: "A0",
    success_deact: "D1",
    error_deact: "D0",
}
msg.MSG_REPLY_HEADER = MQTT_TOPIC_CONFIG.PI_PURPOSE + "#";

// FORMAT : PI_LVL # RES_CODE (NUMBER) # CONTENT [3 TOKENS]
exports.prepareMQTTmessage = (res_dict) => {
    return msg.MSG_REPLY_HEADER + msg.CTRL_RES_CODE[res_dict.code] + "#" + res_dict.content;
};


/**********************************

switch(res_dict.code){
    case "unknown":
        pub_msg = msg.MSG_REPLY_HEADER+msg.CTRL_RES_CODE["unknown"]+"#"+res_dict.content;
        break;        
    case "success_act":
    case "success_deact":
        pub_msg = msg.MSG_REPLY_HEADER+msg.CTRL_RES_CODE["success_act"]+"#"+res_dict.content;
        break;        
    case "error_act":
    case "error_deact":
        pub_msg = msg.MSG_REPLY_HEADER+msg.CTRL_RES_CODE["error_act"]+"#"+res_dict.content;
        break;        

}*/