import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pymongo
import string
from io import BytesIO
import base64

color_pal = sns.color_palette("rocket")
sns.set_palette(color_pal)

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
    return dorm_df

def test1():
    df = mongo_to_df()
    df = clean_data(df)
    df = location_agg_with_count(df,'location','offenses','drug',5)
    sns.barplot(x = df.location, y = df.offenses, data = df).set_title("Drug Cases By Location")
    plt.xticks(rotation=45)
    plt.autoscale()
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

def test2():
    df = mongo_to_df()
    df = clean_data(df)
    df = location_agg_with_count(df,'location','offenses','rape',5)
    sns.barplot(x = df.location, y = df.offenses, data = df).set_title("Rape Cases By Location")
    plt.xticks(rotation=45)
    plt.autoscale()
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

def test3():
    df = mongo_to_df()
    df = clean_data(df)
    df = get_dorms(df)
    df = location_agg_with_count(df,'location','offenses','drug',5)
    sns.barplot(x = df.location, y = df.offenses, data = df).set_title("Drug Cases By Dorm")
    plt.xticks(rotation=45)
    plt.autoscale()
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

    
def test4():
    df = mongo_to_df()
    df = clean_data(df)
    df = get_dorms(df)
    df = location_agg_with_count(df,'location','offenses','rape',5)
    sns.barplot(x = df.location, y = df.offenses, data = df).set_title("Rape Cases By Dorm")
    plt.xticks(rotation=45)
    plt.autoscale()
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

def dorms_v_nondorms():
    df = mongo_to_df()
    df = clean_data(df)
    df["dorm_flag"] = np.where(np.in1d(df['location'], DORMS), "Dorm", "Non-Dorm")
    df = df[["location","offenses","dorm_flag"]].groupby("offenses", as_index=False, sort = True).agg('count')

    g = sns.barplot(data=df, x="location", y="offenses", hue="dorm_flag", ci="sd", palette="dark")
    plt.show()


def percent_crime_near_dorms():
    df = mongo_to_df()
    df = clean_data(df)
    count_total = df.shape[0]
    dorm_df = get_dorms(df)
    count_dorm = dorm_df.shape[0]
    return "{:.2f}%".format(float((count_dorm/count_total) *100))

def percent_drug_related():
    df = mongo_to_df()
    df = clean_data(df)
    count_total = df.shape[0]
    mask = df["offenses"].apply(lambda x: "drug" in x)
    df1 = df[mask]
    count_dorm = df1.shape[0]
    return "{:.2f}%".format(float((count_dorm/count_total) *100))

def percent_drug_related_dorm():
    df = mongo_to_df()
    df = clean_data(df)
    df = get_dorms(df)
    count_total = df.shape[0]
    mask = df["offenses"].apply(lambda x: "drug" in x)
    df1 = df[mask]
    count_dorm = df1.shape[0]
    return "{:.2f}%".format(float((count_dorm/count_total) *100))

def percent_pot_related():
    df = mongo_to_df()
    df = clean_data(df)
    count_total = df.shape[0]
    mask = df["offenses"].apply(lambda x: "marijuana" in x)
    df1 = df[mask]
    count_dorm = df1.shape[0]
    return "{:.2f}%".format(float((count_dorm/count_total) *100))

def percent_pot_related_dorm():
    df = mongo_to_df()
    df = clean_data(df)
    df = get_dorms(df)
    count_total = df.shape[0]
    mask = df["offenses"].apply(lambda x: "marijuana" in x)
    df1 = df[mask]
    count_dorm = df1.shape[0]
    return "{:.2f}%".format(float((count_dorm/count_total) *100))

def percent_violence_related():
    df = mongo_to_df()
    df = clean_data(df)
    count_total = df.shape[0]
    mask = df["offenses"].apply(lambda x: "violence" in x)
    df1 = df[mask]
    count_dorm = df1.shape[0]
    return "{:.2f}%".format(float((count_dorm/count_total) *100))

def percent_violence_related_dorm():
    df = mongo_to_df()
    df = clean_data(df)
    df = get_dorms(df)
    count_total = df.shape[0]
    mask = df["offenses"].apply(lambda x: "violence" in x)
    df1 = df[mask]
    count_dorm = df1.shape[0]
    return "{:.2f}%".format(float((count_dorm/count_total) *100))

