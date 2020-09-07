var config = {};
/*******************
 * TIME DECLARATION 
 *******************/
var TIME_VALUE = {
    week: 604800000,
    day: 86400000,
    hour: 3600000,
    min: 60000,
    sec: 1000
};

//  ADJUST HERE - Time interval for better result
config.TIME_INTERVAL_IN_MIN = {
    disconnect: 60, // In minutes
    img_process: 180, // In minutes
    prev_motion: 5, // In minutes
    detect_motion: 1, // In minutes
}

// https://www.htmlgoodies.com/html5/javascript/calculating-the-difference-between-two-dates-in-javascript.html
Date.dateDiff = function(datepart, fromdate, todate) {
    datepart = datepart.toLowerCase();
    var diff = todate - fromdate;
    return Math.floor(diff / TIME_VALUE[datepart]);
}
config.sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

config.CRON_JOB_INTERVAL = process.env.INTERVAL_CRON || TIME_VALUE.hour * 3;
config.CHANGE_CAM_INTERVAL = process.env.INTERVAL_CHG_CAM || TIME_VALUE.sec * 30;
config.UPDATE_CAM_FEED = process.env.INTERVAL_CAP_IMG || TIME_VALUE.sec * 10;
// config.SEND_IMG_HOUR = [6, 9, 12, 15];
config.SEND_IMG_HOUR = [7, 10, 13, 16];

/*******************
 *  EXPORT CONFIG
 ********************/
module.exports = config;