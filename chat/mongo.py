from django.conf import settings
from pymongo import MongoClient
import gridfs

client = MongoClient(settings.MONGO_DB_URI)
db = client[settings.MONGO_DB_NAME]
collection = db["images"]

fs = gridfs.GridFS(db)

def store_image(filename: str, img, content_type):
    # img -> binary data
    fs.put(img, filename=filename, content_type=content_type)
    return "OK"

def retrieve_image(filename: str):
    img_obj = fs.find_one({"filename": filename})
    return img_obj

def delete_image(filename: str):
    img_obj = fs.find_one({"filename": filename})
    fs.delete(img_obj._id)