// https: //thejackalofjavascript.com/rpi-live-streaming/
// https://www.youtube.com/watch?v=qexy4Ph66JE
// https://github.com/ArduCAM/RaspberryPi/tree/master/Multi_Camera_Adapter/Multi_Adapter_Board_4Channel
/*
DATE = $(date + "%Y-%m-%d_%H%M")
fswebcam - r 1280 x720 /home/pi/Desktop/HELLO.jpg
*/
/*============
 *  IMPORTS
 *============*/
const SimpleNodeLogger = require("simple-node-logger"); // https://www.npmjs.com/package/simple-node-logger
const io = require('socket.io-client');
const PiCamera = require('pi-camera'); // https://www.npmjs.com/package/pi-camera
const { StillCamera } = require("pi-camera-connect");
const fs = require('fs');
const spawn = require('child_process').spawn;
const rasp2c = require('rasp2c'); // https://www.npmjs.com/package/@euoia/rasp2c
const Gpio = require('onoff').Gpio; //include onoff to interact with the GPIO
const async = require("async"); // http://findnerd.com/list/view/Node-js-How-to-perform-endless-loop-with-async-module/21121/
const path = require('path');
// const cron = require("node-cron");

/*-----------------
 *  CUSTOM IMPORTS
 *-----------------*/
const CONFIG = require("./config/cfg_js_server");
const CAMERA = require("./config/cfg_js_camera");
const CAM_SERIAL = require("./config/cfg_js_serial").camera;
const TIME_CFG = require("./config/cfg_js_time");

log = SimpleNodeLogger.createSimpleLogger(CONFIG.log.video_opts);
log.setLevel("debug"); //   trace, debug, info, warn, error and fatal.
log.fatal("\nDIR ==> [ " + __dirname + " ] \nSTART SCRIPT - [ " + path.basename(__filename) + " ] \n");
/*===============
 * Check serial 
 *===============*/
if (CAM_SERIAL === "") {
    console.log("ERROR - No Serial. Cannot proceed without a serial number.");
    process.exit();
}
/*===============
 * Setup Camera  - Adjust based on camera placement
 *===============*/
// RUN CMD if have error for VideoCapture : sudo modprobe bcm2835-v4l2 
const FPS = CAMERA.fps;
const IMG_WIDTH = CAMERA.img_width;
const IMG_HEIGHT = CAMERA.img_height;
const CAM_I2C = CAMERA.i2c;
const NEED_ROTATE = CAMERA.need_rotate;

/*===============
 * Initialize Camera View 
 *===============*/
const pin7 = new Gpio(4, 'out');
const pin11 = new Gpio(17, 'out');
const pin12 = new Gpio(18, 'out');
var CAM_VIEWS = CAMERA.getCamViewList(); // CAM_I2C["camViewList" + CAM_POS];
var haveCamFeed = "";
var CAM_FEED_DICT = {
    "lvl1": { cap_time: new Date(), need_rotate: NEED_ROTATE.lvl1 === "YES", img: '', lvl: "LVL1" },
    "lvl2": { cap_time: new Date(), need_rotate: NEED_ROTATE.lvl2 === "YES", img: '', lvl: "LVL2" },
    "lvl3": { cap_time: new Date(), need_rotate: NEED_ROTATE.lvl3 === "YES", img: '', lvl: "LVL3" },
    "lvl4": { cap_time: new Date(), need_rotate: NEED_ROTATE.lvl4 === "YES", img: '', lvl: "LVL4" },
};
var cam_view_disconnect_time = 0;



/*********************
 * CRON JOB INTERVAL * https://stackoverflow.com/questions/34735908/scheduling-file-every-1-hour-using-nodejs
 **********************/
// const CRON_JOB_INTERVAL = TIME_CFG.CRON_JOB_INTERVAL;
// const TIME_INTERVAL = TIME_CFG.TIME_INTERVAL;
// log.fatal("CRON JOB Time interval : " + CRON_JOB_INTERVAL);
// log.fatal("PRESET INTERVAL (in min) : " + //disconnect : " + TIME_INTERVAL.disconnect + " img_process : " + TIME_INTERVAL.img_process +
//     " prev_motion : " + TIME_INTERVAL.prev_motion + " detect_motion : " + TIME_INTERVAL.detect_motion);

const TIME_INTERVAL_IN_MIN = TIME_CFG.TIME_INTERVAL_IN_MIN;
var LAST_IMG_SEND_TIME = "";

/*############################################################*/
/* 		SOCKET CONNECTION - Start establish connection        */
/*############################################################*/
const camDesc = "[ " + CAM_SERIAL + " ].";
log.warn("Connecting to ", CONFIG.socket_server_url, " as ", camDesc);
var socket = io(CONFIG.socket_server_url);
var videoStreamFunc; // Interval Function
var currStreaming;
/*************
 * On Connect
 *************/
socket.on('connect', function() {
    log.info("\nCONNECTED to server ", CONFIG.socket_server_url, " as ", camDesc,
        "\nTotal camera: ", CAM_VIEWS.list.length,
        "\nCAM_VIEWS:", CAM_VIEWS.obj);
    currStreaming = false;
});
/****************
 * On Disconnect
 ****************/
socket.on('disconnect', function() {
    log.info("\nDISCONNECTED from server ", CONFIG.socket_server_url, " as ", camDesc);
});

/*********************************
 *  Send Client Info (As CAMERA)
 *********************************/
socket.on('client info req', function() {
    const conn_data = {
        client_name: CAM_SERIAL,
        cam_serial: CAM_SERIAL,
        client_type: "camera",
        client_req_cam_serial: "",
    };
    socket.emit('client info res', conn_data);
    log.info("Send camera client info - ", camDesc);
});

// /*******************
//  * Start Streaming
//  *******************/
// socket.on('start-video-stream', function() {
//     log.info("Receive [ START STREAM ] request");
//     if (!currStreaming) {
//         log.debug("Start Streaming video.");
//         currStreaming = true;
//         videoStreamFunc = setInterval(() => {
//             // const frame = vCap.read();
//             //  const image = cv.imencode(".jpg", frame).toString('base64');

//             socket.emit("incoming video stream", {
//                 send_datetime: new Date(),
//                 cam_serial: CAM_SERIAL,
//                 cam_view_list: CAM_VIEWS,
//                 cam_feed: CAM_FEED_DICT
//             });
//         }, 1000 / FPS);
//     }
// });
// /*******************
//  * Stop Streaming
//  *******************/
// socket.on('stop-video-stream', function() {
//     console.log("Receive [ STOP STREAM ] request");
//     if (currStreaming) {
//         clearInterval(videoStreamFunc);
//         log.debug("Stop Streaming video.");
//         currStreaming = false;
//     }
// });

/*******************
 * Request snapshot
 *******************/
socket.on('request-snapshot', function(req) {
    socket.emit("reply-snapshot", {
        app_sid: req.app_sid,
        disconnect: req.auto_disconnect,
        send_datetime: new Date(),
        cam_serial: CAM_SERIAL,
        cam_view_list: CAM_VIEWS.list,
        cam_feed: CAM_FEED_DICT
    });
    console.log("Sent camera feed");
});

function updateCurrentCamState(state, can_request = false) {
    console.log("SEND STATE : \n", state);
    socket.emit("publish-camera-state", {
        serial_num: CAM_SERIAL,
        state: state,
        can_request: can_request
    });
}

function sendImageForProcessing() {
    if (CAM_VIEWS.list.length !== 0) {
        socket.emit("incoming image", {
            send_datetime: new Date(),
            cam_serial: CAM_SERIAL,
            cam_view_list: CAM_VIEWS.list,
            cam_feed: CAM_FEED_DICT
        });
        console.log("Sent camera feed for processing");

    } else {
        console.log("No camera feed for processing");
    }
}

function checkAndSendImageToServer() {
    curr_datetime = new Date();
    if (TIME_CFG.SEND_IMG_HOUR.includes(curr_datetime.getHours())) {
        if (LAST_IMG_SEND_TIME === "") {
            LAST_IMG_SEND_TIME = new Date();
            sendImageForProcessing();
            log.fatal("PROCESS 1 - Initial Transmission");
        } else {
            var send_interval = Date.dateDiff('min', LAST_IMG_SEND_TIME, new Date());
            console.log(LAST_IMG_SEND_TIME)
            if (send_interval >= TIME_INTERVAL_IN_MIN.img_process) {
                LAST_IMG_SEND_TIME = new Date();
                sendImageForProcessing();
                log.fatal("PROCESS 2 - Subsequent Transmission ", send_interval);
            } else {
                log.fatal("NOT TRIGGERED");
            }
        }
    }

}


/*#####################################################*/
/* 		IMAGE BASESTRING UPDATES - MAIN FUNCTION       */
/*#####################################################*/
// https://flaviocopes.com/node-event-loop/

const changeCamera = (targetCamLvl, targetCamSlot) => {
    var camInterface = CAM_I2C;
    console.log("Camera I2C - ", CAM_I2C[targetCamSlot]);
    currCamView = targetCamSlot;
    bus = camInterface[targetCamSlot].bus;
    oldAddr = camInterface[targetCamSlot].oldAddr;
    newAddr = camInterface[targetCamSlot].newAddr;
    // Set the address 0x11 of the I2C device at address 0xa1 on the I2C bus to 0xff
    // '0xa1', '0x11', '0xff' 0x70 0x00 0x04
    return new Promise(resolve =>
        setImmediate(() => {
            rasp2c.set(bus, oldAddr, newAddr, function(err, result) {
                if (err) {
                    console.log("Err changing cam:\n", err);
                    cam_view_disconnect_time += 1;
                    if (cam_view_disconnect_time > 5) {
                        process.exit();
                    }
                    resolve();
                } else {
                    pin7.writeSync(camInterface[targetCamSlot].pin7);
                    pin11.writeSync(camInterface[targetCamSlot].pin11);
                    pin12.writeSync(camInterface[targetCamSlot].pin12);
                    console.log(result);
                    updateCurrentCamState("Changed to [ " + targetCamLvl + " ] camera - [ Slot_" + targetCamSlot + " ]");
                    resolve();
                }
            });
        })
    );
}

var vCap;

function captureImage(targetCamLvl, targetCamSlot) {
    CAM_FEED_DICT[targetCamLvl].cap_time = new Date();
    // vCap.set(cv.CAP_PROP_FPS, FPS) - https://docs.opencv.org/3.1.0/d8/dfe/classcv_1_1VideoCapture.html#a8c6d8c2d37505b5ca61ffd4bb54e9a7c
    // console.log("Finish Setup camera -> %sX%s fps - %s, rotate 180deg : %s", IMG_WIDTH, IMG_HEIGHT, FPS, NEED_ROTATE);
    log.warn("Setup [ " + targetCamLvl + " ] camera - [ Slot_" + targetCamSlot + " ] - > ", IMG_WIDTH, " x ", IMG_HEIGHT, ", fps - ", FPS, ", rotate 180 deg: ", NEED_ROTATE[targetCamLvl]);
    try {
        // vCap = new cv.VideoCapture(0);
        // vCap.set(cv.CAP_PROP_FRAME_WIDTH, IMG_WIDTH);
        // vCap.set(cv.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT);
        const stillCamera = new StillCamera();

        const image = await stillCamera.takeImage();
        CAM_FEED_DICT[targetCamLvl].img = image; //cv.imencode(".jpg", vCap.read()).toString('base64');
        haveCamFeed =
            "lvl1:" + (CAM_FEED_DICT.lvl1.img != '') + ", lvl2:" + (CAM_FEED_DICT.lvl2.img != '') +
            ", lvl3:" + (CAM_FEED_DICT.lvl3.img != '') + ", lvl4:" + (CAM_FEED_DICT.lvl4.img != '');
        console.log("Updated CAM [" + targetCamLvl + "] - [ Slot_" + targetCamSlot + "] ->" + haveCamFeed)
        updateCurrentCamState("Updated camera view [" + targetCamLvl + "] - [ Slot_" + targetCamSlot + " ]")
            // vCap.release();
    } catch (error) {
        console.log("ERROR in capture image : ", error)
    }
}

async function changeAndCaptureImage() {
    console.log("CHANGING & CAPTURE")
    for (const cam_view of CAM_VIEWS.list) {
        console.log("Switch to [ " + cam_view + " ] camera - [ Slot_" + CAM_VIEWS.obj[cam_view] + " ]");
        await changeCamera(cam_view, CAM_VIEWS.obj[cam_view]);
        await TIME_CFG.sleep(TIME_CFG.CHANGE_CAM_INTERVAL);
        await captureImage(cam_view, CAM_VIEWS.obj[cam_view]);
        await TIME_CFG.sleep(TIME_CFG.UPDATE_CAM_FEED);
    }
    updateCurrentCamState("Updated all camera stream", true)
}

// https://www.digitalocean.com/community/tutorials/nodejs-cron-jobs-by-examples
// sudo pm2 start /opt/farmtab/farmtab-usb-video/start_video_stream_client.js  --cron "30 6,9,12,15,17 * * *"
// cron.schedule("30 6,9,12,15,17 * * *", function() {
//     console.log("ALERT - SEND IMAGES FOR PROCESSING");
//     sendImageForProcessing();
// });



const run = async() => {
    while (true) {
        await changeAndCaptureImage();
        await checkAndSendImageToServer();
        // https://stackoverflow.com/questions/14249506/how-can-i-wait-in-node-js-javascript-l-need-to-pause-for-a-period-of-time/49139664
        // await TIME_CFG.sleep(5000);
    }
}

//https://stackoverflow.com/questions/34824460/why-does-a-while-loop-block-the-event-loop
run().then(() => console.log('Done'));