/***************************************  !IMPORTANT : Serial Number is unique globally
 *  RASPBERRY PI Serial Number CONFIG  *
 ***************************************/
var config = {};
config.sensor = process.env.FARMTAB_SERIAL || ""; // TO_CHANGE
config.camera = process.env.FARMTAB_SERIAL || ""; // TO_CHANGE
config.farmtab = process.env.FARMTAB_SERIAL || ""; // TO_CHANGE
module.exports = config;