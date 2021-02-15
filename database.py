import pymongo
import pprint
from pymongo import MongoClient
from pymongo import UpdateOne
import Constants
from WatsonInterface import WatsonInterface
from bson.objectid import ObjectId

# Starter code to get the connection going


class Database:
    client = MongoClient(Constants.MONGO_DB_URI)
    db = client.CrimeDatabase
    collection = db.OSUCrimeReport

    def processCrimeReport(self):
        interface = WatsonInterface()
        crime_reports = interface.createCrimeListObjects()
        requests = [UpdateOne({'crimeID': crime.crimeID},
                              {'$set': {'reportDate': crime.reportDate,
                                        'crimeStart': crime.crimeStart,
                                        'crimeEnd': crime.crimeEnd,
                                        'offenses': crime.offenses,
                                        'location': crime.location,
                                        'disposition': crime.disposition}},
                              upsert=True) for crime in crime_reports]
        print("Inserting or updating up to ", len(requests), " items...")
        self.collection.bulk_write(requests)
        print("Operation complete")

    # Only use if you want to delete ALL of the items in the database
    def delete(self):
        self.collection.remove()
