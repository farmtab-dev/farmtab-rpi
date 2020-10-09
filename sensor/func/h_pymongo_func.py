#http://api.mongodb.com/python/current/tutorial.html 

from pprint import pprint
from config.cfg_py_server import MONGODB_URI, MONGODB_DATABASE
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from bson.json_util import dumps
import json


#===============#
#  INSERT ITEMS # 
#===============#
def insert_item(mongo_col_name, items_list, item_name):
    print ("Store "+item_name+" : "+ str(len(items_list)))
    try:
        mongo_conn = MongoClient(MONGODB_URI)
        
        db = mongo_conn[MONGODB_DATABASE]
        mongo_col = db[mongo_col_name]

        res = mongo_col.insert(items_list)
    except Exception as e:
        print("ERROR when store "+item_name)
        raise Exception(e)

    print("SUCCESS store "+item_name+" : " + str(res))
    return res

#============#
#  FIND ALL  # 
#============#
def find_all_by_query(mongo_col_name,item_name, item_query, 
    field_restrict=None, 
    need_sorting=False, 
    sort_by=None, 
    is_ascending=False, 
    find_limit=0):
    print ("Find All "+item_name+" : "+ str(item_query))
    if (need_sorting):
        if (is_ascending):
            sort_direction = ASCENDING 
        else:
            sort_direction = DESCENDING 

    try:
        mongo_conn = MongoClient(MONGODB_URI)
        
        db = mongo_conn[MONGODB_DATABASE]
        mongo_col = db[mongo_col_name]
        if (field_restrict != None):
            if (need_sorting):
                print ("Field restict with sort")
                if (find_limit != 0):
                    query_res = mongo_col.find(item_query, field_restrict).sort(sort_by, sort_direction).limit(find_limit)
                else:
                    query_res = mongo_col.find(item_query, field_restrict).sort(sort_by, sort_direction)
            else:
                print ("Field restict without sort")
                if (find_limit != 0):
                    query_res = mongo_col.find(item_query, field_restrict).limit(find_limit)
                else:
                    query_res = mongo_col.find(item_query, field_restrict)
        else:
            if (need_sorting):
                print ("No field restict with sort")
                if (find_limit !=0):
                    query_res = mongo_col.find(item_query).sort(sort_by, sort_direction).limit(find_limit)
                else:
                    query_res = mongo_col.find(item_query).sort(sort_by, sort_direction)
            else:
                print ("No field restict without sort")
                if (find_limit !=0):
                    query_res = mongo_col.find(item_query).limit(find_limit)
                else:
                    query_res = mongo_col.find(item_query)

        res = convert_pymongo_query_result(query_res)
        
    except Exception as e:
        print("ERROR when find "+item_name)
        raise Exception(e)

    print("SUCCESS find "+item_name+",datatype:"+str(type(res))+" total : " + str(len(res)))
    return res



#=================================# https://stackoverflow.com/questions/30333299/pymongo-bson-convert-python-cursor-cursor-object-to-serializable-json-object
# CONVERT PYMONGO FIND QUERY RES  # https://stackoverflow.com/questions/4528099/convert-string-to-json-using-python
#=================================#
def convert_pymongo_query_result(pymongo_res):
    return json.loads(dumps(pymongo_res))

#===============#
# Get System ID #
#===============#
def get_mongo_doc_sys_id(doc_obj):
    return doc_obj["_id"]["$oid"]
