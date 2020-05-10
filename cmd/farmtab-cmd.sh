#!/bin/bash
source /opt/farmtab-rpi/cmd/farmtab-cmd-script.sh

Purple='\033[4;35m'      # Purple
Cyan='\033[4;36m'        # Cyan
BIWhite='\033[1;97m'      # White

print_help(){
    printf "Usage:- ${BIWhite}farmtab-cmd${NC} ${Cyan}{TARGET}${NC} ${Purple}{ACTION}${NC} \n"
    if [ $1 -eq 0 -o $1 -eq 1 ]; then
        printf "\nFOR SENSOR :-\n"
        printf "    ${Cyan}sensor${NC} ${Purple}start${NC} - Start or restart SENSOR script\n"
        printf "    ${Cyan}sensor${NC} ${Purple}stop${NC}  - Stop SENSOR script\n"
        printf "    ${Cyan}sensor${NC} ${Purple}log${NC}   - View SENSOR script's log\n"
        printf "    ${Cyan}sensor${NC} ${Purple}code${NC}  - Go to farmtab SENSOR source code dir\n"
    fi
    if [ $1 -eq 0 -o $1 -eq 2 ]; then
        printf "\nFOR CAMERA :-\n"
        printf "    ${Cyan}camera${NC} ${Purple}config${NC} - Setup camera position at the shelf\n"
        printf "    ${Cyan}camera${NC} ${Purple}start${NC}  - Start or restart CAMERA script\n"
        printf "    ${Cyan}camera${NC} ${Purple}stop${NC}   - Stop CAMERA script\n"
        printf "    ${Cyan}camera${NC} ${Purple}log${NC}    - View CAMERA script's log\n"
        printf "    ${Cyan}camera${NC} ${Purple}code${NC}   - Go to farmtab CAMERA source code dir\n"
    fi
    if [ $1 -eq 0 -o $1 -eq 3 ]; then
        printf "\nOTHERS :-\n"
        printf "    ${Cyan}serial${NC} - Reset serial number for both serial & camera\n"
        printf "    ${Cyan}mongo${NC}  - Access mongodb as farmtab_admin\n"
    fi
}

if [ "${1}" == 'sensor' ];then 
    if [ "${2}" == 'start' ];then 
        source /opt/farmtab-rpi/cmd/farmtab-env-cfg  # Run the latest environment variable
        source /opt/farmtab-rpi/cmd/farmtab-env-serial  # Run the latest environment variable
        restart_script "SENSOR" 1  "sensor_script" ${SENSOR_SERIAL}
    elif [ "${2}" == 'stop' ];then 
        stop_script "sensor_script"
    elif [ "${2}" == 'delete' ];then 
        delete_script_process "sensor_script"
    elif [ "${2}" == 'log' ];then 
        view_log "sensor_script"
    elif [ "${2}" == 'code' ];then 
        cd  /opt/farmtab-rpi/sensor
    else 
        print_help 1
    fi
elif [ "${1}" == 'camera' ];then 
    if [ "${2}" == 'start' ];then 
        source /opt/farmtab-rpi/cmd/farmtab-env-cfg  # Run the latest environment variable
        source /opt/farmtab-rpi/cmd/farmtab-env-serial  
        source /opt/farmtab-rpi/cmd/farmtab-env-camera  
        restart_script "CAMERA" 2  "camera_script" ${CAMERA_SERIAL}
    elif [ "${2}" == 'stop' ];then 
        stop_script "camera_script"
    elif [ "${2}" == 'delete' ];then 
        delete_script_process "camera_script"
    elif [ "${2}" == 'log' ];then 
        view_log "camera_script"
    elif [ "${2}" == 'code' ];then 
        cd  /opt/farmtab-rpi/camera
    elif [ "${2}" == 'config' ];then 
        source /opt/farmtab-rpi/cmd/farmtab-env-cfg  # Run the latest environment variable
        source /opt/farmtab-rpi/cmd/farmtab-env-camera  
        setup_camera_config
    elif [ "${2}" == 'preview' ];then 
        source /opt/farmtab-rpi/cmd/farmtab-env-camera-rotate  # Run the latest environment variable
        start_camera_preview
    else 
        print_help 2
    fi
elif [ "${1}" == 'mongo' ];then 
    source /opt/farmtab-rpi/cmd/farmtab-env-cfg  # Run the latest environment variable
    mongo -u ${MONGODB_ADM_USERNAME} -p ${MONGODB_ADM_PASS} --authenticationDatabase admin
elif [ "${1}" == 'serial' ];then 
    source /opt/farmtab-rpi/cmd/farmtab-env-cfg  # Run the latest environment variable
    source /opt/farmtab-rpi/cmd/farmtab-env-serial  
    change_serial_prog   
elif [ "${1}" == 'update' ];then 
    source /opt/farmtab-rpi/cmd/farmtab-env-cfg  # Run the latest environment variable
    source /opt/farmtab-rpi/cmd/farmtab-env-serial  
    source /opt/farmtab-rpi/cmd/farmtab-env-camera  
    source /opt/farmtab-rpi/cmd/farmtab-env-camera-rotate  
    update_software
else 
    print_help 0
fi