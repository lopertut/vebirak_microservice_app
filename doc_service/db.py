from bson import ObjectId
from pymongo import MongoClient
import os


client = MongoClient(os.environ.get("connectin_string"))
dbname = client["doc_service"]
collection = dbname["docs"]


def create_doc(doc: dict):
    return collection.insert_one(doc)


def update_doc(doc_id, key: str, new_value):
    try:
        obj_id = ObjectId(doc_id)
    except Exception:
        return None

    try:
        return collection.find_one_and_update(
            {"_id": obj_id},
            {"$set": {key: new_value}}
        )
    except Exception:
        return None


def get_doc(doc_id):
    try:
        obj_id = ObjectId(doc_id)
    except Exception:
        return None
    
    doc = collection.find_one({"_id": ObjectId(obj_id)})

    if doc:
        doc["_id"] = str(doc["_id"])

    return doc