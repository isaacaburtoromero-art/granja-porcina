from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

URI='mongodb+srv://Maikel:contraseña@cluster0.aqorakb.mongodb.net/?appName=Cluster0'
client= MongoClient(URI)

class ConexionDB:
    def __init__(self, uri, db_name="granja"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, name):
        return self.db[name]
