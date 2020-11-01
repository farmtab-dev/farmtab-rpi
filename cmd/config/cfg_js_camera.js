var config = {};
config.debug = process.env.DEBUG || false;

/**************** 
 * CAMERA CONFIG
 ****************/
config = {};
config.fps = 24;
config.img_width = 320;
config.img_height = 240;
config.need_rotate = { // TO_CHANGE: Camera rotation for (1)
    'lvl1': process.env.CAM_ROTATE_LVL1 || false,
    'lvl2': process.env.CAM_ROTATE_LVL2 || false,
    'lvl3': process.env.CAM_ROTATE_LVL3 || false,
    'lvl4': process.env.CAM_ROTATE_LVL4 || false,
};

/*  Arducam configuration : Camera A - D / E - H. FarmTab shelf has 3 levels (2 at each side) 
 *                                                  Eg : A- C (Left Side), D - F (Right Side)
 */
config.i2c = { // Arducam slot (A - D)
    'A': {
        bus: "0x70",
        oldAddr: "0x00",
        newAddr: "0x04",
        pin7: 0,
        pin11: 0,
        pin12: 1
    },
    'B': {
        bus: "0x70",
        oldAddr: "0x00",
        newAddr: "0x05",
        pin7: 1,
        pin11: 0,
        pin12: 1
    },
    'C': {
        bus: "0x70",
        oldAddr: "0x00",
        newAddr: "0x06",
        pin7: 0,
        pin11: 1,
        pin12: 0
    },
    'D': {
        bus: "0x70",
        oldAddr: "0x00",
        newAddr: "0x07",
        pin7: 1,
        pin11: 1,
        pin12: 0
    }
};

config.cam_position = process.env.CAM_POS || 'left_cam';


config.getCamViewList = () => {
    switch (process.env.TOTAL_CAM) {
        case "4":
        case 4:
            return {
                obj: {
                    'lvl1': process.env.CAM_SLOT_LVL1 || '',
                    'lvl2': process.env.CAM_SLOT_LVL2 || '',
                    'lvl3': process.env.CAM_SLOT_LVL3 || '',
                    'lvl4': process.env.CAM_SLOT_LVL4 || ''
                },
                list: ['lvl1', 'lvl2', 'lvl3', 'lvl4']
            };
        case "3":
        case 3:
            return {
                obj: {
                    'lvl1': process.env.CAM_SLOT_LVL1 || '',
                    'lvl2': process.env.CAM_SLOT_LVL2 || '',
                    'lvl3': process.env.CAM_SLOT_LVL3 || ''
                },
                list: ['lvl1', 'lvl2', 'lvl3']
            };
        case "2":
        case 2:
            return {
                obj: {
                    'lvl1': process.env.CAM_SLOT_LVL1 || '',
                    'lvl2': process.env.CAM_SLOT_LVL2 || ''
                },
                list: ['lvl1', 'lvl2']
            };
        case "1":
        case 1:
            return {
                obj: {
                    'lvl1': process.env.CAM_SLOT_LVL1 || '',
                },
                list: ['lvl1']
            };
        default:
            return {
                obj: {},
                list: []
            };
    }
};

/*******************
 *  EXPORT CONFIG
 ********************/
module.exports = config;