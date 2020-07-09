#!/bin/bash
source /opt/farmtab-rpi/cmd/farmtab-cmd-script.sh

Purple='\033[4;35m'      # Purple
Cyan='\033[4;36m'        # Cyan
BIWhite='\033[1;97m'      # White

load_latest_env_var(){
    source /opt/farmtab-rpi/cmd/farmtab-env-cfg  # Run the latest environment variable
    source /opt/farmtab-rpi/cmd/farmtab-env-serial  
    source /opt/farmtab-rpi/cmd/farmtab-env-camera  
    # source /opt/farmtab-rpi/cmd/farmtab-env-cam-rotate 
}

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
        printf "    ${Cyan}serial${NC} - View Raspberry Pi's serial number\n"
        printf "    ${Cyan}mongo${NC}  - Access mongodb as database admin\n"
        printf "    ${Cyan}update${NC} - Update source code from Git Repositories\n"
    fi
}




if [ "${1}" == 'sensor' ];then 
    check_curr_user "pi"
    if [ $? -eq 0 ]; then
        return
    fi
    if [ "${2}" == 'start' ];then 
        load_latest_env_var
        restart_script "SENSOR" 1  "sensor_script" ${FARMTAB_SERIAL}
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
    check_curr_user "pi"
    if [ $? -eq 0 ]; then
        return
    fi
    if [ "${2}" == 'start' ];then 
        load_latest_env_var
        restart_script "CAMERA" 2  "camera_script" ${FARMTAB_SERIAL}
    elif [ "${2}" == 'stop' ];then 
        stop_script "camera_script"
    elif [ "${2}" == 'delete' ];then 
        delete_script_process "camera_script"
    elif [ "${2}" == 'log' ];then 
        view_log "camera_script"
    elif [ "${2}" == 'code' ];then 
        cd  /opt/farmtab-rpi/camera
    elif [ "${2}" == 'config' ];then 
        load_latest_env_var
        setup_camera_config
    # elif [ "${2}" == 'preview' ];then 
    #     load_latest_env_var
    #     start_camera_preview
    else 
        print_help 2
    fi
elif [ "${1}" == 'mongo' ];then 
    load_latest_env_var
    mongo -u ${MONGODB_ADM_USERNAME} -p ${MONGODB_ADM_PASS} --authenticationDatabase admin
elif [ "${1}" == 'serial' ];then 
    if [ "${2}" == 'start' ];then 
        load_latest_env_var
        start_pi_conn_monitor_script
    elif [ "${2}" == 'stop' ];then 
        stop_script "pi_conn_monitor"
    elif [ "${2}" == 'delete' ];then 
        delete_script_process "pi_conn_monitor"
    elif [ "${2}" == 'log' ];then 
        view_log "pi_conn_monitor"
    elif [ "${2}" == 'code' ];then 
        cd  /opt/farmtab-rpi/serial
    else 
        load_latest_env_var
        view_serial_prog 
    fi
elif [ "${1}" == 'pump' ];then 
    test_pump  $2 $3
elif [ "${1}" == 'update' ];then 
    check_curr_user "root"
    if [ $? -eq 0 ]; then
        return
    fi
    load_latest_env_var 
    update_software
else 
    print_help 0
fi