from config.cfg_py_mqtt_topic import PI_CMD_HEADER, PUB_CLOUD_TOPIC
import os

def mqtt_msg_handler_main(client, mqtt_topic, mqtt_msg_str):
    is_command, cmd_action = perform_checks_on_mqtt_topic(client, mqtt_topic)
    if (is_command):
        if (cmd_action != None):
            res = perform_checks_on_command_mqtt_msg(client, mqtt_msg_str, cmd_action)
    else:
        res = perform_checks_on_basic_mqtt_msg(client, mqtt_msg_str)

    if (res):
        print("Successful")
    else:
        print("Cannot take action on Unknown Command")


#============================#
#  PERFORM CHECK : On Topic  #
#============================#
def perform_checks_on_mqtt_topic(client, mqtt_topic):
    if(mqtt_topic.startswith(PI_CMD_HEADER)):
        topic_tokens = mqtt_topic.split("/")
        cmd_action = topic_tokens[-1]
        print (cmd_action)
        return True, cmd_action  # Means it is a valid command
    return False, None

#==========================#
#  PERFORM CHECK : On Msg  #    [ Basic ]
#==========================#
def perform_checks_on_basic_mqtt_msg(client, mqtt_msg_str):
    #-----------------------------------------------------#
    #  Send_Data : Means send summary data of all sensors #
    #-----------------------------------------------------#
    if (mqtt_msg_str == "Send_Data"):
        all_data = []
        #f = open(SENSOR_DATA_CSV_FILEPATH, "rU")
        #filecontent = f.read()
        #f.close()
        #byteArr = bytes(filecontent)
        #client.publish(MQTT_PUB_CLOUD+"/data", byteArr, 0, True)
        #client.publish(MQTT_PUB_CLOUD+"/test", "Test")
        print (len(all_data))
        for data in all_data:
            client.publish(PUB_CLOUD_TOPIC["pub_data"], str(data))

    #-----------------------------------------------------------#
    #  Send_Image : Means send image (fresh captured) to cloud  #
    #-----------------------------------------------------------#
    elif(mqtt_msg_str == "Send_Image"):
        img_filepath = '' #capture_image()
        f = open(img_filepath, "rb")
        img_content = f.read()
        f.close()
        byteArr = bytes(img_content)
        client.publish(PUB_CLOUD_TOPIC["pub_img"], byteArr, 0, True)

    #--------------------------#
    #  REMOVE RETAINED MESSAGE #
    #--------------------------#
    elif(mqtt_msg_str.startswith("Delete_Retained")):
        target_topic = mqtt_msg_str.split("->")[1]
        client.publish(target_topic, "", 0, True)
        #if (target_topic.endswith("/data")):
        #    os.system("mv "+SENSOR_DATA_CSV_FILEPATH +
        #             " /opt/sensor_data/sent_rep_"+str(get_curr_date())+".csv")
    #--------#
    #  Etc.  #
    #--------#
    else:
        print("Unknown Command : " + mqtt_msg_str)
        return False  # Indicate nothing is done
    
    return True 
    
#==========================#
#  PERFORM CHECK : On Msg  #    [ CLOUD COMMAND ]
#==========================#
def perform_checks_on_command_mqtt_msg(client, mqtt_msg_str, cmd_action):
    tokens = mqtt_msg_str.split("#")
    cmd_code = tokens[0]
    cmd_lvl = tokens[1] #lvl1, lvl2
    return True

