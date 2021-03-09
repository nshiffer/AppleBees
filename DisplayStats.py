import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pymongo
import string


DORMS = ["archer house", "baker hall", "barrett house", "blackburn house", "bowen house", "bradley hall", "busch house", "canfield hall", "drakett tower", "fechko house", "german house", "halloran house", "hanley house", "haverfield house", "houck house", "houston house", "jones tower", "lawrence tower", "lincoln tower", "mack hall", "mendoza house", "morrill tower", "morrison tower", "neil avenue dorm", "norton house", "nosker house", "parkstradley hall", "paterson hall", "pennsylvania place", "pomerene house", "raney house", "scholars east", "scholars west", "scott house", "siebert hall", "smithsteeb hall", "taylor tower", "the residence on tenth", "torres house", "veterans house"]

def mongo_to_df():
    client = pymongo.MongoClient("mongodb+srv://nicktest:test123@crimedatabase.3hugk.mongodb.net/<dbname>?retryWrites=true&w=majority")
    cursor = client['CrimeDatabase']['OSUCrimeReport'].find()
    df = pd.DataFrame(list(cursor))
    return df

# Should call clean for for all dealings with data
def clean_data(df):
    exclude = set(string.punctuation)
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)
    df.offenses = df.offenses.apply(lambda x: " ".join(x).lower()).apply(lambda x: "".join(ch for ch in x if ch not in exclude))
    df.location = df.location.apply(lambda x: "".join(ch for ch in x if ch not in exclude).lower())
    return df

def location_agg_with_count(df, groupby_column, agg_column, agg_var, nlarg):
    mask = df[agg_column].apply(lambda x: agg_var in x)
    df1 = df[mask]
    agg = df1[[groupby_column,agg_column]].groupby(groupby_column, as_index=False, sort = True).agg('count').nlargest(nlarg, agg_column)
    return agg

def get_dorms(df):
    mask2 = df.location.apply(lambda x: x in DORMS)
    dorm_df = df[mask2]

def test1():
    df = mongo_to_df()
    df = clean_data(df)
    df = location_agg_with_count(df,'location','offenses','drug',5)
    return df

def test2():
    df = mongo_to_df()
    df = clean_data(df)
    df = location_agg_with_count(df,'location','offenses','drug',5)
    return df







