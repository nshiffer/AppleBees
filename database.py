import pymongo
import pprint
from pymongo import MongoClient
#Starter code to get the connection going
PASSWORD = "H0g*$aP0f5CR"
DATABASE_NAME = "CrimeDatabase"
MONGO_DB_URI = "mongodb+srv://neilmckibben:" + PASSWORD + "@crimedatabase.3hugk.mongodb.net/" + DATABASE_NAME + "?retryWrites=true&w=majority"
client = MongoClient(MONGO_DB_URI)
db = client.CrimeDatabase
collection = db.OSUCrimeReport
for a in collection.find():
    print(a)
