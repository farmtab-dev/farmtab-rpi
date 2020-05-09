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
# FIND BY ID # 
#============#
def find_item_by_id(mongo_col_name, item_sys_id, item_name):
    print ("Find by ID "+item_name+" : "+ item_sys_id)

    try:
        mongo_conn = MongoClient(MONGODB_URI)
        #mongo_conn = MongoClient()
        #mongo_conn.the_database.authenticate(MONGODB_USER, MONGODB_PASSWORD)
        
        db = mongo_conn[MONGODB_DATABASE]
        mongo_col = db[mongo_col_name]

        query_res = mongo_col.find({"_id": ObjectId(item_sys_id)})
        res = convert_pymongo_query_result(query_res)
        
    except Exception as e:
        print("ERROR when find "+item_name)
        raise Exception(e)

    print("SUCCESS find "+item_name+", total : " + str(len(res)))
    return res[0]

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


#=========#
#  UPDATE # 
#=========#
def update_item(mongo_col_name, item_query,query_with_sys_id, item_update_value, item_name):
    print ("Update "+item_name+" : "+ str(item_query))
    if (query_with_sys_id):
        item_query = {"_id": ObjectId(item_query["item_sys_id"])}

    try:
        mongo_conn = MongoClient(MONGODB_URI)
        
        db = mongo_conn[MONGODB_DATABASE]
        mongo_col = db[mongo_col_name]

        #res = mongo_col.update(item_query, item_update_value, upsert=True)
        res = mongo_col.update(item_query, item_update_value)

    except Exception as e:
        print("ERROR when update "+item_name)
        raise Exception(e)

    print("SUCCESS update "+item_name+" : " + str(res))


#=========#
#  DELETE #  https://www.w3schools.com/python/python_mongodb_delete.asp
#=========#
def delete_many_item(mongo_col_name, item_query, item_name):
    print("Delete Many "+item_name+" : " + str(item_query))

    try:
        mongo_conn = MongoClient(MONGODB_URI)

        db = mongo_conn[MONGODB_DATABASE]
        mongo_col = db[mongo_col_name]

        res = mongo_col.delete_many(item_query)

    except Exception as e:
        print("ERROR when delete "+item_name)
        raise Exception(e)

    print("SUCCESS delete "+item_name+" : " + str(res.deleted_count))


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

#____________________________________________________________________________________

#=================#
#  FIND LAST ITEM #   https://stackoverflow.com/questions/52559576/pymongo-how-to-get-the-last-item-in-the-collection
#=================# 
def find_the_last_item(mongo_col_name, item_query, item_name):
    print ("Find Last Item "+item_name+" : "+ item_query)

    try:
        mongo_conn = MongoClient(MONGODB_URI)
        
        db = mongo_conn[MONGODB_DATABASE]
        mongo_col = db[mongo_col_name]


        last_doc = db.docs.find_one(
            item_query,
            sort=[('_id', DESCENDING)]
        )
        res = convert_pymongo_query_result(last_doc)
        
    except Exception as e:
        print("ERROR when find "+item_name)
        raise Exception(e)

    print("SUCCESS find latest "+item_name+", total : " + str(len(res)))
    return res