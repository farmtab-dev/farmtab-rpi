/***************************************  !IMPORTANT : Serial Number is unique globally
 *  RASPBERRY PI Serial Number CONFIG  *
 ***************************************/
var config = {};
config.sensor = process.env.SENSOR_SERIAL || ""; // TO_CHANGE
config.camera = process.env.CAMERA_SERIAL || ""; // TO_CHANGE
module.exports = config;