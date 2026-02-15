from bson import objectid
from bson.objectid import ObjectId
from pymongo import MongoClient, ReturnDocument
import json
import os
from types import Optional 


client = MongoClient(os.environ.get("connectin_string"))
dbname = client["doc_service"]
collection = dbname["docs"]


def create_doc(doc: Optional[dict], doc_path: Optional[str]):
    if doc_path:
        try:
            with open(doc_path, "r", encoding="utf-8") as f:
                doc = json.load(f)
        except FileNotFoundError:
            print(f"doc file not found: {doc_path}")
            raise
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in doc: {e}")
            raise

    return collection.insert_one(doc)


def update_doc(doc_id, key: str, new_value):
    return collection.find_one_and_update(
        {"_id": doc_id},
        {"$set": {key: new_value}},
        return_document=ReturnDocument.AFTER,
    )


def get_doc(doc_id):
    return collection.find_one({"_id": doc_id})
