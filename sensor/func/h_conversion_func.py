import json
#===============#
# OBJ <--> JSON #
#===============#
def encode_obj_to_json(target_obj):
    return json.dumps(target_obj)

#===============#
# OBJ <--> JSON #
#===============#
def decode_json_to_obj(target_json):
    return json.loads(target_json)
