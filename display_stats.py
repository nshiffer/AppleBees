import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pymongo import MongoClient


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)


    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    myquery = { "offenses": { "$regex": "^S" } }
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df

newTemp = pd.DataFrame({'crimeID': [1, 2, 3], 'reportDate': [1/2/10, 1/2/10, 1/2/10], 'crimeStart': [1/2/10, 1/2/10, 1/2/10], 'crimeEnd': [1/2/10, 1/2/10, 1/2/10], 'offenses': ['drugs', 'drugs', 'drugs'], 'location':['osu', 'osu','osu2'], 'disposition': ['rape','rape','rape']})
newTemp2 = pd.DataFrame({'location':['osu', 'osu','osu2','osu2', 'osu','osu3','osu4'], 'disposition': ['rape','rape','rape','rape','rape','rape','rape']})
agg = newTemp2.groupby('location')['disposition'].agg(['count'])
#heat_map_pivot = newTemp.pivot_table(index='disposition', columns='location', values='disposition', aggfunc=pd.count)

sns.heatmap(agg, annot=True, fmt=".1f")
plt.show()
