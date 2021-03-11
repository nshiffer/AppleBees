# Watson constants
AUTHENTICATION = 'ghODqOQRw_e9AHE4Eqg0QbcT6jdfLi9pBcS7xbSSY58Z'
DISCOVERY_VERSION = '2021-01-31'
WATSON_URL = 'https://api.us-east.discovery.watson.cloud.ibm.com/instances/7fc37f80-f2a5-4059-9db6-dbe6808abf9c'
ENVIORNMENT_ID = '5401113d-17ca-48a1-8627-c534df11a1fb'
COLLECTION_ID = 'd3e37d16-11f1-4be9-9db5-40b1f3f98c62'


# Database constants
PASSWORD = "H0g*$aP0f5CR"
DATABASE_NAME = "CrimeDatabase"
MONGO_DB_URI = "mongodb+srv://neilmckibben:" + PASSWORD + \
    "@crimedatabase.3hugk.mongodb.net/" + DATABASE_NAME + "?retryWrites=true&w=majority"


#Column ordering
columns = [{'name': 'crimeID', 'id': 'crimeID'}, {'name': 'reportDate', 'id': 'reportDate'},
{'name': 'offenses', 'id': 'offenses'}, {'name': 'location', 'id': 'location'},
{'name': 'crimeStart', 'id': 'crimeStart'}, {'name': 'crimeEnd', 'id': 'crimeEnd'},
{'name': 'disposition', 'id': 'disposition'}]
