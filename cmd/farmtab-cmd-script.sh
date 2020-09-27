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

check_curr_user(){
    printf "Current user :- "
    if whoami | grep -q $1 
    then
        echo -e "${BWHITE} $1 ${NC}"
        return 1
    else
        printf "${RED_BLINK} $(whoami) ${NC}"
        printf "\n  ==> Please execute farmtab-cmd command as ${BGREEN}$1${NC}\n"
        return 0
    fi
}

print_serial_number() {
    printf "\n=============================================\n"
    printf " $1 serial numbers :- "
    printf "\n------------------------\n"
        if [ -z "${FARMTAB_SERIAL}" ]; then
            echo -en "${BRED}No serial number${NC}\n"
        else
            echo -en " Serial Number (MAC Address) : ${BGWHITE}${FARMTAB_SERIAL}${NC}\n"
        fi
    if [ $2 -ne 2 ]; then
        printf "\n=============================================\n"
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
    # if [ -z "${CAM_POS}" ]; then
    #     echo -en "${BRED}No camera configuration${NC}\n"
    # else 
    #     echo -en " Camera Position : ${BGWHITE}${CAM_POS}${NC}\n"
    # fi
    if [ -z "${TOTAL_CAM}" ]; then
        echo -en "${BRED}No ArduCam configuration${NC}\n"
    else 
        echo -en " Total Cameras   : ${BGWHITE}${TOTAL_CAM}${NC}\n"
        echo -en " ArduCam slot :-\n"
        echo -en "    > Level 1    : ${BGWHITE}${CAM_SLOT_LVL1}${NC}"
        echo -en "  (Need Rotate : ${BGWHITE}${CAM_ROTATE_LVL1}${NC})\n"
        if [ $TOTAL_CAM -ge 2 ]; then
            echo -en "    > Level 2    : ${BGWHITE}${CAM_SLOT_LVL2}${NC}"
            echo -en "  (Need Rotate : ${BGWHITE}${CAM_ROTATE_LVL2}${NC})\n"
        fi
        if [ $TOTAL_CAM -ge 3 ]; then
            echo -en "    > Level 3    : ${BGWHITE}${CAM_SLOT_LVL3}${NC}"
            echo -en "  (Need Rotate : ${BGWHITE}${CAM_ROTATE_LVL3}${NC})\n"
        fi
        if [ $TOTAL_CAM -ge 4 ]; then
            echo -en "    > Level 4    : ${BGWHITE}${CAM_SLOT_LVL4}${NC}"
            echo -en "  (Need Rotate : ${BGWHITE}${CAM_ROTATE_LVL4}${NC})\n"
        fi
    fi
    printf "\n=============================================\n"
}

print_cam_tune_menu() {
    printf "\n=============================================\n"
    if [ $1 -eq 0 ]; then
        echo -en "MAIN MENU\n"
    else
        printf "\n\n"
    fi
    printf "\n------------------------\n"


    echo -en " 1 - Tune Camera Parameters\n"
    echo -en " 2 - View camera config \n"
    echo -en " 3 - Preview \n"
    echo -en " 4 - Exit \n"
    if [ -z "${TOTAL_CAM}" ]; then
        echo -en "${BRED}No ArduCam configuration${NC}\n"
    else 
        
        echo -en " Total Cameras   : ${BGWHITE}${TOTAL_CAM}${NC}\n"
        echo -en " ArduCam slot :-\n"
        echo -en "    > Level 1    : ${BGWHITE}${CAM_SLOT_LVL1}${NC}"
        echo -en "  (Need Rotate : ${BGWHITE}${CAM_ROTATE_LVL1}${NC})\n"
        if [ $TOTAL_CAM -ge 2 ]; then
            echo -en "    > Level 2    : ${BGWHITE}${CAM_SLOT_LVL2}${NC}"
            echo -en "  (Need Rotate : ${BGWHITE}${CAM_ROTATE_LVL2}${NC})\n"
        fi
        if [ $TOTAL_CAM -ge 3 ]; then
            echo -en "    > Level 3    : ${BGWHITE}${CAM_SLOT_LVL3}${NC}"
            echo -en "  (Need Rotate : ${BGWHITE}${CAM_ROTATE_LVL3}${NC})\n"
        fi
        if [ $TOTAL_CAM -ge 4 ]; then
            echo -en "    > Level 4    : ${BGWHITE}${CAM_SLOT_LVL4}${NC}"
            echo -en "  (Need Rotate : ${BGWHITE}${CAM_ROTATE_LVL4}${NC})\n"
        fi
    fi
    printf "\n=============================================\n"
}

promptyn () {
    while true; do
        read -p "$1 " yn
        case $yn in
            [Yy]* ) return 1;;
            [Nn]* ) return 0;;
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
    # if [ -z "${CAM_POS}" ]; then
    #     printf "No camera position!\n"
    #     printf "${RED_BLINK}WARNING${NC} $1 cannot be executed without proper camera configuration\n"
    #     return 0
    # elif [ -z "${TOTAL_CAM}" ]; then
    if [ -z "${TOTAL_CAM}" ]; then
        printf "Unknown total camera!\n"
        printf "${RED_BLINK}WARNING${NC} $1 cannot be executed without proper camera configuration\n"
        return 0
    elif [ -z "${CAM_SLOT_LVL1}" ]; then
        printf "Camera at level 1 has not been configured!\n"
        printf "${RED_BLINK}WARNING${NC} $1 cannot be executed without proper camera configuration\n"
        return 0
    else
        if [ "${TOTAL_CAM}" -ge 2 ]; then
            is_invalid_single_cam $1 "2" ${CAM_SLOT_LVL2};
            if [ $? -eq 1 ]; then
                return 0
            fi
        fi
        if [ "${TOTAL_CAM}" -ge 3 ]; then
            is_invalid_single_cam $1 "3" ${CAM_SLOT_LVL3};
            if [ $? -eq 1 ]; then
                return 0
            fi
        fi
        if [ "${TOTAL_CAM}" -ge 4 ]; then
            is_invalid_single_cam $1 "4" ${CAM_SLOT_LVL4};
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
# promptlr () {
#     while true; do
#         read -p ">> Current camera position at left/right side of the shelf :- " lr
#         case $lr in
#             [Ll]* ) 
#                 CAM_POS="Left"
#                 return 0;;
#             [Rr]* ) 
#                 CAM_POS="Right"
#                 return 1;;
#             * ) printf "${BRED}Press answer [ L ] or [ R ]${NC}\n";;
#         esac
#     done
# }

promptCameraNum () {
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
            if [ "${2}" == 'lvl1' ];then
                promptyn "      Rotate the camera ? [Y/N]"
                export RotateLVL1=$?
            elif [ "${2}" == 'lvl2' ]; then
                promptyn "      Rotate the camera ? [Y/N]"
                export RotateLVL2=$?
            elif [ "${2}" == 'lvl3' ]; then
                promptyn "      Rotate the camera ? [Y/N]"
                export RotateLVL3=$?
            elif [ "${2}" == 'lvl4' ]; then
                promptyn "      Rotate the camera ? [Y/N]"
                export RotateLVL4=$?
            fi
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
        echo "export CAM_SLOT_LVL${2}=A" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    elif [ $1 -eq 1 ]; then
        echo "export CAM_SLOT_LVL${2}=B" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    elif [ $1 -eq 2 ]; then
        echo "export CAM_SLOT_LVL${2}=C" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    else
        echo "export CAM_SLOT_LVL${2}=D" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    fi
    printf "${BGREEN}Committed changes for camera slot at level $2.${NC}\n"
}

commit_cam_rotate_change(){ #$1 - value $2 - lvl
    if [ $1 -eq 1 ]; then
        echo "export CAM_ROTATE_LVL${2}=YES" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    else
        echo "export CAM_ROTATE_LVL${2}=NO" >> /opt/farmtab-rpi/cmd/farmtab-env-camera
    fi
    printf "${BGREEN}Committed changes for camera rotation at level $2.${NC}\n"
}

# Left A, B, C / right D, E, F
# Level 1  Arducam slot questions A, B, C, D
setup_camera_config(){
    clear
    print_camera_config "Current" 0
    # echo -en "\n${BGWHITE}Camera position :- ${NC} ${RWhite}[ INFO! : Input L/R ]${NC}\n"
    # promptlr 
    echo -en "\n${BGWHITE}Total camera :- ${NC} ${RWhite}[ INFO! : Input 1 ~ 4 ]${NC}\n"
    promptCameraNum 
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
        # echo "export CAM_POS=${CAM_POS}" > /opt/farmtab-rpi/cmd/farmtab-env-camera
        # printf "\n${BGREEN}Committed changes for camera position.${NC}"
        echo "export TOTAL_CAM=${TOTAL_CAM}" > /opt/farmtab-rpi/cmd/farmtab-env-camera
        printf "\n${BGREEN}Committed changes for total camera.${NC}\n"
        commit_cam_change $LVL1 "1"
        commit_cam_rotate_change $RotateLVL1 "1"
        if [ $TOTAL_CAM -ge 2 ]; then
            commit_cam_change $LVL2 "2"
            commit_cam_rotate_change $RotateLVL2 "2"
        fi
        if [ $TOTAL_CAM -ge 3 ]; then
            commit_cam_change $LVL3 "3"
            commit_cam_rotate_change $RotateLVL3 "3"
        fi
        if [ $TOTAL_CAM -ge 4 ]; then
            commit_cam_change $LVL4 "4"
            commit_cam_rotate_change $RotateLVL4 "4"
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
# View Serial Number  
#------------------------------#
view_serial_prog(){
    clear
    source /opt/farmtab-rpi/cmd/farmtab-env-serial  # Run the latest environment variable
    print_serial_number "Current" 0
}
#------------------------------#
# Change Serial Number  : ABANDON
#------------------------------#
# change_serial_prog(){
#     clear
#     source /opt/farmtab-rpi/cmd/farmtab-env-serial  # Run the latest environment variable
#     print_serial_number "Current" 0
#     printf "${BYELLOW}Press [ Enter ] without input to maintain the same serial number.${NC}\n"
#     prompt_serial_input " >> Enter new serial number for sensor: " temp_sn
#     prompt_serial_input " >> Enter new serial number for camera: " temp_cm
#     need_chg=0
#     if [ -z "$temp_sn" ]; then
#         echo "No changes for sensor serial"
#         temp_sn=${SENSOR_SERIAL}
#     else 
#         printf "Sensor serial : ${BRED}${SENSOR_SERIAL}${NC}  ==> ${BGREEN}${temp_sn}${NC}\n"
#         need_chg=1
#     fi
#     if [ -z "$temp_cm" ]; then
#         echo "No changes for camera serial"
#         temp_cm=${CAMERA_SERIAL}
#     else 
#         printf "Camera serial : ${BRED}${CAMERA_SERIAL}${NC}  ==> ${BGREEN}${temp_cm}${NC}\n"
#         need_chg=1
#     fi
#     if [ $need_chg -eq 1 ]; then 
#         echo "export SENSOR_SERIAL=${temp_sn}" > /opt/farmtab-rpi/cmd/farmtab-env-serial
#         echo "export CAMERA_SERIAL=${temp_cm}" >> /opt/farmtab-rpi/cmd/farmtab-env-serial
#         printf "${BGREEN}Committed changes.${NC}"
#         source /opt/farmtab-rpi/cmd/farmtab-env-serial 
#         print_serial_number "Latest" 0
#         printf "${BRED}Remember to run command to restart script${NC}\n"
#     else
#         printf "${BGREEN}No changes${NC}\n"
#     fi

#     check_emp_serial  "Sensor serial number" " Sensor script" ${SENSOR_SERIAL}
#     check_emp_serial  "Camera serial number" "Camera script" ${CAMERA_SERIAL}
# }

#------------------------------#  # https://github.com/Unitech/pm2/issues/325#issuecomment-281580956
#  Start SENSOR/CAMERA Script  #
#------------------------------#
restart_script(){ #$1-"SENSOR/CAMERA" $2-"1/2" $3-S{APPNAME} $4-${FARMTAB_SERIAL} 
    clear
    print_serial_number "Current" ${2}
    if check_emp_serial  "${1} serial number" " ${1} script" ${4}; then
        printf "${BRED}Please run ${NC} ${BGWHITE}installation file${NC} ${BRED}to set serial number${NC}\n"
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
    promptyn "Do you want to start ${1} script with this setting? [Y/N]"
    if [ $? -eq 1 ]; then
        start_pi_conn_monitor_script
        APPNAME=$3
        pm2 describe ${APPNAME} > /dev/null
        RUNNING=$?

        if [ "${RUNNING}" -ne 0 ]; then
            printf "${BYELLOW}Starting ${1} script${NC}\n"
            if [ $2 -eq 1 ]; then 
                pm2 start  /opt/farmtab-rpi/sensor/start_pi_arduino_publisher.py --interpreter=python3 --name=${APPNAME} --silent
            else
                pm2 start  /opt/farmtab-rpi/camera/picam_python/start_picam_stream.py --interpreter=python3 --name=${APPNAME} --silent
                # pm2 start  /opt/farmtab-rpi/camera/picam_nodejs/start_picam_stream.js --name=${APPNAME} --silent
                # pm2 start  /opt/farmtab-rpi/camera/picam_nodejs/start_video_stream_client.js --name=${APPNAME} --silent
            fi
            printf "${BYELLOW}Enable ${1} script on startup${NC}\n"
            # pm2 save --silent
            pm2 save --silent --force
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

start_pi_conn_monitor_script(){
    APPNAME="pi_conn_monitor"
    pm2 describe ${APPNAME} > /dev/null
    RUNNING=$?

    if [ "${RUNNING}" -ne 0 ]; then
        printf "${BYELLOW}Starting Pi connection monitoring script${NC}\n"
        pm2 start  /opt/farmtab-rpi/serial/start_pi_conn_monitoring.js --name=${APPNAME} --silent
        printf "${BYELLOW}Enable Pi connection monitoring script on startup${NC}\n"
        # pm2 save --silent
        pm2 save --silent --force
    else
        printf "${BYELLOW}Restarting Pi connection monitoring script${NC}\n"
        pm2 restart ${APPNAME} --silent --update-env
    fi;
    printf "${BGREEN}Done${NC}\n" 
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

update_software(){
    temp_pwd=$(pwd)
    printf "${BYELLOW} Update Raspberry Pi source code${NC}\n"
    cd /opt/farmtab-rpi
    git reset --hard HEAD
    git pull
    printf "${BGREEN}Done${NC}\n"
    printf "${BYELLOW} Update Arduino source code${NC}\n"
    cd /home/pi/Arduino/farmtab-arduino
    git reset --hard HEAD
    git pull
    printf "${BGREEN}Done${NC}\n"
    cd $temp_pwd
}

# https://stackoverflow.com/questions/8903239/how-to-calculate-time-elapsed-in-bash-script
test_usb_pump(){
    sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'
    SECONDS=0
    printf "${BYELLOW}ON USB PUMP...${NC}\n"
    sudo echo '1-1' > '/sys/bus/usb/drivers/usb/bind'
    sleep $1
    sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'
    printf "${BYELLOW}OFF USB PUMP...${NC}\n"
    # do some work

    duration=$SECONDS
    printf "Result :- ${BGREEN}$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed.${NC}\n"
}

test_pump(){
    gpio mode 3 out  # Water
    gpio mode 21 out # A fertilizer
    gpio mode 22 out # B fertilizer
    SECONDS=0
    if [ $1 -eq 1 ]; then 
        printf "${BYELLOW}ON [ WATER ] PUMP...${NC}\n"
        gpio write 3 1
    elif [ $1 -eq 2 ]; then 
        printf "${BYELLOW}ON [ A fertilizer ] PUMP...${NC}\n"
        gpio write 21 1
    elif [ $1 -eq 3 ]; then 
        printf "${BYELLOW}ON [ B fertilizer ] PUMP...${NC}\n"
        gpio write 22 1
    fi

    sleep $2
    if [ $1 -eq 1 ]; then 
        printf "${BYELLOW}OFF [ WATER ] PUMP...${NC}\n"
        gpio write 3 0
    elif [ $1 -eq 2 ]; then 
        printf "${BYELLOW}OFF [ A fertilizer ] PUMP...${NC}\n"
        gpio write 21 0
    elif [ $1 -eq 3 ]; then 
        printf "${BYELLOW}OFF [ B fertilizer ] PUMP...${NC}\n"
        gpio write 22 0
    fi

    duration=$SECONDS
    printf "Result :- ${BGREEN}$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed.${NC}\n"
}