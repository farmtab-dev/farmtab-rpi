/*============
 *  IMPORTS
 *============*/
const SimpleNodeLogger = require("simple-node-logger"); // https://www.npmjs.com/package/simple-node-logger
const io = require('socket.io-client');
const path = require('path');
const pm2 = require('pm2');
const mqtt = require("mqtt"); // https://www.npmjs.com/package/mqtt
/*-----------------
 *  CUSTOM IMPORTS
 *-----------------*/
const CONFIG = require("../camera/config/cfg_js_server");
const FARMTAB_SERIAL = require("../camera/config/cfg_js_serial").farmtab;

var PM2_OBJ = {
    script: []
}

log = SimpleNodeLogger.createSimpleLogger(CONFIG.log.video_opts);
log.setLevel("debug"); //   trace, debug, info, warn, error and fatal.
log.fatal("\nDIR ==> [ " + __dirname + " ] \nSTART SCRIPT - [ " + path.basename(__filename) + " ] \n");
/*===============
 * Check serial 
 *===============*/
if (FARMTAB_SERIAL === "") {
    console.log("ERROR - No Serial. Cannot proceed without a serial number.");
    process.exit();
}

// https://stackoverflow.com/questions/55623781/pm2-how-can-i-get-access-process-status-programmatically
function describePM2ScriptAndReply(socket, app_sid, script_name, auto_disconnect, need_detail = false) {
    if (script_name === "calibrate_script") {
        is_calibrate = true;
        script_name = "sensor_script";
    } else {
        is_calibrate = false;
    }

    pm2.describe(script_name, (err, data) => {
        console.log("INFO : Describe script ==> [ " + script_name + " ]")
        if (err) {
            console.log("ERROR in Describe [" + script_name + "]:\n");
            console.log(err)
            socket.emit('incoming-script-state', {
                app_sid: app_sid,
                pi_serial: FARMTAB_SERIAL,
                script: is_calibrate ? "calibrate_script" : script_name,
                status: "reading_error",
                auto_disconnect: auto_disconnect
            });
        } else {
            console.log("Total duplicate scripts: " + data.length)
            if (data.length === 0) {
                socket.emit('incoming-script-state', {
                    app_sid: app_sid,
                    pi_serial: FARMTAB_SERIAL,
                    script: is_calibrate ? "calibrate_script" : script_name,
                    status: "not_running",
                    auto_disconnect: auto_disconnect
                });
            } else {
                data.forEach(d => {
                    socket.emit('incoming-script-state', {
                        app_sid: app_sid,
                        pi_serial: FARMTAB_SERIAL,
                        script: is_calibrate ? "calibrate_script" : script_name,
                        status: d.pm2_env.status,
                        auto_disconnect: auto_disconnect
                    });
                    if (need_detail) {
                        console.log(d)
                    } else {
                        console.log(d.name + " ==> " + d.pm2_env.status);
                    }
                });
            }
        }
    })
}


function checkAllPM2Script() {
    pm2.list((err, data) => {
        console.log("INFO : Checking All PM2 scripts")
        if (err) {
            console.log("ERROR in LISTING:\n");
            console.log(err)
        } else {
            console.log("Total scripts: " + data.length)

            PM2_OBJ.script = [];
            data.forEach(d => {
                PM2_OBJ[d.name] = {
                    status: d.pm2_env.status,
                    restart_time: d.pm2_env.restart_time
                };
                PM2_OBJ.script.push(d.name);
                console.log(d.name + " ==> " + d.pm2_env.status);
            });
        }
    })
}

checkAllPM2Script();

/*############################################################*/
/* 		MQTT CONNECTION - Start establish connection        */
/*############################################################*/
var mqtt_client = mqtt.connect("mqtt://localhost:1883");

/*=====================
 *  MQTT On "Connect"
 *=====================*/
mqtt_client.on("connect", function() {
    /**------------------------
     *  SUBCRIBE to MQTT topic 
      -------------------------*/
    mqtt_client.subscribe("/local/res_data", function(err) {
        if (err) {
            log.error("ERROR when connect to MQTT : " + err);
        } else {
            log.info("Subscribe to " + "/local/res_data");
        }
    });
    mqtt_client.subscribe("/local/res_calibrate", function(err) {
        if (err) {
            log.error("ERROR when connect to MQTT : " + err);
        } else {
            log.info("Subscribe to " + "/local/res_calibrate");
        }
    });

});

/*==================================
 *  MQTT : HANDLE INCOMING MESSAGE
 *==================================*/
//handle incoming messages
mqtt_client.on('message', function(mqtt_topic, mqtt_msg, packet) {
    log.info(
        "\nMQTT TOPIC : " + mqtt_topic.toString() + "\nMQTT MSG : " + mqtt_msg.toString()
    );
    res = JSON.parse(mqtt_msg.toString())
    if (mqtt_topic.toString() === "/local/res_data") {
        socket.emit('reply-sample-sensor-data', {
            app_sid: res.socket,
            disconnect: res.disconnect,
            sensor: res.sensor
        });
    } else if (mqtt_topic.toString() === "/local/res_calibrate") {
        socket.emit('reply-calibration', {
            app_sid: res.socket,
            serial_num: FARMTAB_SERIAL,
            disconnect: res.disconnect,
            calibrate_stat: res.c_stat,
            calibrate_msg: res.c_msg
        });
    }
});

/*=====================
 *  MQTT : Handle PUBLISH
 *=====================*/
mqtt_client.on("publish", function() {
    console.log("Publish data");
});
/*=====================
 *  MQTT : Handle ERROR
 *=====================*/
mqtt_client.on("error", function(error) {
    console.error("Can't connect" + error);
    process.exit(1);
});

function pubSampleSensorDataRequest(app_sid, auto_disconnect) {
    console.log("Socket ID : [ " + app_sid + " ] => " + auto_disconnect)
    mqtt_client.publish("/local/req_data/" + app_sid.toString(), auto_disconnect.toString())
}

function pubInitCalibrationRequest(app_sid) {
    console.log("Socket ID : [ " + app_sid + " ] => Init Calibration")
    mqtt_client.publish("/local/calibrate/" + app_sid.toString(), "INIT")
}

function pubCalibrationCMD(app_sid, calibration_cmd) {
    console.log("Socket ID : [ " + app_sid + " ] => Command Calibration")
    mqtt_client.publish("/local/calibrate/" + app_sid.toString(), calibration_cmd.toString())
}

function pubSensorCalibrateCMD(app_sid, calibration_cmd) {
    console.log("Socket ID : [ " + app_sid + " ] => Command Calibration")
    mqtt_client.publish("/local/sensor_cmd/" + app_sid.toString(), calibration_cmd.toString())
}
/*############################################################*/
/* 		SOCKET CONNECTION - Start establish connection        */
/*############################################################*/
const piDesc = "[ " + FARMTAB_SERIAL + " ].";
log.warn("Connecting to ", CONFIG.socket_server_url, " as ", piDesc);
var socket = io(CONFIG.socket_server_url);
var videoStreamFunc; // Interval Function
var currStreaming;
/*************
 * On Connect
 *************/
socket.on('connect', function() {
    log.info("\nCONNECTED to server ", CONFIG.socket_server_url, " as ", piDesc,
        "\nTotal script: ", PM2_OBJ.script.length);
    currStreaming = false;
});
/****************
 * On Disconnect
 ****************/
socket.on('disconnect', function() {
    log.info("\nDISCONNECTED from server ", CONFIG.socket_server_url, " as ", piDesc);
});

/*********************************
 *  Send Client Info (As PI_CTRL)
 *********************************/
socket.on('client info req', function() {
    const conn_data = {
        client_name: "pi_ctrl_" + FARMTAB_SERIAL,
        client_type: "pi",
    };
    socket.emit('client info res', conn_data);
    log.info("Send pi client info - ", piDesc);
});


/*********************************
 *  Alert 
 *********************************/
socket.on('client curr room', handleCurrRoomReport)

function handleCurrRoomReport(room_info) {
    console.log("INFO : Join [ ", room_info.room, " ]")

}
/*********************************
 *  Received Script State Query
 *********************************/
socket.on('req-script-state', handleScriptStateQuery)

function handleScriptStateQuery(query_info) {
    describePM2ScriptAndReply(socket, query_info.app_sid, query_info.script_name, query_info.auto_disconnect)
}

/*********************************
 *  Received Sample Data Query
 *********************************/
socket.on('req-sample-sensor-data', handleSampleSensorData)

function handleSampleSensorData(query_info) {
    pubSampleSensorDataRequest(query_info.app_sid, query_info.auto_disconnect)
}
/*********************************
 *  Received calibrate
 *********************************/
socket.on('req-init-calibration', handleInitCalibration)

function handleInitCalibration(query_info) {
    pubInitCalibrationRequest(query_info.app_sid)
}

socket.on('send-calibration-cmd', handleCalibrationCMD)

function handleCalibrationCMD(query_info) {
    pubCalibrationCMD(query_info.app_sid, query_info.calibration_cmd)
}


socket.on('start-cal-sensor', handleStartCalibration)

function handleStartCalibration(query_info) {
    // pubCalibrationCMD(query_info.app_sid, query_info.calibrate_sensor)
    setTimeout(() => {
        pubSensorCalibrateCMD(query_info.app_sid, "ENTER" + query_info.calibrate_sensor)
    }, 5 * 1000);
    setTimeout(() => {
        pubSensorCalibrateCMD(query_info.app_sid, "CAL" + query_info.calibrate_sensor)
    }, 5 * 1000);
    setTimeout(() => {
        pubSensorCalibrateCMD(query_info.app_sid, "EXIT" + query_info.calibrate_sensor)
    }, 5 * 1000);

    socket.emit('end-cal-sensor', {
        app_sid: query_info.app_sid,
        serial_num: FARMTAB_SERIAL,
        disconnect: false,
        calibrate_stat: "COMP_CALIBRATE",
        calibrate_msg: "Completed calibrate " + query_info.calibrate_sensor + " sensor"
    });
}
socket.on('close-calibration', handleCloseCalibration)

function handleCloseCalibration(query_info) {
    pubCalibrationCMD(query_info.app_sid, "CLOSE")
}