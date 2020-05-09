/*============
 *  IMPORTS
 *============*/
const exec = require('child_process').exec; // https://nodejs.org/api/child_process.html#child_process_child_process_exec_command_options_callback
var MQTT_TOPIC_CONFIG = require("./cfg_js_mqtt_topics");
var MQTT_MSG_PREP = require("./farmtab_js_msg_prep");

/*===================
 *  HANDLE MQTT MSG
 *===================*/
exports.handleMQTTmessage = (mqtt_msg, client, log, curr_datetime_dict) => {
    // https://stackoverflow.com/questions/40667762/turning-on-off-raspberrypi-usb-port-programmatically
    ACTIVATE_CMD = "sudo echo '1-1' > '/sys/bus/usb/drivers/usb/bind'";
    DEACTIVATE_CMD = "sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'";

    console.log("RECEIVE MESSAGE : " + mqtt_msg.toString())
    switch (mqtt_msg.toString()) {
        case '0':
            console.log("EXECUTE DEACT");
            var usb_cmd = exec(DEACTIVATE_CMD);

            usb_cmd.stdout.on('data', function (data) {
                console.log(data.toString());
            });
            usb_cmd.stderr.on('data', (data) => {
                console.log(data.toString());
            });
            usb_cmd.on('close', (code) => {
                console.log(`child process exited with code - ${code}`);
                
                console.log("ALERT MQTT_MSG: " + mqtt_msg)
                console.log("ALERT RESPOND: " + code)
                if (code === 0) {
                    if (curr_datetime_dict.act_time === ''){
                        console.log ("NEW DATE")
                        curr_datetime_dict.act_time = new Date();
                    }
                    curr_datetime_dict.deact_time = new Date();
                    duration = curr_datetime_dict.deact_time - curr_datetime_dict.act_time;
                    res_dict = {
                        code: "success_deact",
                        content: "Successful execute deactivate command#" + curr_datetime_dict.act_time+"#"+curr_datetime_dict.deact_time+"#"+duration
                    }
                } else {
                    res_dict = {
                        code: "error_deact",
                        content: "Error execute deactivate command"
                    }
                }
                console.log(res_dict);
                pub_msg = MQTT_MSG_PREP.prepareMQTTmessage(res_dict);
                client.publish(MQTT_TOPIC_CONFIG.pub.PUB_SELF_CMD_REPLY, pub_msg);
            })
            break;
        case '1':
            console.log("EXECUTE ACT");
            var usb_cmd = exec(ACTIVATE_CMD);

            usb_cmd.stdout.on('data', function (data) {
                console.log(data.toString());
            });
            usb_cmd.stderr.on('data', (data) => {
                console.log(data.toString());
            });
            usb_cmd.on('close', (code) => {
                console.log(`child process exited with code - ${code}`);

                console.log("ALERT MQTT_MSG: " + mqtt_msg)
                console.log("ALERT RESPOND: " + code)
                if (code === 0) {
                    curr_datetime_dict.act_time = new Date();
                    res_dict = {
                        code: "success_act",
                        content: "Successful execute activation command"
                    }
                } else {
                    res_dict = {
                        code: "error_act",
                        content: "Error execute activation command"
                    }
                }
                console.log(res_dict);
                pub_msg = MQTT_MSG_PREP.prepareMQTTmessage(res_dict);
                client.publish(MQTT_TOPIC_CONFIG.pub.PUB_SELF_CMD_REPLY, pub_msg);
            })
            break;
        default:
            log.error(mqtt_msg.toString());
            return {
                code: "unknown",
                content: "Unknown MQTT Message"
            }
    }
}



/***************************************************************
exports.handleMQTTmessage2 = (mqtt_msg, log) => {
    // https://stackoverflow.com/questions/40667762/turning-on-off-raspberrypi-usb-port-programmatically
    ACTIVATE_CMD = "sudo echo '1-1' > '/sys/bus/usb/drivers/usb/bind'";
    DEACTIVATE_CMD = "sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'";
    var res = '';
    switch (mqtt_msg.toString()) {
        case '0':
            action = "deact";


            res = runCommand(DEACTIVATE_CMD);
            console.log("ALERT MQTT_MSG: " + mqtt_msg)
            console.log("ALERT RESPOND: " + res)
            if (res === "SUCCESS") {
                return {
                    code: "success_deact",
                    content: "Successful execute command"
                }
            } else {
                return {
                    code: "error_deact",
                    content: "Error execute command"
                }
            }
        case '1':
            action = "act";
            res = runCommand(ACTIVATE_CMD);
            console.log("ALERT MQTT_MSG: " + mqtt_msg)
            console.log("ALERT RESPOND: " + res)
            if (res === "SUCCESS") {
                return {
                    code: "success_act",
                    content: "Successful execute command"
                }
            } else {
                return {
                    code: "error_act",
                    content: "Error execute command"
                }
            }
        default:
            log.error(mqtt_msg.toString());
            return {
                code: "unknown",
                content: "Unknown MQTT Message"
            }
    }

   *******************
    res_dict = {
        code: "",
        content: res
    }
    console.log("ALERT : " + mqtt_msg)
    console.log("ALERT : " + res)
    res_dict.code = 'success_' + action;
    return res_dict*************
}
// https://www.geeksforgeeks.org/run-python-script-node-js-using-child-process-spawn-method/
function runCommand(cmd) {
    var usb_cmd = exec(cmd);
    console.log("HERE");
    var error_txt = '';

    usb_cmd.stdout.on('data', function (data) {
        console.log(data.toString());
        return "SUCCESS";
    });
    usb_cmd.stderr.on('data', (data) => {
        console.log(data.toString());
    });
    usb_cmd.on('close', (code) => {
        console.log(`child process exited with code - ${code}`);
    })
}
*/