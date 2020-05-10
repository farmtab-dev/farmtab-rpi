#!/bin/bash
BRED='\033[1;31m'
BNORMAL='\033[1;30m'
BGREEN='\033[1;32m'
BGWHITE='\033[1;100m'
BGWHITE='\033[1;100m'
UYellow='\033[4;33m'      # Yellow
BWHITE='\033[1;37m'       # White
RED_BLINK='\033[1;91;7;5m'
GREEN_BLINK='\033[1;92;7;5m'
BYELLOW='\033[1;33m'       # Yellow
RWhite='\033[0;37m'  
NC='\033[0m' # No Color
FARMTAB_CAM="/opt/farmtab-rpi/camera"
FARMTAB_SENSOR="/opt/farmtab-rpi/sensor"

print_serial_number() {
    printf "\n=============================================\n"
    printf " $1 serial numbers :- "
    printf "\n------------------------\n"
    if [ $2 -eq 0 ]; then
        if [ -z "${SENSOR_SERIAL}" ]; then
            echo -en "${BRED}No sensor serial number${NC}\n"
        else
            echo -en " Sensor : ${BGWHITE}${SENSOR_SERIAL}${NC}\n"
        fi
        if [ -z "${CAMERA_SERIAL}" ]; then
            echo -en "${BRED}No camera serial number${NC}\n"
        else
            echo -en " Camera : ${BGWHITE}${CAMERA_SERIAL}${NC}"
        fi
        printf "\n=============================================\n"
    elif [ $2 -eq 1 ]; then 
        if [ -z "${SENSOR_SERIAL}" ]; then
            echo -en "${BRED}No sensor serial number${NC}\n"
        else
            echo -en " Sensor : ${BGWHITE}${SENSOR_SERIAL}${NC}\n"
        fi
        printf "\n=============================================\n"
    elif [ $2 -eq 2 ]; then
        if [ -z "${CAMERA_SERIAL}" ]; then
            echo -en "${BRED}No camera serial number${NC}\n"
        else
            echo -en " Camera : ${BGWHITE}${CAMERA_SERIAL}${NC}"
        fi
    fi
}
print_camera_config() {
    if [ $2 -eq 0 ]; then
        printf "\n=============================================\n"
    else
        printf "\n\n"
    fi
    printf " $1 camera config :- "
    printf "\n------------------------\n"
    if [ -z "${CAM_POS}" ]; then
        echo -en "${BRED}No camera configuration${NC}\n"
    else 
        echo -en " Camera Position : ${BGWHITE}${CAM_POS}${NC}\n"
    fi
    if [ -z "${TOTAL_CAM}" ]; then
        echo -en "${BRED}No ArduCam configuration${NC}\n"
    else 
        echo -en " Total Cameras   : ${BGWHITE}${TOTAL_CAM}${NC}\n"
        echo -en " ArduCam slot :-\n"
        echo -en "    > Level 1    : ${BGWHITE}${CAM_LVL1}${NC}\n"
        if [ $TOTAL_CAM -ge 2 ]; then
            echo -en "    > Level 2    : ${BGWHITE}${CAM_LVL2}${NC}\n"
        fi
        if [ $TOTAL_CAM -ge 3 ]; then
            echo -en "    > Level 3    : ${BGWHITE}${CAM_LVL3}${NC}\n"
        fi
        if [ $TOTAL_CAM -ge 4 ]; then
            echo -en "    > Level 4    : ${BGWHITE}${CAM_LVL4}${NC}"
        fi
    fi
    printf "\n=============================================\n"
}

promptyn () {
    while true; do
        read -p "$1 " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) printf "${BRED}Press answer [ Y ] or [ N ]${NC}\n";;
        esac
    done
}

prompt_serial_input () {
    while true; do
        read -p "$1 " $2 
        case $2 in
            ("" | *[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_/\&?:.=-]*)
                return;;
            (*)
                echo "Invalid serial number.";;
        esac
    done
}

check_emp_serial(){
    if [ -z "${3}" ]; then
        printf "$1 is empty!\n"
        printf "${RED_BLINK}WARNING${NC} $2 cannot be executed with empty serial number\n"
        return 0
    else 
        return 1
    fi
}
is_invalid_single_cam(){ # $1 - Camera script, $2 lvl $3 value
    if [ -z "${3}" ]; then
        printf "Camera at level ${2} has not been configured!\n"
        printf "${RED_BLINK}WARNING${NC} $1 cannot be executed without proper camera configuration\n"
        return 1
    else 
        return 0
    fi
}
check_emp_cam_config(){
    if [ -z "${CAM_POS}" ]; then
        printf "No camera position!\n"
        printf "${RED_BLINK}WARNING${NC} $1 cannot be executed without proper camera configuration\n"
        return 0
    elif [ -z "${TOTAL_CAM}" ]; then
        printf "Unknown total camera!\n"
        printf "${RED_BLINK}WARNING${NC} $1 cannot be executed without proper camera configuration\n"
        return 0
    elif [ -z "${CAM_LVL1}" ]; then
        printf "Camera at level 1 has not been configured!\n"
        printf "${RED_BLINK}WARNING${NC} $1 cannot be executed without proper camera configuration\n"
        return 0
    else
        if [ "${TOTAL_CAM}" -ge 2 ]; then
            is_invalid_single_cam $1 "2" ${CAM_LVL2};
            if [ $? -eq 1 ]; then
                return 0
            fi
        fi
        if [ "${TOTAL_CAM}" -ge 3 ]; then
            is_invalid_single_cam $1 "3" ${CAM_LVL3};
            if [ $? -eq 1 ]; then
                return 0
            fi
        fi
        if [ "${TOTAL_CAM}" -ge 4 ]; then
            is_invalid_single_cam $1 "4" ${CAM_LVL4};
            if [ $? -eq 1 ]; then
                return 0
            fi
        fi
        return 1
    fi
}
#=====================#
# FOR CAMERA
#=====================#
promptlr () {
    while true; do
        read -p ">> Current camera position at left/right side of the shelf :- " lr
        case $lr in
            [Ll]* ) 
                CAM_POS="Left"
                return 0;;
            [Rr]* ) 
                CAM_POS="Right"
                return 1;;
            * ) printf "${BRED}Press answer [ L ] or [ R ]${NC}\n";;
        esac
    done
}
promptNum () {
    while true; do
        read -p ">> Number of camera connected :- " num
        case $num in
            [1]* ) 
                TOTAL_CAM=1
                return ;;
            [2]* ) 
                TOTAL_CAM=2
                return ;;
            [3]* ) 
                TOTAL_CAM=3
                return ;;
            [4]* ) 
                TOTAL_CAM=4
                return ;;
            * ) printf "${BRED}Press input a single digit [ 1 ~ 4 ]${NC}\n";;
        esac
    done
}
reset_arducam_setting(){ #reset to any value other than 0,1,2,3
    LVL1=9
    LVL2=9
    LVL3=9
    LVL4=9
}
prompt_and_check_arducam_code () {
    while true; do
        prompt_arducam_code  $1 
        check_duplicate_arducam_slot "$2" $?
        if [ $? -eq 1 ]; then
            return
        else
            printf "${BRED}Duplicate arducam slot. Must be unique for each camera view ${NC}\n"
        fi
    done
}
prompt_arducam_code () {
    while true; do
        read -p "  >> Which Arducam slot used in Level $1 :- " code 
        case $code in
            [Aa]* ) return 0;;
            [Bb]* ) return 1;;        
            [Cc]* ) return 2;;
            [Dd]* ) return 3;;
            (*) printf "${BRED}Invalid arducam slot, either A, B, C, or D.${NC}\n";;
        esac
    done
}
is_duplicate_arducam(){  #$1-checking value $2-lvl value
    if [ -z "${2}" ]; then  # Currently empty
        return 0 
    elif [ "${1}" == "${2}" ]; then   # Same, means duplicate
        return 1
    else  
        return 0
    fi
}

check_duplicate_arducam_slot(){
    if [ "${1}" == 'lvl1' ];then
        is_duplicate_arducam ${2} $LVL2
        if [ $? -eq 1 ]; then
            return 0
        fi
        is_duplicate_arducam $2 $LVL3;
        if [ $? -eq 1 ]; then
            return 0
        fi
        is_duplicate_arducam $2 $LVL4;
        if [ $? -eq 1 ]; then
            return 0
        fi
        export LVL1=$2
    elif [ "${1}" == 'lvl2' ];then
        is_duplicate_arducam ${2} $LVL1
        if [ $? -eq 1 ]; then
            return 0
        fi
        is_duplicate_arducam $2 $LVL3;
        if [ $? -eq 1 ]; then
            return 0
        fi
        is_duplicate_arducam $2 $LVL4;
        if [ $? -eq 1 ]; then
            return 0
        fi
        export LVL2=$2
    elif [ "${1}" == 'lvl3' ];then
        is_duplicate_arducam ${2} $LVL1
        if [ $? -eq 1 ]; then
            return 0
        fi
        is_duplicate_arducam $2 $LVL2;
        if [ $? -eq 1 ]; then
            return 0
        fi
        is_duplicate_arducam $2 $LVL4;
        if [ $? -eq 1 ]; then
            return 0
        fi
        export LVL3=$2
    elif [ "${1}" == 'lvl4' ];then
        is_duplicate_arducam ${2} $LVL1
        if [ $? -eq 1 ]; then
            return 0
        fi
        is_duplicate_arducam $2 $LVL2;
        if [ $? -eq 1 ]; then
            return 0
        fi
        is_duplicate_arducam $2 $LVL3;
        if [ $? -eq 1 ]; then
            return 0
        fi
        export LVL4=$2
    else
        return 0
    fi
    return 1
}

commit_cam_change(){ #$1 - value $2 - lvl
    if [ $1 -eq 0 ]; then
        echo "export CAM_LVL${2}=A" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    elif [ $1 -eq 1 ]; then
        echo "export CAM_LVL${2}=B" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    elif [ $1 -eq 2 ]; then
        echo "export CAM_LVL${2}=C" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    else
        echo "export CAM_LVL${2}=D" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    fi
    printf "${BGREEN}Committed changes for level $2.${NC}\n"
}

# Left A, B, C / right D, E, F
# Level 1  Arducam slot questions A, B, C, D
setup_camera_config(){
    clear
    print_camera_config "Current" 0
    echo -en "\n${BGWHITE}Camera position :- ${NC} ${RWhite}[ INFO! : Input L/R ]${NC}\n"
    promptlr 
    echo -en "\n${BGWHITE}Total camera :- ${NC} ${RWhite}[ INFO! : Input 1 ~ 4 ]${NC}\n"
    promptNum 
    #if promptyn "Are you using ArduCam? [Y/N]"; then
        echo -en "\n${BGWHITE}ArduCam slot setting :-${NC} ${RWhite}[ INFO! : Input A,B,C or D ]${NC}\n"
        reset_arducam_setting
        prompt_and_check_arducam_code "1" "lvl1"
        if [ $TOTAL_CAM -ge 2 ]; then
            prompt_and_check_arducam_code "2" "lvl2"
        else
            unset LVL2
        fi
        if [ $TOTAL_CAM -ge 3 ]; then
            prompt_and_check_arducam_code "3" "lvl3"
        else
            unset LVL3
        fi
        if [ $TOTAL_CAM -ge 4 ]; then
            prompt_and_check_arducam_code "4" "lvl4"
        else
            unset LVL4
        fi
        echo "export CAM_POS=${CAM_POS}" > /opt/farmtab-rpi/cmd/farmtab-env-camera
        printf "\n${BGREEN}Committed changes for camera position.${NC}"
        echo "export TOTAL_CAM=${TOTAL_CAM}" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
        printf "\n${BGREEN}Committed changes for total camera.${NC}\n"
        commit_cam_change $LVL1 "1"
        if [ $TOTAL_CAM -ge 2 ]; then
            commit_cam_change $LVL2 "2"
        fi
        if [ $TOTAL_CAM -ge 3 ]; then
            commit_cam_change $LVL3 "3"
        fi
        if [ $TOTAL_CAM -ge 4 ]; then
            commit_cam_change $LVL4 "4"
        fi
        source /opt/farmtab-rpi/cmd/farmtab-env-camera
        print_camera_config "Latest" 0
        printf "${BGREEN}Done!${NC}\n"
    #else
    #    printf "${BGREEN}Done!${NC}\n"
    #fi

} 

start_camera_preview(){
    printf "${BGREEN}Work in progress${NC}\n"
}

#------------------------------#
# Change Serial Number
#------------------------------#
change_serial_prog(){
    clear
    source /opt/farmtab-rpi/cmd/farmtab-env-serial  # Run the latest environment variable
    print_serial_number "Current" 0
    printf "${BYELLOW}Press [ Enter ] without input to maintain the same serial number.${NC}\n"
    prompt_serial_input " >> Enter new serial number for sensor: " temp_sn
    prompt_serial_input " >> Enter new serial number for camera: " temp_cm
    need_chg=0
    if [ -z "$temp_sn" ]; then
        echo "No changes for sensor serial"
        temp_sn=${SENSOR_SERIAL}
    else 
        printf "Sensor serial : ${BRED}${SENSOR_SERIAL}${NC}  ==> ${BGREEN}${temp_sn}${NC}\n"
        need_chg=1
    fi
    if [ -z "$temp_cm" ]; then
        echo "No changes for camera serial"
        temp_cm=${CAMERA_SERIAL}
    else 
        printf "Camera serial : ${BRED}${CAMERA_SERIAL}${NC}  ==> ${BGREEN}${temp_cm}${NC}\n"
        need_chg=1
    fi
    if [ $need_chg -eq 1 ]; then 
        echo "export SENSOR_SERIAL=${temp_sn}" > /opt/farmtab-rpi/cmd/farmtab-env-serial
        echo "export CAMERA_SERIAL=${temp_cm}" >> /opt/farmtab-rpi/cmd/farmtab-env-serial
        printf "${BGREEN}Committed changes.${NC}"
        source /opt/farmtab-rpi/cmd/farmtab-env-serial 
        print_serial_number "Latest" 0
        printf "${BRED}Remember to run command to restart script${NC}\n"
    else
        printf "${BGREEN}No changes${NC}\n"
    fi

    check_emp_serial  "Sensor serial number" " Sensor script" ${SENSOR_SERIAL}
    check_emp_serial  "Camera serial number" "Camera script" ${CAMERA_SERIAL}
}

#------------------------------#  # https://github.com/Unitech/pm2/issues/325#issuecomment-281580956
#  Start SENSOR/CAMERA Script  #
#------------------------------#
restart_script(){ #$1-"SENSOR/CAMERA" $2-"1/2" $3-${SENSOR_SERIAL/CAMERA_SERIAL} $4-S{APPNAME}
    clear
    print_serial_number "Current" ${2}
    if check_emp_serial  "${1} serial number" " ${1} script" ${3}; then
        printf "${BRED}Please run ${NC} ${BGWHITE}farmtab-cmd set_serial${NC} ${BRED}command to set serial number${NC}\n"
        return
    fi
    if [ ${1} == "CAMERA" ]; then
        print_camera_config "Current" 1
        check_emp_cam_config " ${1} script" 
        if [ $? -eq 0 ]; then
            printf "${BRED}Please run ${NC} ${BGWHITE}farmtab-cmd camera config${NC} ${BRED}command to configure camera position${NC}\n"
            return
        fi
    fi
    if promptyn "Do you want to start ${1} script with this setting? [Y/N]"; then
        APPNAME=$4
        pm2 describe ${APPNAME} > /dev/null
        RUNNING=$?

        if [ "${RUNNING}" -ne 0 ]; then
            printf "${BYELLOW}Starting ${1} script${NC}\n"
            if [ $2 -eq 1 ]; then 
                pm2 start  /opt/farmtab-rpi/sensor/start_pi_arduino_publisher.py --interpreter=python3 --name=${APPNAME} --silent
            else
                pm2 start  /opt/farmtab-rpi/camera/start_video_stream_client.js --name=${APPNAME} --silent
            fi
            printf "${BYELLOW}Enable ${1} script on startup${NC}\n"
            pm2 save --silent
        else
            printf "${BYELLOW}Restarting ${1} script${NC}\n"
            pm2 restart ${APPNAME} --silent --update-env
            # pm2 delete --silent ${SENSOR_APPNAME}
        fi;
        printf "${BGREEN}Done${NC}\n"
    else
        printf "${BGREEN}No changes${NC}\n"
    fi   
}


stop_script(){
    printf "${BYELLOW} Stop ${1} script${NC}\n"
    pm2 stop --silent ${1}
    printf "${BGREEN}Done${NC}\n"
}
delete_script_process(){
    printf "${BYELLOW} Remove ${1} script${NC}\n"
    pm2 delete --silent ${1}
    printf "${BYELLOW} Disable ${1} script on startup${NC}\n"
    pm2 save --silent --force
    printf "${BGREEN}Done${NC}\n"
}
view_log(){
    pm2 log ${1}
}


