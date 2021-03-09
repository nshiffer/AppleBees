import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pymongo
import string
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import StringIO  
import base64

color_pal = sns.color_palette("rocket")
sns.set_palette(color_pal)

client = pymongo.MongoClient("mongodb+srv://nicktest:test123@crimedatabase.3hugk.mongodb.net/<dbname>?retryWrites=true&w=majority")
cursor = client['CrimeDatabase']['OSUCrimeReport'].find()
# Expand the cursor and construct the DataFrame
df =  pd.DataFrame(list(cursor))


# https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask

# For sub string matching, join arrays as strings and make all lower case
df.offenses = df.offenses.apply(lambda x: " ".join(x).lower().strip())

# TODO this can be upgraded to a faster operation, but written like this for consistency
exclude = set(string.punctuation)
df.location = df.location.apply(lambda x: "".join(ch for ch in x if ch not in exclude).lower().strip())

mask = df.offenses.apply(lambda x: 'drug' in x)
df1 = df[mask]
agg = df1[['location','offenses']].groupby('location').agg('count').nlargest(5, 'offenses')

sns.heatmap(agg, annot=True, fmt=".1f").set_title("Violance By Location")
plt.show()
dorms = ["archer house", "baker hall", "barrett house", "blackburn house", "bowen house", "bradley hall", "busch house", "canfield hall", "drakett tower", "fechko house", "german house", "halloran house", "hanley house", "haverfield house", "houck house", "houston house", "jones tower", "lawrence tower", "lincoln tower", "mack hall", "mendoza house", "morrill tower", "morrison tower", "neil avenue dorm", "norton house", "nosker house", "parkstradley hall", "paterson hall", "pennsylvania place", "pomerene house", "raney house", "scholars east", "scholars west", "scott house", "siebert hall", "smithsteeb hall", "taylor tower", "the residence on tenth", "torres house", "veterans house"]
mask2 = df.location.apply(lambda x: x in dorms)
dorm_df = df[mask2]
dorm_agg = dorm_df[['location','offenses']].groupby('location', as_index=False, sort = True).agg('count').nlargest(5, 'offenses')

sns.barplot(x = dorm_agg.location, y = dorm_agg.offenses, data = dorm_agg).set_title("Drug Use By Dorm")
plt.show()