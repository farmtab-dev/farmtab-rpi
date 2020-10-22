/***************************************  !IMPORTANT : Serial Number is unique globally
 *  RASPBERRY PI Serial Number CONFIG  *
 ***************************************/
var config = {};
config.farmtab = process.env.FARMTAB_SERIAL || ""; // TO_CHANGE
config.org_name = process.env.ORG_NAME || 'images_' + config.farmtab.replace(":", "_");

module.exports = config;